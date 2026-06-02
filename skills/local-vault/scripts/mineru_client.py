"""MinerU 精准 API 客户端封装。

参考已有脚本：/Users/ligen/Documents/Projects/02 NYUAD/09 investment research/
              03 AI投研/02 中东财富分析/99 archive/convert_pdf_to_md.py
"""

from __future__ import annotations

import logging
import time
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Optional

import requests

import config


@dataclass
class ConvertResult:
    source_file: Path
    success: bool
    zip_bytes: Optional[bytes]
    error: Optional[str]
    batch_id: str
    pages: Optional[int]


class MinerUClient:
    def __init__(self, token: str, logger: logging.Logger):
        self.token = token
        self.logger = logger
        # Session 复用 TCP/TLS 连接，跨境链路下减少握手开销
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        })

    def convert_batch(
        self,
        files: list[Path],
        *,
        language: str,
        model_version: str,
        enable_formula: bool,
        enable_table: bool,
    ) -> list[ConvertResult]:
        """非流式：收集 streaming 生成器为完整列表（向后兼容）。"""
        return list(self.convert_batch_streaming(
            files,
            language=language,
            model_version=model_version,
            enable_formula=enable_formula,
            enable_table=enable_table,
        ))

    def convert_batch_streaming(
        self,
        files: list[Path],
        *,
        language: str,
        model_version: str,
        enable_formula: bool,
        enable_table: bool,
    ) -> Iterator[ConvertResult]:
        """端到端流式版：申请 URL → 并发上传 → 轮询时谁先 done 谁先下载 → yield。

        关键收益：单个慢文件不阻塞已 done 的文件下载；轮询超时只丢失那个还没好的，
        已 yield 的结果在调用方那里已经落地。
        """
        if not files:
            return
        batch_id, file_urls = self._request_upload_urls(
            files,
            language=language,
            model_version=model_version,
            enable_formula=enable_formula,
            enable_table=enable_table,
        )
        self.logger.info(
            f"  batch_id={batch_id}, model={model_version}, language={language}, "
            f"upload URLs acquired ({len(file_urls)})"
        )

        # Step 2: 并发上传到 OSS（仍然要等全部上传完才能开始轮询）
        upload_t0 = time.time()
        self._upload_files(files, file_urls)
        self.logger.info(f"  Uploaded {len(files)} files to OSS in {time.time() - upload_t0:.1f}s")

        # Step 3+4: 轮询 + 并发下载交错进行，发现 done 就丢给下载，结果就 yield
        yield from self._poll_and_download_streaming(files, batch_id)

    # ------------- Step 1: 申请上传 URL -------------

    def _request_upload_urls(
        self,
        files: list[Path],
        *,
        language: str,
        model_version: str,
        enable_formula: bool,
        enable_table: bool,
    ) -> tuple[str, list[str]]:
        url = f"{config.MINERU_API_BASE}/file-urls/batch"
        body = {
            "files": [{"name": f.name} for f in files],
            "model_version": model_version,
            "enable_formula": enable_formula,
            "enable_table": enable_table,
            "language": language,
        }
        resp = self.session.post(url, json=body, timeout=30)
        if resp.status_code == 401:
            raise RuntimeError(
                "Token rejected by MinerU (401). 请检查/更新 .env 里的 MINERU_TOKEN。"
            )
        data = resp.json()
        if resp.status_code != 200 or data.get("code") != 0:
            raise RuntimeError(f"申请上传 URL 失败：{data}")
        return data["data"]["batch_id"], data["data"]["file_urls"]

    # ------------- Step 2: 上传 (并发 + 重试) -------------

    def _upload_files(self, files: list[Path], upload_urls: list[str]) -> None:
        """并发上传所有文件。任一文件多次重试仍失败 → 抛异常终止本批。"""
        # 开始前列一个总览，避免大文件期间日志静默看起来"卡住"
        total_mb = sum(f.stat().st_size for f in files) / (1024 * 1024)
        self.logger.info(
            f"  Uploading {len(files)} files ({total_mb:.1f} MB total, "
            f"max {config.UPLOAD_MAX_WORKERS} concurrent)..."
        )
        for f in files:
            self.logger.info(f"    → {f.name} ({f.stat().st_size / 1024:.0f} KB)")

        def upload_one(item: tuple[Path, str]) -> None:
            path, url = item
            t0 = time.time()
            self._http_put_with_retry(url, path)
            size_kb = path.stat().st_size / 1024
            self.logger.info(
                f"  ✓ uploaded {path.name} ({size_kb:.0f} KB in {time.time() - t0:.1f}s)"
            )

        with ThreadPoolExecutor(max_workers=config.UPLOAD_MAX_WORKERS) as pool:
            list(pool.map(upload_one, zip(files, upload_urls)))

    def _http_put_with_retry(self, url: str, path: Path) -> None:
        """PUT 单个文件，带指数退避重试。最终仍失败则抛 RuntimeError。"""
        last_err = "unknown"
        for attempt in range(1, config.HTTP_MAX_RETRIES + 1):
            try:
                with open(path, "rb") as f:
                    resp = requests.put(url, data=f, timeout=300)  # OSS URL 不带 token，直接用 requests
                if resp.status_code in (200, 201):
                    return
                last_err = f"HTTP {resp.status_code}"
            except requests.exceptions.RequestException as exc:
                last_err = f"{type(exc).__name__}: {exc}"
            if attempt < config.HTTP_MAX_RETRIES:
                wait = config.HTTP_BACKOFF_SEC * (2 ** (attempt - 1))
                self.logger.warning(
                    f"  ⚠ {path.name} upload failed ({last_err}), retry in {wait}s "
                    f"({attempt}/{config.HTTP_MAX_RETRIES})"
                )
                time.sleep(wait)
        raise RuntimeError(
            f"上传失败 {path.name}: {last_err}（{config.HTTP_MAX_RETRIES} 次重试后仍失败）"
        )

    # ------------- Step 3+4 流式：轮询 + 边 done 边下载 边 yield -------------

    def _poll_and_download_streaming(
        self,
        files: list[Path],
        batch_id: str,
    ) -> Iterator[ConvertResult]:
        """
        每轮 poll：
          - 新 done 的文件 → 提交到下载线程池
          - 新 failed 的文件 → 立即 yield 失败结果
          - 已完成下载的 future → yield 对应成功/失败结果
        全部文件 yield 完即结束。轮询超时只丢未 done 的，已 yield 的不受影响。
        """
        url = f"{config.MINERU_API_BASE}/extract-results/batch/{batch_id}"
        n = len(files)
        # 各文件当前状态机
        yielded: set[int] = set()                       # 已 yield 的下标
        download_futures: dict[int, Future] = {}        # idx → 下载 Future
        pending_raw: dict[int, dict] = {}               # idx → 最新 raw（含 pages 等元数据）

        start = time.time()
        last_state_signature = None
        last_log_time = start
        self.logger.info(
            f"  Polling MinerU every {config.POLL_INTERVAL_SEC}s "
            f"(heartbeat every {config.POLL_HEARTBEAT_SEC}s), 流式下载就绪文件..."
        )

        download_pool = ThreadPoolExecutor(max_workers=config.DOWNLOAD_MAX_WORKERS)
        try:
            while len(yielded) < n:
                elapsed = int(time.time() - start)

                # 1) 先收割已完成下载的 future
                for idx in list(download_futures.keys()):
                    if idx in yielded:
                        continue
                    fut = download_futures[idx]
                    if not fut.done():
                        continue
                    src = files[idx]
                    raw = pending_raw.get(idx, {})
                    try:
                        zip_bytes = fut.result()
                        self.logger.info(
                            f"  ✓ downloaded {src.name} "
                            f"({len(zip_bytes) / 1024:.0f} KB)"
                        )
                        yield ConvertResult(
                            source_file=src, success=True, zip_bytes=zip_bytes,
                            error=None, batch_id=batch_id,
                            pages=self._extract_pages(raw),
                        )
                    except Exception as exc:
                        yield ConvertResult(
                            source_file=src, success=False, zip_bytes=None,
                            error=f"download failed: {exc}",
                            batch_id=batch_id, pages=None,
                        )
                    yielded.add(idx)

                if len(yielded) == n:
                    break

                # 2) 轮询超时检查：把还没结束的标失败 yield，整批退出
                if elapsed > config.POLL_TIMEOUT_SEC:
                    self.logger.error(
                        f"  ⚠ 轮询超时（>{config.POLL_TIMEOUT_SEC}s），剩 {n - len(yielded)} 个文件未完成"
                    )
                    for idx in range(n):
                        if idx in yielded:
                            continue
                        yield ConvertResult(
                            source_file=files[idx], success=False, zip_bytes=None,
                            error=f"poll timeout after {elapsed}s",
                            batch_id=batch_id, pages=None,
                        )
                        yielded.add(idx)
                    break

                # 3) Poll once
                try:
                    resp = self.session.get(url, timeout=30)
                    data = resp.json()
                except requests.exceptions.RequestException as exc:
                    self.logger.warning(f"  Poll network error: {exc}")
                    time.sleep(config.POLL_INTERVAL_SEC)
                    continue
                if resp.status_code != 200 or data.get("code") != 0:
                    self.logger.warning(f"  Poll error: {data}")
                    time.sleep(config.POLL_INTERVAL_SEC)
                    continue

                raw_results = data["data"].get("extract_result", [])
                # raw_results 按 file_name 不一定按输入顺序，逐个用位置对齐
                for idx, raw in enumerate(raw_results[:n]):
                    pending_raw[idx] = raw
                    if idx in yielded or idx in download_futures:
                        continue
                    state = raw.get("state")
                    if state == "done":
                        zip_url = raw.get("full_zip_url")
                        if zip_url:
                            download_futures[idx] = download_pool.submit(
                                self._http_get_with_retry, zip_url
                            )
                            self.logger.info(
                                f"  → dispatched download for {files[idx].name}"
                            )
                        else:
                            yield ConvertResult(
                                source_file=files[idx], success=False, zip_bytes=None,
                                error="state=done but no full_zip_url",
                                batch_id=batch_id, pages=None,
                            )
                            yielded.add(idx)
                    elif state == "failed":
                        err = raw.get("err_msg") or "failed"
                        self.logger.error(f"  ✗ {files[idx].name}: {err}")
                        yield ConvertResult(
                            source_file=files[idx], success=False, zip_bytes=None,
                            error=err, batch_id=batch_id, pages=None,
                        )
                        yielded.add(idx)

                # 4) 心跳 log（不刷屏）
                done = sum(1 for r in raw_results if r.get("state") == "done")
                failed = sum(1 for r in raw_results if r.get("state") == "failed")
                running_details = [
                    f"{r.get('file_name', '?')} "
                    f"{(r.get('extract_progress') or {}).get('extracted_pages', '?')}/"
                    f"{(r.get('extract_progress') or {}).get('total_pages', '?')}p"
                    for r in raw_results
                    if r.get("state") == "running" and r.get("extract_progress")
                ]
                signature = (done, failed, len(yielded), len(download_futures))
                now = time.time()
                if signature != last_state_signature or (now - last_log_time) >= config.POLL_HEARTBEAT_SEC:
                    msg = (
                        f"  [{elapsed}s] {done}/{len(raw_results)} done, "
                        f"{failed} failed · {len(yielded)} yielded, "
                        f"{len(download_futures) - len(yielded)} downloading"
                    )
                    if running_details:
                        msg += " · running: " + ", ".join(running_details[:3])
                        if len(running_details) > 3:
                            msg += f" (+{len(running_details) - 3} more)"
                    self.logger.info(msg)
                    last_state_signature = signature
                    last_log_time = now

                time.sleep(config.POLL_INTERVAL_SEC)
        finally:
            download_pool.shutdown(wait=False)

    def _http_get_with_retry(self, url: str) -> bytes:
        """GET 一个 OSS URL，带指数退避重试。"""
        last_err = "unknown"
        for attempt in range(1, config.HTTP_MAX_RETRIES + 1):
            try:
                resp = requests.get(url, timeout=120)
                if resp.status_code == 200:
                    return resp.content
                last_err = f"HTTP {resp.status_code}"
            except requests.exceptions.RequestException as exc:
                last_err = f"{type(exc).__name__}: {exc}"
            if attempt < config.HTTP_MAX_RETRIES:
                wait = config.HTTP_BACKOFF_SEC * (2 ** (attempt - 1))
                self.logger.warning(
                    f"  ⚠ ZIP download failed ({last_err}), retry in {wait}s "
                    f"({attempt}/{config.HTTP_MAX_RETRIES})"
                )
                time.sleep(wait)
        raise RuntimeError(f"ZIP 下载失败：{last_err}")

    @staticmethod
    def _extract_pages(raw: dict) -> Optional[int]:
        prog = raw.get("extract_progress") or {}
        return prog.get("total_pages")

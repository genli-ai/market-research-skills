"""配置常量与 .env 加载。

路径默认从本文件位置推导（PROJECT_ROOT 下的 01/02），但可被环境变量覆盖，
方便把这套脚本打包成 skill / 装到别处时指向任意 vault：
  KB_SOURCE_DIR   原始文件目录（默认 PROJECT_ROOT/"02 原始知识库"）
  KB_TARGET_DIR   产出 MD 的 vault 目录（默认 PROJECT_ROOT/"01 MD知识库"）
  KB_ORPHANED_DIR 孤儿暂存目录（默认 PROJECT_ROOT/"orphaned"）
  KB_LOG_DIR      日志目录（默认 TOOL_DIR/"logs"）
"""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

TOOL_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TOOL_DIR.parent

# .env 要在读取 KB_* / MINERU_TOKEN 之前加载
load_dotenv(TOOL_DIR / ".env")


def _env_path(name: str) -> Optional[Path]:
    """环境变量里的路径（展开 ~ 并 resolve）；未设返回 None。"""
    v = os.getenv(name)
    return Path(v).expanduser().resolve() if v else None


SOURCE_DIR = _env_path("KB_SOURCE_DIR") or (PROJECT_ROOT / "02 原始知识库")
TARGET_DIR = _env_path("KB_TARGET_DIR") or (PROJECT_ROOT / "01 MD知识库")
ORPHANED_DIR = _env_path("KB_ORPHANED_DIR") or (PROJECT_ROOT / "orphaned")
LOG_DIR = _env_path("KB_LOG_DIR") or (TOOL_DIR / "logs")

MINERU_TOKEN = os.getenv("MINERU_TOKEN", "")

# 是否在原始文件目录放一个可双击的 sync.command（仅 macOS）。
# 默认开；在 .env 里设 KB_NO_LAUNCHER=1 关掉（不想让脚本往数据目录写入口文件时用）。
INSTALL_CLICKABLE_LAUNCHER = (
    os.getenv("KB_NO_LAUNCHER", "").strip().lower() not in {"1", "true", "yes", "on"}
)

MINERU_API_BASE = "https://mineru.net/api/v4"
MINERU_LANGUAGE = "ch"

# MinerU profile（仅在 pymupdf4llm 处理不了的情况下兜底）
#   vlm        — 扫描件 PDF + 图片（OCR + 版面分析）
#   pipeline   — Office 文档（.doc/.docx/.ppt/.pptx）
#   html       — HTML 专用
MINERU_PROFILES = {
    "vlm": {
        "model_version": "vlm",
        "enable_formula": True,
        "enable_table": True,
    },
    "pipeline": {
        "model_version": "pipeline",
        "enable_formula": True,
        "enable_table": True,
    },
    "html": {
        "model_version": "MinerU-HTML",
        "enable_formula": False,
        "enable_table": True,
    },
}

# 扩展名 → MinerU profile。仅在 PDF 走 fallback、或非本地路径文件走 MinerU 时用。
# .pdf 走动态判断（先 pymupdf4llm，失败 fallback vlm），不在此映射里。
# .docx/.pptx/.xlsx/.html 走本地（pandoc/python-pptx/openpyxl），不进 MinerU。
# 只剩老二进制 .doc/.ppt（本地库读不了）+ 图片 走 MinerU。
EXT_TO_PROFILE = {
    ".doc": "pipeline",
    ".ppt": "pipeline",
    ".png": "vlm", ".jpg": "vlm", ".jpeg": "vlm", ".jp2": "vlm",
    ".webp": "vlm", ".gif": "vlm", ".bmp": "vlm",
}


def profile_name_for(path: Path) -> str:
    """根据文件后缀选 MinerU profile 名。未识别后缀走 vlm。"""
    return EXT_TO_PROFILE.get(path.suffix.lower(), "vlm")


def profile_for(path: Path) -> dict:
    """根据文件后缀返回 MinerU 请求体的 model_version / enable_* 字段。"""
    return MINERU_PROFILES[profile_name_for(path)]


# 本地转换路由集合（不进 MinerU 云）。各组对应一条本地处理路径。
PANDOC_EXTS = {".docx", ".rtf", ".odt", ".epub", ".html", ".htm"}  # → pandoc 转 Markdown（本地，按扩展名自动识别）；.html 抽正文去样式，本地无需 MinerU
PPTX_LOCAL_EXTS = {".pptx"}      # → python-pptx 抽文字/表格/备注 + 图片（本地，可选 OCR）
XLSX_LOCAL_EXTS = {".xlsx"}      # → openpyxl 双读（值 + 公式）（本地）
CSV_EXTS = {".csv", ".tsv"}      # → csv 模块转 Markdown 表格（本地）
PASSTHROUGH_EXTS = {".md", ".markdown", ".txt"}  # → 已是文本/Markdown，直接拷贝（仅补 frontmatter，不动正文）
# 代码/结构化文本：包进代码块（带语言标注）+ 补 frontmatter。需要加新类型在这里追加。
CODE_EXTS = {
    ".json", ".yaml", ".yml", ".toml", ".ini",
    ".py", ".js", ".ts", ".sh", ".sql", ".r",
}
# 扩展名 → 代码块 fence 语言；未列出的用去掉点的扩展名本身。
CODE_FENCE_LANG = {
    ".yml": "yaml", ".py": "python", ".js": "javascript",
    ".ts": "typescript", ".sh": "bash", ".r": "r",
}

# 音视频 → 本地 whisper 转写（mlx-whisper，Apple GPU 原生，零 token/配额）。
# 视频容器（.mp4/.mov/...）也走这里：ffmpeg 直接抽音轨喂 whisper，与音频同一条路（V1 不抽关键帧）。
TRANSCRIBE_EXTS = {
    ".mp3", ".m4a", ".wav", ".aac", ".flac", ".ogg",   # 音频
    ".mp4", ".mov", ".m4v",                            # 视频（只转音轨）
}

# 直接走 sidecar（只生成 metadata MD、不转换内容）的扩展名。
# 仅老二进制 .xls（openpyxl 读不了）；.xlsx 已改走 XLSX_LOCAL_EXTS 本地导内容。
SIDECAR_EXTS = {".xls"}

# pandoc（docx/rtf/odt/epub → Markdown）
PANDOC_CMD = "pandoc"
PANDOC_TIMEOUT_SEC = 120

# CSV/TSV 转表格的行数上限；超过截断 + 提示。
CSV_MAX_ROWS = 1000

# PPT 图片 OCR：用 claude -p 的 Read 工具把图片里的文字转出来，紧跟图片引用插入正文。
# 失败/空 → 只保留图片引用，不阻塞（fail-soft）。测试默认关（见 conftest）。
# 「智能 OCR」三件套避免每张装饰图都串行起 claude（慢的根因）：
#   ① 跳过小于 OCR_MIN_IMAGE_BYTES 的图（logo/图标/装饰，OCR 无价值）
#   ② 同一张图（blob 内容相同）只抽取 + OCR 一次，跨页复用结果
#   ③ 唯一内容图用 OCR_MAX_WORKERS 个线程并发跑
OCR_PPTX_IMAGES = True
OCR_TIMEOUT_SEC = 90
OCR_MIN_IMAGE_BYTES = 30000   # < 30KB 的图视为装饰，跳过 OCR（仍抽取+引用）
OCR_MAX_WORKERS = 4           # 并发 claude -p 数；订阅有速率限制，别开太大

# 音视频转写（本地 whisper）：纯本地、零 token/配额/API key。
# 引擎按平台自动选（可被 env 覆盖）：
#   Apple Silicon → mlx-whisper（GPU 原生、最快）；其它平台 → faster-whisper（跨平台 CPU/CUDA）。
WHISPER_ENGINE = os.getenv("KB_WHISPER_ENGINE", "auto")   # auto | mlx | faster
# 用户选过的模型档（首次在终端交互选择后写回 .env）。""=还没选；"skip"=用户选择不转写音视频。
WHISPER_MODEL_KEY = os.getenv("KB_WHISPER_MODEL", "")
WHISPER_DEFAULT_MODEL_KEY = "turbo"                       # 菜单默认 / 推荐档
# 模型档：key → {各引擎模型 id, 近似下载大小, 一句说明}。首次下、之后离线复用。
WHISPER_MODELS = {
    "tiny":     {"mlx": "mlx-community/whisper-tiny",           "faster": "tiny",           "size": "~75 MB",  "note": "最快，准确率最低（快速预览）"},
    "small":    {"mlx": "mlx-community/whisper-small",          "faster": "small",          "size": "~480 MB", "note": "速度/精度折中"},
    "turbo":    {"mlx": "mlx-community/whisper-large-v3-turbo", "faster": "large-v3-turbo", "size": "~1.6 GB", "note": "精度高 + 快"},
    "large-v3": {"mlx": "mlx-community/whisper-large-v3",       "faster": "large-v3",       "size": "~3 GB",   "note": "最高精度、最慢"},
}
WHISPER_LANGUAGE = None        # None = 自动检测（比 MinerU 写死 "ch" 好），检测结果写进产物 body
TRANSCRIBE_TIMESTAMPS = True   # 正文每段加 [mm:ss] 时间戳（音视频版「页码回溯」）；False → 纯段落

# Excel 单 sheet 导出的单元格上限；超过则截断 + 提示，避免万行表撑爆 vault。
# 用户仍可点 frontmatter 的 source 双链回 02 看全表。
EXCEL_MAX_CELLS_PER_SHEET = 5000


# PDF 转换：pymupdf4llm 输出字符密度低于此阈值（每页字符数）→ 判定为扫描件，
# fallback 到 MinerU vlm。典型数字 PDF 每页 1000-3000 字符。
PYMUPDF4LLM_MIN_CHARS_PER_PAGE = 200

# 数字版 PDF（pymupdf4llm 路）是否抽图。关掉 → 纯文字、最快、vault 不长图。
# 想要图表/示意图进 attachments 就开着；只关心文字就设 False（或 .env: KB_PDF_NO_IMAGES=1）。
PYMUPDF4LLM_WRITE_IMAGES = (
    os.getenv("KB_PDF_NO_IMAGES", "").strip().lower() not in {"1", "true", "yes", "on"}
)
# 抽图阈值：图面积小于页面的这个比例就不抽（logo / 图标 / 装饰小图无检索价值）。
# 0.12 = 页面 12%，只留大图（图表/示意图），砍掉小装饰。设 0 抽全部，设 1 基本不抽。
PYMUPDF4LLM_IMAGE_SIZE_LIMIT = 0.12
# 抽出后再按字节过滤：小于这个大小的图视为装饰/噪音，丢弃（连引用一起删）。
PYMUPDF4LLM_IMAGE_MIN_BYTES = 6000

MAX_FILE_SIZE_MB = 200
MAX_BATCH_SIZE = 200

# 并发与重试（仅影响 MinerU 调用）
UPLOAD_MAX_WORKERS = 8
DOWNLOAD_MAX_WORKERS = 8
HTTP_MAX_RETRIES = 3
HTTP_BACKOFF_SEC = 2

POLL_INTERVAL_SEC = 5
POLL_TIMEOUT_SEC = 600
POLL_HEARTBEAT_SEC = 30

# Frontmatter 富化：每个产出 MD 调 claude -p 写 abstract / tags / synonyms
# 设为 False 可关掉自动化（手动用 Claude Code 会话 enrich）
ENRICH_FRONTMATTER = True
ENRICH_CLAUDE_CMD = "claude"      # 调用的 CLI 名（必须在 PATH）
ENRICH_TIMEOUT_SEC = 90           # 单次 enrich 调用超时
ENRICH_SAMPLE_HEAD_CHARS = 5000   # 喂给 Claude 的 MD 开头字符数
ENRICH_SAMPLE_TAIL_CHARS = 5000   # 喂给 Claude 的 MD 末尾字符数

SUPPORTED_EXTS = (
    {".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".html",
     ".png", ".jpg", ".jpeg", ".jp2", ".webp", ".gif", ".bmp"}
    | PANDOC_EXTS | PPTX_LOCAL_EXTS | XLSX_LOCAL_EXTS
    | CSV_EXTS | PASSTHROUGH_EXTS | CODE_EXTS | SIDECAR_EXTS | TRANSCRIBE_EXTS
)

# 未转换文件的处理建议（report_skipped 用）。键是小写扩展名。
# 注：常见音视频（mp3/m4a/wav/mp4/mov/...）已走本地 whisper 转写（见 TRANSCRIBE_EXTS）。
UNSUPPORTED_HINTS = {
    ".numbers": "Apple Numbers 专有格式：请在 Numbers 里导出为 .xlsx 再放进 02",
    ".pages": "Apple Pages 专有格式：请在 Pages 里导出为 .docx 再放进 02",
    ".key": "Apple Keynote 专有格式：请在 Keynote 里导出为 .pptx 再放进 02",
    ".zip": "压缩包：请解压后把里面的文件放进 02（下次 sync 自动处理）",
    ".rar": "压缩包：请解压后再放进 02",
    ".7z": "压缩包：请解压后再放进 02",
}
DEFAULT_UNSUPPORTED_HINT = "当前未支持的类型；很多文本/Office 类可低成本接入，需要的话告诉维护者"

TOOL_MARKER = "MinerU"
# is_tool_generated 接受的 converted_by marker。增加新转换器时在这里加一项。
# excel-sidecar 保留兼容存量（旧 xlsx sidecar + 当前 .xls sidecar）。
KNOWN_CONVERTERS = (
    "MinerU", "pymupdf4llm", "excel-sidecar",
    "pandoc", "python-pptx", "excel-openpyxl", "passthrough", "csv", "whisper",
)

# prune_empty_dirs 保留的顶层子目录名（含其所有子孙）。
# 以 '.' 开头的目录（.obsidian / .claudian / .git / ...）自动跳过，无需在此列。
PROTECTED_TARGET_DIR_NAMES = {"索引"}

# 删空目录时可一并清掉的 OS 残留文件——只剩这些时该目录视作"空"。
# macOS Finder/Obsidian 一进目录就生成 .DS_Store，会让 rmdir 误判非空。
# 仅精确匹配这些名字 + AppleDouble `._*` 前缀；绝不动其它用户文件。
PRUNABLE_CRUFT_NAMES = {".DS_Store", "Thumbs.db", ".localized"}

DEFAULT_TAGS = ["自动生成", "待整理"]

"""Jinja2 渲染器：把 Briefing 渲染为最终 HTML。

模板设计同时兼容浏览器查看 + 复制粘贴进微信公众号编辑器：
  - 全 inline `style=""`，不依赖 `<style>` 块
  - `<table>` 嵌套布局，背景色 / 横条放在 `<td>` 上
  - 装饰元素用实体 `<span>` / `<td>`，不用伪元素 / 渐变 / CSS 变量
"""
from __future__ import annotations
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

from .schema import Briefing

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"


def render_briefing(briefing: Briefing, template: str = "briefing.html") -> str:
    """渲染单期简报为完整 HTML 字符串。"""
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=select_autoescape(["html"]),
    )

    seen_urls: list[str] = []

    def footnote_index(url: str) -> int:
        if url not in seen_urls:
            seen_urls.append(url)
        return seen_urls.index(url) + 1

    tmpl = env.get_template(template)
    all_sources = briefing.all_sources()
    for s in all_sources:
        footnote_index(s.url)
    return tmpl.render(
        briefing=briefing,
        all_sources=all_sources,
        footnote_index=footnote_index,
    )


def save_briefing(briefing: Briefing, out_dir,
                  template: str = "briefing.html",
                  filename=None):
    """渲染并保存到磁盘，返回文件路径。"""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    if filename is None:
        safe = briefing.issue_title.replace("/", "_").replace(" ", "_")[:60]
        filename = f"{briefing.period_end}_{safe}.html"

    html = render_briefing(briefing, template=template)
    p = out_dir / filename
    p.write_text(html, encoding="utf-8")
    return p

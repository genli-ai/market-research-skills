"""Briefing 数据结构 —— 主题观察简报的标准 schema。

一份 briefing JSON 应该有以下顶层字段：

  brand_name        显示在 HTML 封面顶部的品牌名（默认 "TOPIC BRIEF"）
  subject_name      本期主题（如 "中东" / "半导体" / "AI 立法" / "美联储"）
  issue_title       主标题，一句话核心结论，含数字 + 机构名
  period_start      "YYYY-MM-DD"
  period_end        "YYYY-MM-DD"
  period_label      显示用，如 "5.1-5.12"
  summary           本期要点（焦点摘要 + 4 条子板块速览）
  focus             焦点观察长文（标题/副标题/正文 sections）
  sections          4 个子板块，每个含 3-4 条 items
  disclaimer        免责声明（默认值见下）

历史项目（一带一路观察）用的字段是 region_name + regions，新 skill 用
subject_name + sections，from_dict 时兼容老字段。
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import date
from typing import List, Optional
import json
import re

DEFAULT_DISCLAIMER = (
    "本产品中的信息是基于公众媒体或其它第三方公开披露的信息编制而成。"
    "本产品不构成买卖任何投资工具或者达成任何交易的推荐，亦不构成财务、法律、税务、"
    "投资建议、投资咨询意见或其他意见。本产品所提供信息仅供接收者参考。"
)
EVENT_DATE_FORMAT_MESSAGE = "event_date must use YYYY-MM-DD or YYYY-MM"
FULL_DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}")
MONTH_PATTERN = re.compile(r"\d{4}-\d{2}")


@dataclass
class SourceRef:
    """脚注引用：媒体或机构名 + URL。"""
    label: str
    url: str


@dataclass
class Item:
    """单条新闻条目。"""
    headline: str            # ≤30 字，含数字或明确结论
    body: str                # 100-300 字
    source: SourceRef
    event_date: str = ""  # YYYY-MM-DD 或 YYYY-MM；旧版 regions 可为空


@dataclass
class Section:
    """子板块。4 个子板块用什么轴分由 subject 决定：
       - 区域主题 → 按国家或地理子区域（沙特/UAE/卡塔尔/OPEC+）
       - 行业主题 → 按价值链环节或主体（设计/制造/封测/政策）
       - 议题主题 → 按时间线或维度（立法/执行/争议/影响）
       - 机构主题 → 按职能或主题域（货币/金融稳定/支付/研究）
    """
    label: str
    items: List[Item] = field(default_factory=list)


@dataclass
class SummaryItem:
    """本期要点中的一句话速览。"""
    label: str
    text: str


@dataclass
class Summary:
    """本期要点框。"""
    focus_blurb: str
    items: List[SummaryItem] = field(default_factory=list)


@dataclass
class Focus:
    """焦点观察长文。"""
    title: str
    subtitle: Optional[str] = None
    source_org: str = ""
    source_url: str = ""
    image_url: Optional[str] = None
    sections: List[dict] = field(default_factory=list)


@dataclass
class Briefing:
    """一期完整简报。"""
    issue_title: str
    period_start: str
    period_end: str
    period_label: str
    subject_name: str = ""
    brand_name: str = "TOPIC BRIEF"
    author: str = "developed by Gen"                       # 封面左下角作者/团队信息。显式 "" 表示不显示
    summary: Summary = field(default_factory=lambda: Summary(""))
    focus: Focus = field(default_factory=lambda: Focus(""))
    sections: List[Section] = field(default_factory=list)
    disclaimer: str = DEFAULT_DISCLAIMER

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    @classmethod
    def from_dict(cls, d: dict) -> "Briefing":
        """从 dict 构建。兼容旧 schema 的字段别名:
             region_name → subject_name
             regions     → sections
             region_items → items（summary 内）
             region_label → label（summary item 内）
        """
        period_start = _parse_iso_date(d["period_start"], "period_start")
        period_end = _parse_iso_date(d["period_end"], "period_end")
        if period_start > period_end:
            raise ValueError("period_start must not be after period_end")

        focus_d = d.get("focus", {})
        focus = Focus(
            title=focus_d.get("title", ""),
            subtitle=focus_d.get("subtitle"),
            source_org=focus_d.get("source_org", ""),
            source_url=focus_d.get("source_url", ""),
            image_url=focus_d.get("image_url"),
            sections=focus_d.get("sections", []),
        )

        s = d.get("summary", {})
        items_data = s.get("items", s.get("region_items", []))
        summary = Summary(
            focus_blurb=s.get("focus_blurb", ""),
            items=[
                SummaryItem(
                    label=si.get("label", si.get("region_label", "")),
                    text=si["text"],
                )
                for si in items_data
            ],
        )

        uses_legacy_regions = "sections" not in d and "regions" in d
        sec_data = d.get("sections", d.get("regions", []))
        sections = [
            Section(
                label=sec.get("label", ""),
                items=[
                    _item_from_dict(
                        it,
                        period_start=period_start,
                        period_end=period_end,
                        allow_missing_event_date=uses_legacy_regions,
                    )
                    for it in sec.get("items", [])
                ],
            )
            for sec in sec_data
        ]

        return cls(
            issue_title=d["issue_title"],
            period_start=d["period_start"],
            period_end=d["period_end"],
            period_label=d["period_label"],
            subject_name=d.get("subject_name", d.get("region_name", "")),
            brand_name=d.get("brand_name", cls.__dataclass_fields__["brand_name"].default),
            author=d.get("author", cls.__dataclass_fields__["author"].default),
            summary=summary,
            focus=focus,
            sections=sections,
            disclaimer=d.get("disclaimer", DEFAULT_DISCLAIMER),
        )

    def all_sources(self) -> List[SourceRef]:
        """聚合所有 URL 用于脚注列表（保持出现顺序，去重在渲染器里处理）。"""
        out: List[SourceRef] = []
        if self.focus.source_url:
            out.append(SourceRef(
                label=self.focus.source_org or "焦点报告",
                url=self.focus.source_url,
            ))
        for sec in self.sections:
            for it in sec.items:
                out.append(it.source)
        return out


def _parse_iso_date(value: str, field_name: str) -> date:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must use YYYY-MM-DD")
    if FULL_DATE_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{field_name} must use YYYY-MM-DD")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field_name} must use YYYY-MM-DD") from exc


def _validate_event_date(
    value: str,
    period_start: date,
    period_end: date,
) -> None:
    if not isinstance(value, str):
        raise ValueError(EVENT_DATE_FORMAT_MESSAGE)
    if MONTH_PATTERN.fullmatch(value) is not None:
        try:
            date.fromisoformat(f"{value}-01")
        except ValueError as exc:
            raise ValueError(EVENT_DATE_FORMAT_MESSAGE) from exc
        start_month = period_start.strftime("%Y-%m")
        end_month = period_end.strftime("%Y-%m")
        if start_month <= value <= end_month:
            return
    elif FULL_DATE_PATTERN.fullmatch(value) is not None:
        try:
            parsed = date.fromisoformat(value)
        except ValueError as exc:
            raise ValueError(EVENT_DATE_FORMAT_MESSAGE) from exc
        if period_start <= parsed <= period_end:
            return
    else:
        raise ValueError(EVENT_DATE_FORMAT_MESSAGE)
    raise ValueError("event_date must fall within the briefing period")


def _item_from_dict(
    item: dict,
    *,
    period_start: date,
    period_end: date,
    allow_missing_event_date: bool,
) -> Item:
    event_date = item.get("event_date", "")
    if not event_date and not allow_missing_event_date:
        raise ValueError("Each sections item requires event_date")
    if event_date:
        _validate_event_date(event_date, period_start, period_end)
    return Item(
        headline=item["headline"],
        body=item["body"],
        source=SourceRef(**item["source"]),
        event_date=event_date,
    )

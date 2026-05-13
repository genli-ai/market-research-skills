"""撰写器：把种子 JSON 装入 Briefing 对象。

写正文这一步由 Claude 在会话中扮演（按 SKILL.md 的工作流指引）。
本模块只负责"种子 JSON → Briefing 对象"这一段。
"""
from __future__ import annotations
from .schema import Briefing


def write_briefing_mock(seed: dict) -> Briefing:
    """把种子 dict 装入 Briefing，schema 校验由 from_dict 完成。"""
    return Briefing.from_dict(seed)

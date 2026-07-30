from __future__ import annotations

import copy
import importlib
import sys
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TOPIC_BRIEF_ROOT = REPOSITORY_ROOT / "skills" / "topic-brief"
sys.path.insert(0, str(TOPIC_BRIEF_ROOT))

render_briefing = importlib.import_module("lib.renderer").render_briefing
Briefing = importlib.import_module("lib.schema").Briefing


def briefing_seed(event_date: str | None = "2026-05-05") -> dict:
    item = {
        "headline": "A verified development",
        "body": "A source-backed briefing item.",
        "source": {
            "label": "Example",
            "url": "https://example.com/report",
        },
    }
    if event_date is not None:
        item["event_date"] = event_date
    return {
        "issue_title": "Example briefing",
        "period_start": "2026-05-01",
        "period_end": "2026-05-31",
        "period_label": "May 2026",
        "subject_name": "Example",
        "summary": {"focus_blurb": "", "items": []},
        "focus": {
            "title": "Example",
            "source_org": "Example",
            "source_url": "https://example.com/report",
            "sections": [],
        },
        "sections": [{"label": "Updates", "items": [item]}],
    }


class TopicBriefEventDateTests(unittest.TestCase):
    def test_event_date_survives_round_trip_and_rendering(self):
        briefing = Briefing.from_dict(briefing_seed())
        item = briefing.sections[0].items[0]

        self.assertEqual(item.event_date, "2026-05-05")
        self.assertEqual(
            briefing.to_dict()["sections"][0]["items"][0]["event_date"],
            "2026-05-05",
        )
        self.assertIn("2026-05-05", render_briefing(briefing))

    def test_new_schema_requires_event_date(self):
        with self.assertRaisesRegex(
            ValueError,
            "Each sections item requires event_date",
        ):
            Briefing.from_dict(briefing_seed(event_date=None))

    def test_rejects_event_date_outside_period(self):
        with self.assertRaisesRegex(
            ValueError,
            "event_date must fall within the briefing period",
        ):
            Briefing.from_dict(briefing_seed(event_date="2026-04-30"))

    def test_rejects_noncanonical_event_date(self):
        with self.assertRaisesRegex(
            ValueError,
            "event_date must use YYYY-MM-DD or YYYY-MM",
        ):
            Briefing.from_dict(briefing_seed(event_date="20260505"))

    def test_accepts_month_granularity_within_period(self):
        briefing = Briefing.from_dict(briefing_seed(event_date="2026-05"))

        self.assertEqual(briefing.sections[0].items[0].event_date, "2026-05")

    def test_legacy_regions_remain_compatible(self):
        seed = copy.deepcopy(briefing_seed(event_date=None))
        seed["regions"] = seed.pop("sections")

        briefing = Briefing.from_dict(seed)

        self.assertEqual(briefing.sections[0].items[0].event_date, "")


if __name__ == "__main__":
    unittest.main()

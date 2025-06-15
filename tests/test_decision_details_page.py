import unittest

from cabinet.web import ContentsPage


class TestCase(unittest.TestCase):
    def test_cabinet_decision(self):
        page = (
            ContentsPage()
            .get_year_page("2025")
            .get_day_page("2025-01-06")
            .decision_details_page_list[0]
        )
        decision = page.cabinet_decision
        self.assertEqual(decision.decision_num, 1)
        self.assertEqual(
            decision.title,
            "Agreement on Co-operation and Mutual Assistance in"
            + " Customs Matters between Sri Lanka and Vietnam",
        )
        self.assertEqual(
            decision.decision_details[:40],
            "- Although approval of the Cabinet had b",
        )

        self.assertEqual(
            decision.decision_details[-40:],
            "nd Vietnam, was approved by the Cabinet.",
        )

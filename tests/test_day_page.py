import unittest

from cabinet import CabinetDecision, ContentsPage


class TestCase(unittest.TestCase):
    def test_decision_list(self):
        day_page = (
            ContentsPage().get_year_page("2025").get_day_page("2025-01-06")
        )
        decision_list = day_page.cabinet_decision_list
        self.assertEqual(len(decision_list), 17)

        first_decision = decision_list[0]

        self.assertEqual(
            first_decision,
            CabinetDecision(
                decision_num=1,
                title="Agreement on Co-operation and Mutual Assistance in"
                + " Customs Matters between Sri Lanka and Vietnam",
            ),
        )

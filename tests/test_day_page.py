import unittest

from cabinet import ContentsPage


class TestCase(unittest.TestCase):
    def test_decision_details_page_list(self):
        day_page = (
            ContentsPage().get_year_page("2025").get_day_page("2025-01-06")
        )
        decision_details_page_list = day_page.decision_details_page_list
        self.assertEqual(len(decision_details_page_list), 17)
        first_page = decision_details_page_list[0]
        self.assertEqual(first_page.decision_num, 1)
        self.assertEqual(
            first_page.title,
            "Agreement on Co-operation and Mutual Assistance in"
            + " Customs Matters between Sri Lanka and Vietnam",
        )
        self.assertEqual(
            first_page.params,
            {
                "option": "com_content",
                "view": "article",
                "id": "16",
                "Itemid": "49",
                "dID": "12973",
                "lang": "en",
            },
        )

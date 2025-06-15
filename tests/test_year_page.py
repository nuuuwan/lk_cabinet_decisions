import unittest

from cabinet import ContentsPage


class TestCase(unittest.TestCase):

    def test_day_page_idx(self):
        year_page = ContentsPage().get_year_page("2025")
        day_page_idx = year_page.day_page_idx
        self.assertGreater(len(day_page_idx), 10)

    def test_get_day_page(self):
        year_page = ContentsPage().get_year_page("2025")
        with self.assertRaises(ValueError):
            year_page.get_day_page("2025-01-01")

        day_page = year_page.get_day_page("2025-01-06")
        self.assertEqual(
            day_page.params,
            {
                "option": "com_content",
                "view": "article",
                "id": "15",
                "Itemid": "49",
                "dDate": "2025-01-06",
                "lang": "en",
            },
        )

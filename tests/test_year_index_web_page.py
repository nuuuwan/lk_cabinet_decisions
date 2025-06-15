import unittest

from cabinet import YearIndexPage


class TestCase(unittest.TestCase):
    def test_content(self):
        page = YearIndexPage()
        content = page.content
        self.assertGreater(len(content), 30_000)

    def test_year_to_url(self):
        page = YearIndexPage()
        year_to_year_page_list = page.year_to_year_page_list
        self.assertGreater(len(year_to_year_page_list), 10)
        self.assertEqual(
            year_to_year_page_list["2025"].params,
            {
                "option": "com_content",
                "view": "article",
                "id": "63",
                "Itemid": "116",
                "lang": "en",
            },
        )

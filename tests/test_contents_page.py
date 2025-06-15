import unittest

from cabinet import ContentsPage


class TestCase(unittest.TestCase):
    def test_content(self):
        page = ContentsPage()
        content = page.content
        self.assertGreater(len(content), 30_000)

    def test_year_page_idx(self):
        page = ContentsPage()
        year_page_idx = page.year_page_idx
        self.assertGreater(len(year_page_idx), 10)

    def test_get_year_page(self):
        page = ContentsPage()
        year_page_idx = page.year_page_idx
        self.assertEqual(
            year_page_idx["2025"].params,
            {
                "option": "com_content",
                "view": "article",
                "id": "63",
                "Itemid": "116",
                "lang": "en",
            },
        )
        with self.assertRaises(ValueError):
            page.get_year_page("1215")

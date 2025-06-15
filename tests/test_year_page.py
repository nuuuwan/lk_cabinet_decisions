import unittest

from cabinet import YearIndexPage


class TestCase(unittest.TestCase):
    def test_init(self):
        page = YearIndexPage().get_year_page("2025")
        self.assertEqual(page.year, "2025")

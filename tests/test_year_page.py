import unittest

from cabinet import ContentsPage


class TestCase(unittest.TestCase):
    def test_init(self):
        page = ContentsPage().get_year_page("2025")
        self.assertEqual(page.year, "2025")

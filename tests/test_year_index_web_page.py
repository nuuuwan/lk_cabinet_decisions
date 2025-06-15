import unittest

from cabinet import YearIndexPage


class TestCase(unittest.TestCase):
    def test_content(self):
        page = YearIndexPage()
        content = page.content
        self.assertGreater(len(content), 30_000)

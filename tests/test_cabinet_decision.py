import os
import unittest

from cabinet import CabinetDecision


class TestCase(unittest.TestCase):
    def test_build_table(self):

        CabinetDecision.build_table()
        self.assertTrue(
            os.path.exists(CabinetDecision.CABINET_DESICIONS_TABLE_PATH)
        )
        self.assertGreater(len(CabinetDecision.list_all()), 0)

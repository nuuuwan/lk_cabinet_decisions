import os
import unittest

from cabinet import CabinetDecision, Pipeline


class TestCase(unittest.TestCase):

    def test_run(self):
        pipeline = Pipeline()
        pipeline.run(max_n_hot=10)
        self.assertTrue(
            os.path.exists(CabinetDecision.CABINET_DESICIONS_TABLE_PATH)
        )

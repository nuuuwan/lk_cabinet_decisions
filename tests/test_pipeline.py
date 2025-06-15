import os
import unittest

from cabinet import CabinetDecision, Pipeline


class TestCase(unittest.TestCase):

    def test_run(self):
        pipeline = Pipeline(do_shuffle=False)
        pipeline.run(max_n_hot=0)
        self.assertTrue(
            os.path.exists(CabinetDecision.CABINET_DESICIONS_TABLE_PATH)
        )

import os
import unittest

from cabinet import Pipeline


class TestCase(unittest.TestCase):
    def test_pipeline(self):
        pipeline = Pipeline()
        decision_list = pipeline.get_cabinet_decision_list(limit=10)
        self.assertEqual(len(decision_list), 10)

    def test_run(self):
        pipeline = Pipeline()
        pipeline.run(limit=10)
        self.assertTrue(os.path.exists(pipeline.CABINET_DESICIONS_TABLE_PATH))

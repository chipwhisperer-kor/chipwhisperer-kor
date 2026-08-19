import unittest
from unittest import mock

import numpy as np

from physai.tests import dpa, tvla
import sca_schema as S


class FakeTtestResult:
    values = np.array([0.0, 12.0, 0.0])

    @property
    def statistic(self):
        return self.values


def minimal_spec():
    return {"algorithm": "aes-128-ecb",
            "analysis_inputs": {
                "tvla": {"fixed": "fixed", "random": "random"},
                "dpa": {"subset": "attack", "target": "round1-sbox-byte0-bit0"}}}


class StatisticalSemanticsTests(unittest.TestCase):
    def dpa_group(self):
        n = 16
        return {S.F_TRACE: np.zeros((n, 3), dtype=np.int16),
                S.F_KEY: np.zeros((n, 16), dtype=np.uint8),
                S.F_PLAINTEXT: np.arange(n * 16, dtype=np.uint8).reshape(n, 16)}

    def test_dpa_detection_is_fail_even_when_underpowered(self):
        FakeTtestResult.values = np.array([0.0, 12.0, 0.0])
        with mock.patch.object(dpa, "ttest_ind", return_value=FakeTtestResult()), \
             mock.patch.object(dpa.S, "load_group", return_value=self.dpa_group()), \
             mock.patch.object(dpa.S, "instruction_window_columns", return_value=None):
            result = dpa.run("unused", minimal_spec(), {"threshold": 5.0}, 1000, (0, 3))
        self.assertEqual(result["verdict"], "fail")
        self.assertEqual(result["statistical_power"], "underpowered")
        self.assertEqual(result["early_finding"], "detected")

    def test_dpa_underpowered_non_detection_is_inconclusive(self):
        FakeTtestResult.values = np.zeros(3)
        with mock.patch.object(dpa, "ttest_ind", return_value=FakeTtestResult()), \
             mock.patch.object(dpa.S, "load_group", return_value=self.dpa_group()), \
             mock.patch.object(dpa.S, "instruction_window_columns", return_value=None):
            result = dpa.run("unused", minimal_spec(), {"threshold": 5.0}, 1000, (0, 3))
        self.assertEqual(result["verdict"], "inconclusive")
        self.assertEqual(result["early_finding"], "not-detected-at-N")

    def test_tvla_is_independent_not_iso_verdict(self):
        FakeTtestResult.values = np.array([0.0, 10.0, 0.0])
        traces = {S.F_TRACE: np.zeros((8, 3), dtype=np.float64)}
        with mock.patch.object(tvla, "ttest_ind", return_value=FakeTtestResult()), \
             mock.patch.object(tvla.S, "group_len", return_value=8), \
             mock.patch.object(tvla.S, "load_group", return_value=traces):
            result = tvla.run("unused", minimal_spec(), {"threshold": 5.0}, 1000)
        self.assertEqual(result["early_finding"], "detected")
        self.assertEqual(result["preassessment_verdict"], "not-applicable")
        self.assertTrue(result["standard_verdict_role"].startswith("TVLA"))


if __name__ == "__main__":
    unittest.main()

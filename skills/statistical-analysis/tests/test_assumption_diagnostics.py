"""Regression checks for diagnostic decisions and non-interactive inspection."""

import contextlib
import io
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from assumption_checks import (  # noqa: E402
    check_homogeneity_of_variance,
    check_normality,
    check_normality_per_group,
    comprehensive_assumption_check,
)


class DiagnosticTests(unittest.TestCase):
    def test_non_rejection_is_a_test_decision(self):
        sample = stats.norm.ppf(np.linspace(0.02, 0.98, 40))
        result = check_normality(sample, plot=False)
        self.assertGreater(result["p_value"], 0.05)
        self.assertIs(result["normality_rejected"], False)
        self.assertNotIn("is_normal", result)

    def test_skewed_sample_reports_rejection(self):
        sample = np.exp(np.linspace(-3, 3, 40))
        result = check_normality(sample, plot=False)
        self.assertLess(result["p_value"], 0.05)
        self.assertIs(result["normality_rejected"], True)

    def test_uninformative_normality_inputs_are_undetermined(self):
        for sample in ([1.0, 2.0], [1.0] * 8, [1.0, 2.0, np.inf]):
            with self.subTest(sample=sample):
                result = check_normality(sample, plot=False)
                self.assertIsNone(result["normality_rejected"])
                self.assertTrue(np.isnan(result["p_value"]))

    def test_group_table_preserves_undetermined_results(self):
        frame = pd.DataFrame({"score": [1.0, 2.0, 5.0, 5.0, 5.0],
                              "group": ["A", "A", "B", "B", "B"]})
        result = check_normality_per_group(frame, "score", "group", plot=False)
        self.assertEqual(result["Normality decision"].tolist(),
                         ["Undetermined", "Undetermined"])

    def test_equal_variance_non_rejection_is_not_a_certificate(self):
        values = np.arange(10, dtype=float)
        frame = pd.DataFrame({"score": np.tile(values, 2),
                              "group": ["A"] * 10 + ["B"] * 10})
        result = check_homogeneity_of_variance(frame, "score", "group", plot=False)
        self.assertIs(result["equal_variance_rejected"], False)
        self.assertNotIn("is_homogeneous", result)

    def test_single_group_variance_comparison_is_undetermined(self):
        frame = pd.DataFrame({"score": np.arange(5, dtype=float), "group": "A"})
        result = check_homogeneity_of_variance(frame, "score", "group", plot=False)
        self.assertIsNone(result["equal_variance_rejected"])

    def test_headless_summary_does_not_certify_or_switch_analysis(self):
        sample = stats.norm.ppf(np.linspace(0.02, 0.98, 40))
        frame = pd.DataFrame({"score": np.tile(sample, 2),
                              "group": ["A"] * 40 + ["B"] * 40})
        original = frame.copy(deep=True)
        output = io.StringIO()
        with patch("assumption_checks.plt.subplots") as subplots:
            with contextlib.redirect_stdout(output):
                result = comprehensive_assumption_check(
                    frame, "score", "group", plot=False)
            subplots.assert_not_called()
        pd.testing.assert_frame_equal(frame, original)
        self.assertIn("normality_per_group", result)
        self.assertNotRegex(output.getvalue(),
                            r"All assumptions met|Normality assumption met|"
                            r"Normality violated\. Use non-parametric")


if __name__ == "__main__":
    unittest.main()

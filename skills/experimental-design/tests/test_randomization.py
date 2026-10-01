"""Regression checks for unit identity, completed blocks, and invalid layouts."""

from pathlib import Path
import subprocess
import sys
import unittest

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
from randomization import (  # noqa: E402
    block_randomization,
    stratified_block_randomization,
)


class RandomizationTests(unittest.TestCase):
    def test_interleaved_strata_stay_attached_to_original_units(self):
        strata = ["batch_A", "batch_B"] * 8
        layout = stratified_block_randomization(
            strata, arms=["A", "B"], block_size=4, seed=20261001)
        self.assertEqual(layout.unit_id.tolist(), list(range(1, 17)))
        self.assertEqual(layout.stratum.tolist(), strata)
        for _, block in layout.groupby(["stratum", "block"]):
            self.assertEqual(block.arm.value_counts().to_dict(), {"A": 2, "B": 2})

    def test_counts_dictionary_retains_global_unique_units(self):
        layout = stratified_block_randomization(
            {"batch_A": 8, "batch_B": 4}, block_size=4, seed=5)
        self.assertEqual(layout.unit_id.tolist(), list(range(1, 13)))
        self.assertEqual(layout.stratum.value_counts().to_dict(),
                         {"batch_A": 8, "batch_B": 4})

    def test_incomplete_tail_is_retained_after_balanced_complete_block(self):
        layout = block_randomization(5, arms=["A", "B"], block_size=4, seed=5)
        self.assertEqual(layout.unit_id.tolist(), list(range(1, 6)))
        self.assertEqual(layout.groupby("block").size().tolist(), [4, 1])
        self.assertEqual(layout[layout.block == 0].arm.value_counts().to_dict(),
                         {"A": 2, "B": 2})

    def test_seed_reproduces_allocation(self):
        arguments = {"strata": ["A", "B"] * 8, "block_size": 4, "seed": 5}
        pd.testing.assert_frame_equal(
            stratified_block_randomization(**arguments),
            stratified_block_randomization(**arguments))

    def test_missing_stratum_cannot_silently_drop_a_unit(self):
        with self.assertRaisesRegex(ValueError, "missing"):
            stratified_block_randomization(["A", None, "B"])

    def test_zero_block_size_fails_without_hanging(self):
        # Keep the regression bounded if the old infinite loop reappears.
        code = (
            f"import sys; sys.path.insert(0, {str(SCRIPT_DIR)!r})\n"
            "from randomization import block_randomization\n"
            "try:\n"
            "    block_randomization(4, block_size=0)\n"
            "except ValueError:\n"
            "    pass\n"
            "else:\n"
            "    raise AssertionError('zero block size was accepted')\n"
        )
        result = subprocess.run([sys.executable, "-c", code], capture_output=True,
                                text=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()

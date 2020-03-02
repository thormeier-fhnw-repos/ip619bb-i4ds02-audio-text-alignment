import unittest
from typing import List, Tuple
from lib.src.align.sequence_alignment.semi_global import semi_global


class TestSmithWaterman(unittest.TestCase):
    """
    Test the Semi-Global alignment implementation.
    """

    def compare(self, a, b) -> bool:
        """
        Basic compare function.
        :param a: Element of sequence A
        :param b: Element of sequence B
        :return: True if match
        """
        return a == b

    def assert_result(self, a: List, b: List, expected: Tuple[List, List, int]) -> None:
        """
        Convenience method
        :param a:        List of elements to align a
        :param b:        List of elements to align b
        :param expected: Expected alignment
        :return: None
        """
        self.assertEqual(expected, semi_global(a, b, 2, -1, -1, self.compare))

    def test_align(self) -> None:
        """
        Test alignment of example used in slides about Semi-Global alignment
        :return: None
        """
        self.assert_result(
            ["A", "T", "C", "C", "G", "A", "A", "C", "A", "T", "C", "C", "A", "A", "T", "C", "G", "A", "A", "G", "C"],
            ["A", "G", "C", "A", "T", "G", "C", "A", "A", "T"],
            (["A",  "T",  "C",  "C",  "G",  "A", "A", "C", "A", "T", "C", "C", "A", "A", "T",  "C",  "G",  "A",  "A",  "G",  "C"], [None, None, None, None, None, "A", "G", "C", "A", "T", "G", "C", "A", "A", "T", None, None, None, None, None, None], 8.0)
        )

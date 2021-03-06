import unittest
from typing import List, Tuple
from lib.src.align.sequence_alignment.smith_waterman import smith_waterman


class TestSmithWaterman(unittest.TestCase):
    """
    Test the Smith-Waterman implementation.
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
        self.assertEqual(expected, smith_waterman(a, b, 2, -1, -1, self.compare))

    def test_align(self) -> None:
        """
        Test alignment of example used in slides about Smith-Waterman
        :return: None
        """
        self.assert_result(
            ["C", "T", "C", "A", "T", "G", "C"],
            ["A", "C", "A", "A", "T", "C", "G"],
            (["C", None, "A", "T", "G", "C"], ["C", "A", "A", "T", None, "C"], 6.0)
        )

    def test_perfect_align(self) -> None:
        """
        Test alignment of perfectly matching sequences
        :return: None
        """
        self.assert_result(
            ["F", "O", "O", "B", "A", "R"],
            ["F", "O", "O", "B", "A", "R"],
            (["F", "O", "O", "B", "A", "R"], ["F", "O", "O", "B", "A", "R"], 12.0)
        )

    def test_empty_alignment(self) -> None:
        """
        Test empty alignment for completely different sequences
        :return: None
        """
        self.assert_result(
            ["F", "O", "O"],
            ["B", "A", "R"],
            ([], [], 0.0)
        )
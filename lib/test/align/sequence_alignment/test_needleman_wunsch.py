import unittest
from typing import List, Tuple
from unittest_data_provider import data_provider
from lib.src.align.sequence_alignment.needleman_wunsch import needleman_wunsch


class TestNeedlemanWunsch(unittest.TestCase):
    """
    Tests the implementation of the Needleman-Wunsch algorithm
    """

    def compare(self, a, b) -> bool:
        """
        Basic compare function.
        :param a: Element of sequence A
        :param b: Element of sequence B
        :return: True if match
        """
        return a == b

    needleman_wunsch_data_provider = lambda: (
        ([1, 2, 3], [1, 2, 3], ([1, 2, 3], [1, 2, 3], 15)),  # Test same
        ([1, 2, 3, 4], [1, 2, 4], ([1, 2, 3, 4], [1, 2, None, 4], 5.0)),  # Test alignment if a gap has to be introduced.
        ([1, 2, 4], [1, 2, 3, 4], ([1, 2, None, 4], [1, 2, 3, 4], 5.0)),  # Test alignment if a gap has to be introduced.
        ([3, 4, 5], [2, 3, 4, 5], ([None, 3, 4, 5], [2, 3, 4, 5], 5.0)),  # Test alignment if a gap has to be introduced.
        ([3, 4, 5], [1, 2, 3, 4, 5], ([None, None, 3, 4, 5], [1, 2, 3, 4, 5], -5.0)),  # Tests if a gap is introduced at the beginning.
        ([1, 2, 3], [1, 2, 3, 4], ([1, 2, 3, None], [1, 2, 3, 4], 5.0)),  # Test if a gap is introduced at the end
        ([1, 2, 3], [1, 2, 3, 4, 5], ([1, 2, 3, None, None], [1, 2, 3, 4, 5], -5.0)),  # Test if a gap is introduced at the end
        ([2, 3], [1, 2, 3, 4], ([None, 2, 3, None], [1, 2, 3, 4], -10.0)),  # Test if a gap is introduced at the start and end
        ([3], [1, 2, 3, 4, 5], ([None, None, 3, None, None], [1, 2, 3, 4, 5], -35.0)),  # Test if a gap is introduced at the start and end
        ([2, 4], [1, 2, 3, 4, 5], ([None, 2, None, 4, None], [1, 2, 3, 4, 5], -20.0)),  # Test if a gap is introduced at the start, end and in between
        (["F", "R", "I", "E", "D"], ["F", "R", "E", "S", "H"], (["F", "R", "I", "E", None, "D"], ["F", "R", None, "E", "S", "H"], -20.0)),  # Test alignment example from paper.
    )

    @data_provider(needleman_wunsch_data_provider)
    def test_needleman_wunsch(self, a: List, b: List, expected: Tuple[List, List, int]) -> None:
        """
        Convenience method
        :param a:        List of elements to align a
        :param b:        List of elements to align b
        :param expected: Expected Alignment
        :return: None
        """
        self.assertEqual(expected, needleman_wunsch(a, b, 5, -15, -10, self.compare))

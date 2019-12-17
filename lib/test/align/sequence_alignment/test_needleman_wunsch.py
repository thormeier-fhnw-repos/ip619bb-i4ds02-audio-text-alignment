import unittest
from typing import List, Tuple
from lib.src.align.sequence_alignment.needleman_wunsch import needleman_wunsch


class TestNeedlemanWunsch(unittest.TestCase):
    """
    Tests the implementation of the Needleman-Wunsch algorithm
    """

    def compare(self, a, b):
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
        :param a: List of elements to align a
        :param b: List of elements to align b
        :param expected:
        :return: Tuple
        """
        self.assertEqual(expected, needleman_wunsch(a, b, 5, -15, -10, self.compare))

    def test_same(self) -> None:
        """
        Test perfect alignment if both lists are same
        :return: None
        """
        self.assert_result(
            [1, 2, 3],
            [1, 2, 3],
            ([1, 2, 3], [1, 2, 3], 15)
        )

    def test_gap_left(self) -> None:
        """
        Test alignment if a gap has to be introduced.
        :return:
        """
        self.assert_result(
            [1, 2, 3, 4],
            [1, 2, 4],
            ([1, 2, 3, 4], [1, 2, None, 4], 5.0)
        )

    def test_gap_up(self) -> None:
        """
        Test alignment if a gap has to be introduced.
        :return:
        """
        self.assert_result(
            [1, 2, 4],
            [1, 2, 3, 4],
            ([1, 2, None, 4], [1, 2, 3, 4], 5.0)
        )

    def test_gap_start(self) -> None:
        """
        Tests if a gap is introduced at the beginning
        :return:
        """
        self.assert_result(
            [3, 4, 5],
            [2, 3, 4, 5],
            ([None, 3, 4, 5], [2, 3, 4, 5], 5.0)
        )

        self.assert_result(
            [3, 4, 5],
            [1, 2, 3, 4, 5],
            ([None, None, 3, 4, 5], [1, 2, 3, 4, 5], -5.0)
        )

    def test_gap_end(self) -> None:
        """
        Test if a gap is introduced at the end
        :return:
        """
        self.assert_result(
            [1, 2, 3],
            [1, 2, 3, 4],
            ([1, 2, 3, None], [1, 2, 3, 4], 5.0)
        )

        self.assert_result(
            [1, 2, 3],
            [1, 2, 3, 4, 5],
            ([1, 2, 3, None, None], [1, 2, 3, 4, 5], -5.0)
        )

    def test_gap_start_and_end(self) -> None:
        """
        Test if a gap is introduced at the start and end
        :return:
        """
        self.assert_result(
            [2, 3],
            [1, 2, 3, 4],
            ([None, 2, 3, None], [1, 2, 3, 4], -10.0)
        )

        self.assert_result(
            [3],
            [1, 2, 3, 4, 5],
            ([None, None, 3, None, None], [1, 2, 3, 4, 5], -35.0)
        )

    def test_gap_start_and_end_and_between(self) -> None:
        """
        Test if a gap is introduced at the start, end and in between
        :return:
        """
        self.assert_result(
            [2, 4],
            [1, 2, 3, 4, 5],
            ([None, 2, None, 4, None], [1, 2, 3, 4, 5], -20.0)
        )

    def test_align_example(self):
        """
        Test alignment example from paper.
        :return: None
        """
        self.assert_result(
            ['F', 'R', 'I', 'E', 'D'],
            ['F', 'R', 'E', 'S', 'H'],
            (['F', 'R', 'I', 'E', None, 'D'], ['F', 'R', None, 'E', 'S', 'H'], -20.0)
        )

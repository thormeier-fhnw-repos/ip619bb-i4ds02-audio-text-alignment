import unittest
from typing import List, Tuple
from lib.src.align.sequence_alignment.semi_global import semi_global


class TestSmithWaterman(unittest.TestCase):
    """
    Test the Semi-Global alignment implementation.
    """

    def assert_result(self, a: List, b: List, expected: List[Tuple[List, List, int]]) -> None:
        """
        Convenience method
        :param a: List of elements to align a
        :param b: List of elements to align b
        :param expected:
        :return: Tuple
        """
        self.assertEqual(expected, semi_global(a, b, 2, -1, -1))

    def test_align(self):
        """
        Test alignment of example used in slides about Semi-Global alignment
        :return:
        """
        self.assert_result(
            ['A', 'T', 'C', 'C', 'G', 'A', 'A', 'C', 'A', 'T', 'C', 'C', 'A', 'A', 'T', 'C', 'G', 'A', 'A', 'G', 'C'],
            ['A', 'G', 'C', 'A', 'T', 'G', 'C', 'A', 'A', 'T'],
            [
                (['C', None, 'A', 'T', None, 'G'], ['C', 'A', 'A', 'T', 'C', 'G'], 6.0),
                (['C', None, 'A', 'T', 'G', 'C'], ['C', 'A', 'A', 'T', None, 'C'], 6.0)
            ]
        )

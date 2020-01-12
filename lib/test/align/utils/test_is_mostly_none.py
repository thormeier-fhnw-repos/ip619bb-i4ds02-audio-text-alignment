import unittest
from lib.src.align.utils.is_mostly_none import is_mostly_none
from unittest_data_provider import data_provider
from typing import List


class TestIsMostlyNone(unittest.TestCase):
    """
    Tests lib.src.align.utils.is_mostly_none
    """

    is_mostly_none_data_provider = lambda: (
        (list('-'), True),
        (list('a'), False),
        (list('a-'), False),
        (list('a--'), False),
        (list('a---'), False),
        (list('a----'), False),
        (list('a-----'), True),
        ([], True),
    )

    @data_provider(is_mostly_none_data_provider)
    def test_is_mostly_none(self, input_data: List, expected_result: bool) -> None:
        """
        Tests is_mostly_none function's behaviour
        :param input_data:      Input list
        :param expected_result: Expected result
        :return: None
        """
        self.assertEqual(expected_result, is_mostly_none(input_data))



if __name__ == '__main__':
    unittest.main()

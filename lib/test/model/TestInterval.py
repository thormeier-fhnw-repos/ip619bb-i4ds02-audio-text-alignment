import unittest
from typing import Any
from unittest_data_provider import data_provider
from lib.src.model.Interval import Interval


class TestInterval(unittest.TestCase):
    """
    Test class lib.src.model.Interval
    """

    intersection_data_provider = lambda: (
        (0.0, 0.0, 0.0, 0.0, 0.0),  # Sanity check
        (0.0, 1.0, 0.0, 1.0, 1.0),  # Full overlap
        (0.0, 1.0, 0.5, 1.5, 0.5),  # Partial overlap
        ("-", 1.0, 0.0, 1.0, 0.0),  # Character present, therefore no overlap
        (0.0, "-", 0.0, 1.0, 0.0),  # Character present, therefore no overlap
        ("-", "-", 0.0, 1.0, 0.0),  # Character present, therefore no overlap
        (None, 1.0, 0.0, 1.0, 0.0),  # None present, therefore no overlap
        (0.0, None, 0.0, 1.0, 0.0),  # None present, therefore no overlap
        (None, None, 0.0, 1.0, 0.0),  # None present, therefore no overlap
        (0.0, 1.0, 2.0, 3.0, 0.0),  # No overlap
    )

    @data_provider(intersection_data_provider)
    def test_get_intersection(self, start: Any, end: Any, other_start: Any, other_end: Any,
                              expected_intersection: float) -> None:
        """
        Tests the get_intersection method's behaviour
        :param start:                 Start of interval a
        :param end:                   End of interval a
        :param other_start:           Start of interval b
        :param other_end:             End of interval b
        :param expected_intersection: Value to check against
        :return: None
        """
        a = Interval(start, end)
        b = Interval(other_start, other_end)

        self.assertEqual(a.get_intersection(b), expected_intersection)

    union_data_provider = lambda: (
        (0.0, 0.0, 0.0, 0.0, 0.0),  # Sanity check
        (0.0, 1.0, 0.0, 1.0, 1.0),  # Full overlap, same union
        (0.0, 1.0, 0.5, 1.5, 1.5),  # Partial overlap
        ("-", 1.0, 0.0, 1.0, 0.0),  # Character present, therefore no overlap
        (0.0, "-", 0.0, 1.0, 0.0),  # Character present, therefore no overlap
        ("-", "-", 0.0, 1.0, 0.0),  # Character present, therefore no overlap
        (None, 1.0, 0.0, 1.0, 0.0),  # None present, therefore no overlap
        (0.0, None, 0.0, 1.0, 0.0),  # None present, therefore no overlap
        (None, None, 0.0, 1.0, 0.0),  # None present, therefore no overlap
        (0.0, 1.0, 2.0, 3.0, 3.0),  # No overlap
    )

    @data_provider(union_data_provider)
    def test_get_union(self, start: Any, end: Any, other_start: Any, other_end: Any,
                       expected_union: float) -> None:
        """
        Tests the get_union method's behaviour
        :param start:          Start of interval a
        :param end:            End of interval a
        :param other_start:    Start of interval b
        :param other_end:      End of interval b
        :param expected_union: Value to check against
        :return: None
        """
        a = Interval(start, end)
        b = Interval(other_start, other_end)
        self.assertEqual(a.get_union(b), expected_union)

    length_data_provider = lambda: (
        (0.0, 0.0, 0.0),  # Sanity check
        ("-", 0.0, 0.0),  # Character present, no length
        (0.0, "-", 0.0),  # Character present, no length
        ("-", "-", 0.0),  # Character present, no length
        (None, 0.0, 0.0),  # None present, no length
        (0.0, None, 0.0),  # None present, no length
        (None, None, 0.0),  # None present, no length
        (0.0, 1.0, 1.0),  # Valid length calculation
    )

    @data_provider(length_data_provider)
    def test_get_length(self, start: Any, end: Any, expected_length: float) -> None:
        """
        Tests get_length method's behaviour
        :param start:           Start of the interval
        :param end:             End of the interval
        :param expected_length: Expected calculated length
        :return: None
        """
        a = Interval(start, end)
        self.assertEqual(a.get_length(), expected_length)

    formatted_data_provider = lambda: (
        (0.0, 0.0, "0.000000000000000\t0.000000000000000"),  # Sanity check
        (0.0, 0.123456789, "0.000000000000000\t0.123456789000000"),  # Places after comma
        (0.0, 0.12345678901234567890, "0.000000000000000\t0.123456789012346"),  # Lengthy places after comma with rounding
        (0.0, 1000.0, "0.000000000000000\t1000.000000000000000"),  # Lengthy integer value
        ("-", 0.0, "-\t0.000000000000000"),  # One of them is character
        (0.0, "-", "0.000000000000000\t-"),  # The other one is character
        ("-", "-", "-\t-"),  # Both are characters
        (None, 0.0, "None\t0.000000000000000"),  # One of them is None
        (0.0, None, "0.000000000000000\tNone"),  # The other one is None
        (None, None, "None\tNone"),  # Both are None
    )

    @data_provider(formatted_data_provider)
    def test_to_formatted(self, start: Any, end: Any, expected_formatted: str) -> None:
        """
        Tests to_formatted method's behaviour.
        :param start:              Start of the interval
        :param end:                End of the interval
        :param expected_formatted: Expected formatted output
        :return: None
        """
        a = Interval(start, end)
        self.assertEqual(a.to_formatted(), expected_formatted)


if __name__ == '__main__':
    unittest.main()

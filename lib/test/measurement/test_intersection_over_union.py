import unittest
from typing import Any
from lib.src.model.Interval import Interval
from unittest_data_provider import data_provider
from lib.src.measurement.intersection_over_union import intersection_over_union


class IntervalMock(Interval):
    """
    Mocks the Interval class
    """

    def __init__(self, intersection_value: Any, union_value: Any):
        super().__init__(0.0, 0.1)
        self.intersection_value = intersection_value
        self.union_value = union_value

    def get_intersection(self, other: Interval) -> float:
        """
        Mocks get_intersection
        :param other: Other interval, ignored
        :return: Predefined value
        """
        return self.intersection_value

    def get_union(self, other: Interval):
        """
        Mocks get_union
        :param other: Other interval, ignored
        :return: Predefined value
        """
        return self.union_value


class TestIntersectionOverUnion(unittest.TestCase):
    """
    Tests lib.src.measurement.intersection_over_union
    """

    intersection_over_union_data_provider = lambda: (
        (IntervalMock(1.0, 1.0), Interval(0.0, 0.0), 1.0),  # Sanity check
        (IntervalMock(3.0, 6.0), Interval(0.0, 0.0), 0.5),  # Sanity check
        (IntervalMock(1.0, 0.0), Interval(0.0, 0.0), 0.0),  # Shouldn't do a division by 0
        (IntervalMock(0.0, 1.0), Interval(0.0, 0.0), 0.0),  # One 0 should yield value 0
    )

    @data_provider(intersection_over_union_data_provider)
    def test_intersection_over_union(self, a: IntervalMock, b: IntervalMock, expected_value: float) -> None:
        """
        Tests intersection_over_union function.
        :param a:
        :param b:
        :param expected_value:
        :return:
        """
        self.assertEqual(intersection_over_union(a, b), expected_value)


if __name__ == "__main__":
    unittest.main()

import unittest

from src.measurement.intersection_over_union import intersection_over_union


class IntervalMock:
    def __init__(self, intersection_result, union_result):
        """
        Interval mock to return predetermined results
        :param intersection_result: Float
        :param union_result: Float
        """
        self.intersection_result = intersection_result
        self.union_result = union_result

    def get_union(self, ignored):
        """
        Union mock
        :param ignored: Any
        :return: Predetermined value
        """
        return self.union_result

    def get_intersection(self, ignored):
        """
        Intersection mock
        :param ignored: any
        :return: Predetermined value
        """
        return self.intersection_result


class TestIntersectionOverUnion(unittest.TestCase):
    """
    Tests the src.model.intersection_over_union function
    """
    def test_intersection_over_union_normal(self):
        a = IntervalMock(1, 2)
        b = IntervalMock(None, None) # No results necessary

        self.assertEqual(0.5, intersection_over_union(a, b))

    """
    Tests the src.model.intersection_over_union function
    """
    def test_intersection_over_union_nonsense(self):
        a = IntervalMock(None, None)
        b = IntervalMock(None, None)

        self.assertEqual(0, intersection_over_union(a, b))

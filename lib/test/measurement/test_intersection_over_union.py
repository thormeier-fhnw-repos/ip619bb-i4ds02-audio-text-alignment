import unittest

from lib.src.measurement.intersection_over_union import intersection_over_union


class IntervalMock:
    """
    Mocks an interval to return predefined values.
    """

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
    def test_intersection_over_union_normal(self):
        """
        Tests the src.model.intersection_over_union function
        """
        a = IntervalMock(1, 2)
        b = IntervalMock(None, None) # No results necessary

        self.assertEqual(0.5, intersection_over_union(a, b))

    def test_intersection_over_union_nonsense(self):
        """
        Tests the src.model.intersection_over_union function
        """
        a = IntervalMock(None, None)
        b = IntervalMock(None, None)

        self.assertEqual(0, intersection_over_union(a, b))


if __name__ == '__main__':
    unittest.main()

import unittest
from lib.src.model.Interval import Interval


class TestInterval(unittest.TestCase):
    """
    Tests the src.model.Interval class
    """

    def test_get_intersection_nonsense(self):
        """
        Non-Interval params should raise an AttributeError.
        """
        a = Interval(3, 3)
        with self.assertRaises(AttributeError):
            a.get_intersection(None)
        with self.assertRaises(AttributeError):
            a.get_intersection(False)
        with self.assertRaises(AttributeError):
            a.get_intersection(12)

    def test_get_intersection_same(self):
        """
        Equal intervals should overlap fully, hence
        overlapping area should equal interval area.
        """
        x = 1
        y = 3
        a = Interval(x, y)
        b = Interval(x, y)

        self.assertEqual(y - x, a.get_intersection(b))
        self.assertEqual(y - x, b.get_intersection(a))

    def test_get_intersection_none(self):
        """
        Intervals far apart should yield 0 overlaping area.
        """
        a = Interval(1, 2)
        b = Interval(4, 5)

        self.assertEqual(0, a.get_intersection(b))
        self.assertEqual(0, b.get_intersection(a))

    def test_get_intersection_partial(self):
        """
        Partially overlapping intervals should
        only return the actual overlapping area.
        """
        a = Interval(1, 3)
        b = Interval(2, 4)

        self.assertEqual(1, a.get_intersection(b))
        self.assertEqual(1, b.get_intersection(a))

    def test_get_union_nonsense(self):
        """
        Non-Interval params should raise an AttributeError.
        """
        a = Interval(3, 3)
        with self.assertRaises(AttributeError):
            a.get_union(None)
        with self.assertRaises(AttributeError):
            a.get_union(False)
        with self.assertRaises(AttributeError):
            a.get_union(12)

    def test_get_union_same(self):
        """
        Same intervals shouldn't have more area in union as one.
        """
        x = 1
        y = 3
        a = Interval(x, y)
        b = Interval(x, y)

        self.assertEqual(y - x, a.get_union(b))
        self.assertEqual(y - x, b.get_union(a))

    def test_get_union_no_overlap(self):
        """
        Non-overlapping intervals should add up.
        """
        a = Interval(1, 2)
        b = Interval(4, 5)

        self.assertEqual(4, a.get_union(b))
        self.assertEqual(4, b.get_union(a))

    def test_get_union_partial(self):
        """
        Partially overlapping intervals should
        only return the actual overlapping area.
        """
        a = Interval(1, 3)
        b = Interval(2, 4)

        self.assertEqual(3, a.get_union(b))
        self.assertEqual(3, b.get_union(a))


if __name__ == '__main__':
    unittest.main()

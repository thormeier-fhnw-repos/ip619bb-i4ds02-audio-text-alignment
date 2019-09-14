class Interval:
    def __init__(self, start, end):
        """
        Defines an interval with start and end.
        :param start: Float
        :param end: Float
        """
        self.start = start
        self.end = end

    def get_intersection(self, other):
        """
        Returns the relative intersection area of this pair with another.
        :param other: Pair
        :return: Float
        """
        start = self.start if self.start >= other.start else other.start
        end = self.end if self.end <= other.end else other.end

        area = end - start

        return end - start if area >= 0 else 0

    def get_union(self, other):
        """
        Returns the total area of this pair with another.
        :param other: Pair
        :return: Float
        """
        start = self.start if self.start <= other.start else other.start
        end = self.end if self.end >= other.end else other.end

        return end - start

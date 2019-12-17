class Interval:
    def __init__(self, start: float, end: float):
        """
        Defines an interval with start and end.
        :param start: float
        :param end: float
        """
        self.start = start
        self.end = end

    def get_intersection(self, other: 'Interval') -> float:
        """
        Returns the relative intersection area of this pair with another.
        :param other: Interval
        :return: float
        """
        start = self.start if self.start >= other.start else other.start
        end = self.end if self.end <= other.end else other.end

        area = end - start

        return end - start if area >= 0 else 0

    def get_union(self, other: 'Interval') -> float:
        """
        Returns the total area of this pair with another.
        :param other: Interval
        :return: float
        """
        start = self.start if self.start <= other.start else other.start
        end = self.end if self.end >= other.end else other.end

        return end - start

    def get_length(self) -> float:
        """
        Calculates the length of a this interval
        :return:
        """
        return self.end - self.start
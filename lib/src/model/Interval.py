from typing import Any


class Interval:
    def __init__(self, start: Any, end: Any):
        """
        Defines an interval with start and end.
        :param start: float or character
        :param end: float or character
        """
        self.start = start
        self.end = end

    def get_intersection(self, other: 'Interval') -> float:
        """
        Returns the relative intersection area of this pair with another.
        :param other: Interval
        :return: float
        """
        if not isinstance(self.start, float) \
                or not isinstance(self.end, float) \
                or not isinstance(other.start, float) \
                or not isinstance(other.end, float):
            return 0.0

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
        if not isinstance(self.start, float) \
                or not isinstance(self.end, float) \
                or not isinstance(other.start, float) \
                or not isinstance(other.end, float):
            return 0.0

        start = self.start if self.start <= other.start else other.start
        end = self.end if self.end >= other.end else other.end

        return end - start

    def get_length(self) -> float:
        """
        Calculates the length of a this interval
        :return: Length, or near-0 or 0 if not appearing at all
        """
        if isinstance(self.start, float) and isinstance(self.end, float):
            return self.end - self.start

        return 0.0

    def to_formatted(self) -> str:
        """
        Formats this interval to later fit into audacity label format
        :return: Formatted version
        """
        start = self.start
        end = self.end

        if isinstance(self.start, float):
            start = "%.15f" % (self.start if self.start is not None else 0.0)

        if isinstance(self.end, float):
            end = "%.15f" % (self.end if self.end is not None else 0.0)

        return str(start) + "\t" + str(end)

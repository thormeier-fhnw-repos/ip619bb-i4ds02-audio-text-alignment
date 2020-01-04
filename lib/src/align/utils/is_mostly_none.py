from typing import List


def is_mostly_none(l: List) -> bool:
    """
    Determines if a a given list consists of mostly gaps.
    :param l: List of aligned words
    :return: True if threshold is reached
    """
    return len(l) == 0 or (l.count("-")) / len(l) > 0.8

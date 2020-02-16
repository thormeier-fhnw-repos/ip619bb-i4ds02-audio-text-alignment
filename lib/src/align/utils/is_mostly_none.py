from typing import List
from lib.src.align.utils.get_none_part import get_none_part


def is_mostly_none(l: List) -> bool:
    """
    Determines if a a given list consists of mostly gaps.
    :param l: List of aligned words
    :return: True if threshold is reached
    """
    return len(l) == 0 or get_none_part(l) > 0.8

from typing import List


def get_none_part(l: List) -> float:
    """
    Calculates the amount of gaps relative to the sentence length

    :param l: Sentence or sentence part

    :return: Percentage of gaps
    """
    return (l.count("-")) / len(l)

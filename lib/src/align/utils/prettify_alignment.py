from typing import List


def prettify_alignment(a: List, b: List) -> str:
    """
    Makes two alignments prettier to print next to each other
    :param a: Alignment (Google side)
    :param b: Alignment (Transcript side)
    :return: Prettified alignment
    """
    a = ['-' if el is None else el for el in a]
    b = ['-' if el is None else el for el in b]

    combined = [e[0].ljust(30) + e[1] for e in zip(a, b)]

    return "\n" + ("\n".join(combined))

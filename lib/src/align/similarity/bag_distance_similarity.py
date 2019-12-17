from collections import Counter


def bag_distance_similarity(a: str, b: str) -> float:
    """
    Calculates the bag distance of two given strings as approximation of
    :param a: Word
    :param b: Word
    :return: Percentage of similarity estimate
    """
    ca = Counter(a)
    cb = Counter(b)

    max_len = max(len(a), len(b))
    bag_distance = max(
        len(list((ca - cb).elements())),
        len(list((cb - ca).elements()))
    )

    return 1 - (bag_distance / max_len)

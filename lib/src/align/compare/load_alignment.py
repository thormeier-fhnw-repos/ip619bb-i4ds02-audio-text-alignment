from lib.src.model.Sentence import sentence_from_string, Sentence
from typing import List


def load_alignment(path: str) -> List[Sentence]:
    """
    Loads all sentences from a file

    :param path: Path to alignment

    :return: List of sentences from the given file
    """
    with open(path, "r+", encoding="utf-8") as f:
        sentences = f.readlines()

    return [sentence_from_string(s) for s in sentences if len(s) > 0]

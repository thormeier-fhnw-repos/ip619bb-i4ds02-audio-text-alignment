from lib.src.model.Sentence import sentence_from_string, Sentence
from typing import List


def load_alignment(path: str) -> List[Sentence]:
    """
    Loads all sentences from a file
    :param path:
    :return: list[Sentence]
    """
    sentences = []
    with open(path) as f:
        sentences = f.readlines()

    return [sentence_from_string(s) for s in sentences if len(s) > 0]

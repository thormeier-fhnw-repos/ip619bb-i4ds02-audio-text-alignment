from nltk.tokenize import sent_tokenize
from lib.src.model.Sentence import Sentence
from lib.src.model.Interval import Interval
from typing import List


def transcricpt_to_sentences(transcript: str) -> List[Sentence]:
    """
    Creates a list of Sentence instances with empty intervals from a given text.
    :param transcript: String
    :return: List of Sentence instances
    """
    return [Sentence(sentence, Interval(None, None)) for sentence in sent_tokenize(transcript, 'german')]

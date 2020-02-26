import abc
from typing import List
from lib.src.model.Sentence import Sentence


class AbstractAlignerStrategy(abc.ABC):
    """
    Abstract base class to allow typehinting.
    """

    """
    List of execution times per sentence
    """
    execution_times = []

    """
    List of alingment time consumption
    """
    alignment_times = []

    @staticmethod
    @abc.abstractmethod
    def perform_alignment(transcript: str, wav_path: str, verbosity: int) -> List[Sentence]:
        """
        Aligns a given transcript to a given wav
        :param transcript: Transcript as string
        :param wav_path:   Path to given wav file
        :param verbosity:  Verbosity of output
        :return: List of aligned sentences
        """""
        pass

    @classmethod
    def align(cls, transcript: str, wav_path: str, verbosity: int) -> List[Sentence]:
        """
        Calls inner implementation of perform_alignment. Allows for specific overrideable
        default behaviour of different kinds of aligners.
        :param transcript: Transcript as string
        :param wav_path:   Path to given wav file
        :param verbosity:  Verbosity of output
        :return:
        """
        return cls.perform_alignment(transcript, wav_path, verbosity)


from lib.src.align.aligner.google.AbstractGoogleAlignerStrategy import AbstractGoogleAlignerStrategy
from typing import Dict, Any


class GoogleSemiglobalWordAlignerStrategy(AbstractGoogleAlignerStrategy):
    """
    Semi-global alignment, word based
    """

    @staticmethod
    def perform_alignment(transcript: str, google_output: object, verbosity: int,
                          alignment_parameters: Dict[str, Any]) -> Dict[str, Any]:

        # TODO: Add alignment

        return {
            "google": "",
            "transcript": "",
            "score": 0.0  # TODO: Get actual score
        }
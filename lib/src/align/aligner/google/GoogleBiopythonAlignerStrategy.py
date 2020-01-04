from lib.src.align.aligner.google.AbstractGoogleAlignerStrategy import AbstractGoogleAlignerStrategy
from typing import Dict, Any
from Bio import pairwise2


class GoogleBiopythonAlignerStrategy(AbstractGoogleAlignerStrategy):
    """
    Alignment with biopythons pairwise2
    """

    @staticmethod
    def perform_alignment(transcript: str, google_output: object, verbosity: int,
                          alignment_parameters: Dict[str, Any]) -> Dict[str, Any]:
        alignments = pairwise2.align.localms(
            google_output,
            transcript,
            alignment_parameters["algorithm"]["match_reward"],
            alignment_parameters["algorithm"]["mismatch_penalty"],
            alignment_parameters["algorithm"]["gap_penalty"],
            alignment_parameters["algorithm"]["gap_penalty"],
            penalize_end_gaps=(True, True),
            one_alignment_only=True,
        )

        alignment = alignments[0]

        return {
            "google": alignment[0],
            "transcript": alignment[1],
            "score": 0.0 # TODO: Get actual score
        }

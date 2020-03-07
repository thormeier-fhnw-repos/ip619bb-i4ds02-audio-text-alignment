from lib.src.align.aligner.google.AbstractGoogleAlignerStrategy import AbstractGoogleAlignerStrategy
from typing import Dict, Any
import Bio


class GoogleBiopythonAlignerStrategy(AbstractGoogleAlignerStrategy):
    """
    Alignment with biopythons pairwise2
    """

    @staticmethod
    def perform_alignment(transcript: str, google_output: object, verbosity: int,
                          alignment_parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Performs an alignment via Biopython's pairwise2

        :param transcript:           Transcript as string
        :param google_output:        Google STT output
        :param verbosity:            Verbosity level
        :param alignment_parameters: Config

        :return: Alignments + score
        """
        alignments = Bio.pairwise2.align.localms(
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
            "score": alignment[2]
        }

from lib.src.align.aligner.google.AbstractGoogleAlignerStrategy import AbstractGoogleAlignerStrategy
from lib.src.align.sequence_alignment.needleman_wunsch import needleman_wunsch
from typing import Dict, Any


class GoogleGlobalCharacterAlignerStrategy(AbstractGoogleAlignerStrategy):
    """
    Global alignment, character based
    """

    @staticmethod
    def perform_alignment(transcript: str, google_output: str, verbosity: int,
                          alignment_parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform the alignment

        :param transcript:           Transcript
        :param google_output:        Googles output as string
        :param verbosity:            Verbosity level
        :param alignment_parameters: Config

        :return: Alignments + score
        """
        def compare(a: str, b: str) -> bool:
            """
            Checks if two characters are equal

            :param a: String to compare
            :param b: String to compare

            :return: Equality of stringsperform_alignment
            """
            return a == b

        alignment = needleman_wunsch(
            list(google_output),
            list(transcript),
            alignment_parameters["algorithm"]["match_reward"],
            alignment_parameters["algorithm"]["mismatch_penalty"],
            alignment_parameters["algorithm"]["gap_penalty"],
            compare
        )

        return {
            "google": "".join([c if c is not None else "-" for c in alignment[0]]),
            "transcript": "".join([c if c is not None else "-" for c in alignment[1]]),
            "score": alignment[2]
        }

from lib.src.align.aligner.google.AbstractGoogleAlignerStrategy import AbstractGoogleAlignerStrategy
from lib.src.align.sequence_alignment.semi_global import semi_global
from typing import Dict, Any
from memory_profiler import profile


class GoogleSemiglobalCharacterAlignerStrategy(AbstractGoogleAlignerStrategy):
    """
    Semi-global alignment, character based
    """

    @staticmethod
    # @profile
    def perform_alignment(transcript: str, google_output: object, verbosity: int,
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

            :return: Equality of strings
            """
            return a == b

        alignment = semi_global(
            list(google_output),
            list(transcript),
            alignment_parameters["algorithm"]["match_reward"],
            alignment_parameters["algorithm"]["mismatch_penalty"],
            alignment_parameters["algorithm"]["gap_penalty"],
            compare
        )

        return {
            "google": ''.join([c if c is not None else "-" for c in alignment[0]]),
            "transcript": ''.join([c if c is not None else "-" for c in alignment[1]]),
            "score": alignment[2]
        }

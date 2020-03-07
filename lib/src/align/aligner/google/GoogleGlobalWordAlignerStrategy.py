from lib.src.align.aligner.google.AbstractGoogleAlignerStrategy import AbstractGoogleAlignerStrategy
from lib.src.align.sequence_alignment.needleman_wunsch import needleman_wunsch
from typing import Dict, Any
from lib.src.align.sequence_alignment.bag_distance_similarity import bag_distance_similarity


class GoogleGlobalWordAlignerStrategy(AbstractGoogleAlignerStrategy):
    """
    Global alignment, word based
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
            Checks if two words cen be considered equal
            :param a: String to compare
            :param b: String to compare
            :return: Equality of strings
            """
            return bag_distance_similarity(a, b) >= 0.6

        alignment = needleman_wunsch(
            google_output.split(" "),
            transcript.split(" "),
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

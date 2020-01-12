from lib.src.align.aligner.google.GoogleFilesAligner import GoogleFilesAligner
from lib.src.align.compare.compare_alignments import compare_alignments
from typing import Dict, Any, List
from scipy.optimize import minimize
import numpy as np


def adjust_parameters(input_path: str, output_path: str, google_files_aligner: GoogleFilesAligner, alignment_parameters: Dict[str, Any], verbosity: int) -> None:
    """
    Tries to find the best parameters for google alignment.
    :param input_path:           Path to load all alignments from
    :param output_path:          Path to write the alignments to
    :param google_files_aligner: GoogleFLiesAligner to re-align every epoch
    :param verbosity:            Verbosity of the output
    :return: None
    """

    def optimize_function(params: List) -> float:
        """
        Function to optimize against
        :param params: Numpy array of parameters in the order match_reward, mismatch_penalty and gap_penalty
        :return: Deviation of optimal value for mean IOU and F1 score.
        """
        google_files_aligner.alignment_parameters["match_reward"] = params[0]
        google_files_aligner.alignment_parameters["mismatch_penalty"] = params[1]
        google_files_aligner.alignment_parameters["gap_penalty"] = params[2]
        google_files_aligner.align_files(input_path, output_path, 0)

        result = compare_alignments(input_path, 0, "hand", "google", True, alignment_parameters)

        return 1 - result["ious"]["mean"] * result["appearance"]["f1_score"]

    x0 = np.array([alignment_parameters["algorithm"]["match_reward"], alignment_parameters["algorithm"]["mismatch_penalty"], alignment_parameters["algorithm"]["gap_penalty"]])
    res = minimize(optimize_function, x0, method='nelder-mead', options = {'xatol': 1e-8, 'disp': True})

    print(res)
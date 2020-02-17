from bin._bin import bin_print
from lib.src.align.aligner.google.GoogleFilesAligner import GoogleFilesAligner
from lib.src.align.compare.compare_alignments import compare_alignments
from typing import Dict, Any, List
from GPyOpt.methods import BayesianOptimization
import numpy as np


def optimize_parameters(
        input_path: str,
        output_path: str,
        google_files_aligner: GoogleFilesAligner,
        alignment_parameters: Dict[str, Any],
        convergence_plot_file: str,
        acquisition_plot_file: str,
        verbosity: int
) -> None:
    """
    Tries to find the best parameters for google alignment.
    :param input_path:            Path to load all alignments from
    :param output_path:           Path to write the alignments to
    :param google_files_aligner:  GoogleFLiesAligner to re-align every epoch
    :param alignment_parameters:  Alignment parameters for comparison
    :param convergence_plot_file: Where to save the convergence plot
    :param acquisition_plot_file: Where to save the acquisition plot
    :param verbosity:             Verbosity of the output
    :return: None
    """

    def optimize_function(params: List) -> float:
        """
        Function to optimize against
        :param params: Parameters given by BOpt
        :return: 1 - Mean IOU * F1
        """
        bin_print(verbosity, 1, "Starting new iteration...")

        google_files_aligner.alignment_parameters["algorithm"]["match_reward"] = params[0][0]
        google_files_aligner.alignment_parameters["algorithm"]["mismatch_penalty"] = params[0][1]
        google_files_aligner.alignment_parameters["algorithm"]["gap_penalty"] = params[0][2]

        bin_print(verbosity, 3, "Configured params: ", google_files_aligner.alignment_parameters)

        google_files_aligner.align_files(input_path, output_path, 0)

        result = compare_alignments(input_path, 0, "hand", "google", False, alignment_parameters)

        # score = result["scores"]["deviation"]["mean"] * (1 - (result["ious"]["mean"] * result["appearance"]["f1_score"]))
        score = 1 - result["ious"]["mean"]

        bin_print(verbosity, 1, "Parameters:                         ", params)
        bin_print(verbosity, 1, "Achieved score (smaller == better): ", score)

        return score

    domain = [
        {'name': 'match_reward', 'type': 'continuous', 'domain': (0, 100)},
        {'name': 'mismatch_penalty', 'type': 'continuous', 'domain': (-100, 0)},
        {'name': 'gap_penalty', 'type': 'continuous', 'domain': (-100, 0)},
    ]

    bopt = BayesianOptimization(f=optimize_function, domain=domain)

    bopt.run_optimization(max_iter=25)

    bopt.plot_convergence(filename=convergence_plot_file)
    bopt.plot_acquisition(filename=acquisition_plot_file)

    bin_print(verbosity, 0, "Best values:", bopt.x_opt)

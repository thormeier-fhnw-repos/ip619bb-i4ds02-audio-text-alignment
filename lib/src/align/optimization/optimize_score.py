from bin._bin import bin_print
from lib.src.align.compare.compare_alignments import compare_alignments
from lib.src.measurement.pearsonr_lists import pearsonr_lists
from typing import Dict, Any, List
from GPyOpt.methods import BayesianOptimization


def optimize_score(
        input_path: str,
        alignment_parameters: Dict[str, Any],
        convergence_plot_file: str,
        verbosity: int
) -> None:
    """
    Tries to find the best parameters for overall score.

    :param input_path:            Path to load all alignments from
    :param alignment_parameters:  Alignment parameters for comparison
    :param convergence_plot_file: Where to save the convergence plot
    :param verbosity:             Verbosity of the output

    :return: None
    """
    def optimize_function(params: List) -> float:
        """
        Function to optimize against

        :param params: Parameters given by BOpt

        :return: Calculated score
        """
        bin_print(verbosity, 2, "Parameters: ", params)

        alignment_parameters["score_weights"]["gaps_google"] = params[0][0]
        alignment_parameters["score_weights"]["gaps_transcript"] = params[0][1]
        alignment_parameters["score_weights"]["alignment_score"] = params[0][2]
        alignment_parameters["score_weights"]["google_confidence"] = params[0][3]

        results = compare_alignments(input_path, 0, "hand", "google", True, alignment_parameters)

        correlation_ious = pearsonr_lists(results["scores"]["ious"]["all"], results["scores"]["calculated"]["all"])
        correlation_deviation = pearsonr_lists(results["scores"]["deviation"]["all"], results["scores"]["calculated"]["all"])

        bin_print(verbosity, 1, "Correlation IOUs: ", correlation_ious)
        bin_print(verbosity, 1, "Correlation deviation: ", correlation_deviation)

        # Only maximize correlation with IOU
        return abs(correlation_ious)

    domain = [
        {"name": "gaps_google", "type": "continuous", "domain": (-100, 100)},
        {"name": "gaps_transcript", "type": "continuous", "domain": (-100, 100)},
        {"name": "alignment_score", "type": "continuous", "domain": (-100, 100)},
        {"name": "google_confidence", "type": "continuous", "domain": (-100, 100)},
    ]

    bopt = BayesianOptimization(
        f=optimize_function,
        domain=domain,
        model_type="GP",
        acquisition_type="EI",
        acquisition_jitter=0.05,
        maximize=True
    )

    bopt.run_optimization(max_iter=250)

    bopt.plot_convergence(filename=convergence_plot_file)

    bin_print(verbosity, 0, "Best values:", bopt.x_opt)

#!/usr/bin/python
import sys

sys.path.append(".")

from bin._bin import intro, bin_print, load_config
import time
from lib.src.align.aligner.get_aligner import get_aligner
from lib.src.align.optimization.optimize_parameters import optimize_parameters


def main(argv: list) -> None:
    title = "Optimize alignments"
    description = """
Tries to find the best alignment parameters based on Bayesian optimization.

Usage:
    python optimize_parameters.py --path=<path> --config=<path> --convergence-plot-file=<path> [-v|-vv|-vvv]

Args:
    --path:                  Path to read alignment data from
    --config:                Path to configuration
    --convergence-plot-file: Filename for the plot of the convergence, PNG
    -v|-vv|-vvv:             Verbosity level of the output
    -h:                      Prints this help
    """
    args = ["path=", "config=", "convergence-plot-file="]

    input_args = intro(title, description, args, argv)

    start = time.time()
    config = load_config(input_args["config"])

    bin_print(input_args["verbosity"], 2, "Loaded configuration: ", config)

    aligner = get_aligner(config)

    optimize_parameters(
        input_args["path"],
        input_args["path"],
        aligner,
        config,
        input_args["convergence-plot-file"],
        input_args["verbosity"]
    )

    end = time.time()

    bin_print(input_args["verbosity"], 0, "Done.")
    bin_print(input_args["verbosity"], 1, "Time elapsed:", (end - start))


if __name__ == "__main__":
    print("")
    main(sys.argv[1:])
    print("")

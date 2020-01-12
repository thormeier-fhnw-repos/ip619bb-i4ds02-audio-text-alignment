#!/usr/bin/python
import sys

sys.path.append('.')

from bin._bin import intro, bin_print, load_config
import time
from lib.src.align.aligner.get_aligner import get_aligner
from lib.src.align.parameter_adjustment.adjust_parameters import adjust_parameters


def main(argv: list) -> None:
    title = "Create alignment"
    description = """
Tries to find the best alignment parameters based on stochastic gradient descent.

Usage:
    python get_best_parameters.py --path=<path> --config=<path> [-v|-vv|-vvv]

Args:
    --path:      Path to read raw data from and write alignments to
    --config:    Path to configuration
    -v|-vv|-vvv: Verbosity level of the output
    -h:          Prints this help
    """
    args = ["path=", "config="]

    input_args = intro(title, description, args, argv)

    start = time.time()
    config = load_config(input_args["config"])

    bin_print(input_args["verbosity"], 2, "Loaded configuration: ", config)

    aligner = get_aligner(config)

    adjust_parameters(input_args["path"], input_args["path"], aligner, config, input_args["verbosity"])

    end = time.time()

    bin_print(input_args["verbosity"], 0, "Done.")
    bin_print(input_args["verbosity"], 1, "Time elapsed:", (end - start))


if __name__ == "__main__":
    print("")
    main(sys.argv[1:])
    print("")

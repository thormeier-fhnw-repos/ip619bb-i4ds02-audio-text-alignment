#!/usr/bin/python
import sys

sys.path.append('.')

from bin._bin import intro, bin_print, load_config
import time
from lib.src.align.aligner.get_aligner import get_aligner
from string import punctuation


def main(argv: list) -> None:
    title = "Create alignment"
    description = """
Creates an alignment based on configuration. See README.md for setting up a correct configuration.

Usage:
    python create_alignment.py --path=<path> --config=<path> [-v|-vv|-vvv]
    
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

    aligner.align_files(input_args["path"], input_args["path"], input_args["verbosity"])

    end = time.time()

    bin_print(input_args["verbosity"], 0, "Done.")
    bin_print(input_args["verbosity"], 1, "Time elapsed:", (end - start))


if __name__ == "__main__":
    print("")
    main(sys.argv[1:])
    print("")

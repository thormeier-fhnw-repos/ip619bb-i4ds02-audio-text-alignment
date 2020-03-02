#!/usr/bin/python
import sys

sys.path.append(".")

from bin._bin import intro, bin_print
from lib.src.align.utils.fix_hand_alignments import fix_hand_alignments
import time


def main(argv: list) -> None:
    title = "Fix hand alignments"
    description = """
Fix hand alignments: Reshuffle training data and/or assign `-` to nonexisting sentences.

Usage:
    python fix_hand_alignments.py --path=<path> [-v|-vv|-vvv] [--fix-nonexisting] [--reshuffle-training]

Args:
    --path:               Path to read alignment data
    -v|-vv|-vvv:          Verbosity level of the output
    --fix-nonexisting:    If non-existing sentences should be marked with `-` for interval start and end points
    --reshuffle-training: Select a new 70% of all sentences as training data
    -h:                   Prints this help
        """
    args = ["path=", "config=", "fix-nonexisting", "reshuffle-training"]
    input_args = intro(title, description, args, argv)

    input_args["fix-nonexisting"] = True if "with-list" in input_args else False
    input_args["reshuffle-training"] = True if "get-low-means" in input_args else False

    start = time.time()

    fix_hand_alignments(input_args["path"], input_args["fix-nonexisting"], input_args["reshuffle-training"], input_args["verbosity"])
    end = time.time()

    bin_print(input_args["verbosity"], 0, "Done.")
    bin_print(input_args["verbosity"], 1, "Time elapsed:", (end - start))


if __name__ == "__main__":
    print("")
    main(sys.argv[1:])
    print("")

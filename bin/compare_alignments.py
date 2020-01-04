#!/usr/bin/python
import sys

sys.path.append('.')
from bin._bin import intro, bin_print
from lib.src.align.compare.compare_alignments import compare_alignments
import time


def main(argv: list) -> None:
    title = "Compare alignments"
    description = """
Compares two kinds of alignments

Usage:
    python compare_alignment.py --path=<path> --type1=basic,hand,random,google --type2=basic,hand,random,google [-v|-vv|-vvv] [--with-list] [--get-low-means] [--training-only]

Args:
    --path:          Path to read alignment data
    --type1:         First type to compare, one of basic, hand, random or google
    --type2:         Second type to compare, one of basic, hand, random or google
    -v|-vv|-vvv:     Verbosity level of the output
    --with-list:     Include a list with all calculated IOUs for copy/paste (to use in an EXCEL sheet, for example)
    --get-low-means: Includes a list of wav files with a mean IOU < 0.3, for debugging purposes
    --training-only: Only ever compares sentences marked with [TRAINING] in the first type of the alignment
    -h:              Prints this help
    """
    args = ["path=", "type1=", "type2=", "with-list", "get-low-means", "training-only"]
    input_args = intro(title, description, args, argv)

    input_args["with-list"] = True if "with-list" in input_args else False
    input_args["get-low-means"] = True if "get-low-means" in input_args else False
    input_args["training-only"] = True if "training-only" in input_args else False

    start = time.time()
    compare_alignments(input_args["path"], input_args["verbosity"], input_args["type1"], input_args["type2"], input_args["with-list"], input_args["get-low-means"], input_args["training-only"])
    end = time.time()

    bin_print(input_args["verbosity"], 0, "Done.")
    bin_print(input_args["verbosity"], 1, "Time elapsed:", (end - start))


if __name__ == "__main__":
    print("")
    main(sys.argv[1:])
    print("")

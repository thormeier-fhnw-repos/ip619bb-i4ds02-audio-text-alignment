#!/usr/bin/python
import sys

sys.path.append('.')

import getopt
from bin._bin import intro, bin_print
from lib.src.align.basic.create_basic_alignments import create_basic_alignments
import time


def main(argv: list) -> None:
    input_args = intro("Create basic alignment", "Creates a basic alignment for all pairs of wav/txt files in a given "
                                                 "directory.\n\ncreate_basic_alignment.py --path=<path> ["
                                                 "-v|-vv|-vvv]", ["path="], argv)

    start = time.time()
    create_basic_alignments(input_args["path"], input_args["path"], input_args["verbosity"])
    end = time.time()

    bin_print(input_args["verbosity"], 0, "Done.")
    bin_print(input_args["verbosity"], 1, "Time elapsed:", (end - start))


if __name__ == "__main__":
    print("")
    main(sys.argv[1:])
    print("")

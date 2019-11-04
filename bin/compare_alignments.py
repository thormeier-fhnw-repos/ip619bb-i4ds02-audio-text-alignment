#!/usr/bin/python
import sys

sys.path.append('.')
from bin._bin import intro, bin_print
from lib.src.align.compare.compare_alignments import compare_alignments
import time


def main(argv: list) -> None:
    input_args = intro("Compare alignments",
                       "Compares basic, hand and auto alignments.\n\ncompare_alignment.py --path=<path> --type1=basic,hand,random --type2=basic,hand,random [-v|-vv|-vvv] [--with-list]",
                       ["path=", "type1=", "type2=", "with-list"], argv)

    input_args["with-list"] = True if "with-list" in input_args else False

    start = time.time()
    compare_alignments(input_args["path"], input_args["verbosity"], input_args["type1"], input_args["type2"], input_args["with-list"])
    end = time.time()

    bin_print(input_args["verbosity"], 0, "Done.")
    bin_print(input_args["verbosity"], 1, "Time elapsed:", (end - start))


if __name__ == "__main__":
    print("")
    main(sys.argv[1:])
    print("")

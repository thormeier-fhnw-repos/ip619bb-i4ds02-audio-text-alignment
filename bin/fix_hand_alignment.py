#!/usr/bin/python
import sys

sys.path.append('.')
from bin._bin import intro, bin_print
from lib.src.align.hand.fix_hand_alignments import fix_hand_alignments
import time


def main(argv: list) -> None:
    input_args = intro("Fix hand alignments",
                       "Moves non-existing sentences to beginning of file.\n\nfix_hand_alignments.py --path=<path> [-v|-vv|-vvv]",
                       ["path="], argv)

    start = time.time()
    fix_hand_alignments(input_args["path"], input_args["verbosity"])
    end = time.time()

    bin_print(input_args["verbosity"], 0, "Done.")
    bin_print(input_args["verbosity"], 1, "Time elapsed:", (end - start))


if __name__ == "__main__":
    print("")
    main(sys.argv[1:])
    print("")

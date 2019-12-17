#!/usr/bin/python
import sys

sys.path.append('.')
from bin._bin import intro, bin_print
from lib.src.align.google.create_google_alignments import create_google_alignments
import time


def main(argv: list) -> None:
    input_args = intro("Create Google STT alignment",
                       "Creates an alignment in Audacity label format, based on Google's STT.\n\ncreate_google_alignment.py --inputpath=<path> --outputpath=<path> [-v|-vv|-vvv]",
                       ["inputpath=", "outputpath="], argv)

    start = time.time()
    create_google_alignments(input_args["inputpath"], input_args["outputpath"], input_args["verbosity"])
    end = time.time()

    bin_print(input_args["verbosity"], 0, "Done.")
    bin_print(input_args["verbosity"], 1, "Time elapsed:", (end - start))


if __name__ == "__main__":
    print("")
    main(sys.argv[1:])
    print("")

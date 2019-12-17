#!/usr/bin/python
import sys

sys.path.append('.')
from bin._bin import intro, bin_print
import time


def main(argv: list) -> None:
    input_args = intro("Monitor",
                       "Monitor a certain command from the bin folder.\n\nmonitor.py --command=<modulename> --n=<number> [any command params, such as --inputpath]",
                       ["command=", "n="], argv[:2])

    start = time.time()
    bin_print(0, 0, "Loading " + input_args["command"])
    mod = __import__(input_args["command"])

    bin_print(0, 0, "Executing main " + str(input_args["n"]) + "times while monitoring, swallowing all output to stdout...")

    end = time.time()


if __name__ == "__main__":
    print("")
    main(sys.argv[1:])
    print("")

#!/usr/bin/python
import sys

sys.path.append(".")

import os
from bin._bin import intro, bin_print
from lib.src.google.get_and_save_raw import get_and_save_raw
import time


def main(argv: list) -> None:
    title = "Get Google recognition"
    description = """
Gets the Speech Recognition result of Google Cloud API and stores it in a caching folder.

Usage:
    python get_google_recognition_raw.py --path=<path> --authpath=<path> --bucket=<bucket name> --outpath=<path> [-v|-vv|-vvv]

Args:
    --path:      Path to read transcript files from (needed to filter which files to actually transcript)
    --authpath:  Path containing the authentication files necessary to connect to Google Cloud API services
    --bucket:    Name of the bucket containing all FLAC files
    --outpath:   Path to write the raw JSON output to
    -v|-vv|-vvv: Verbosity level of the output
    -h:          Prints this help
        """
    args = ["path=", "config="]

    input_args = intro(title, description, args, argv)

    input_args = intro("Get Google recognition raw",
                       "Gets the Speech Recognition result of Google Cloud API and stores it in a caching folder.\n\nget_google_recognition_raw.py --path=<path> --authpath=<path> --bucket=<bucket name> --outpath=<path> [-v|-vv|-vvv]",
                       ["path=", "authpath=", "outpath=", "bucket="], argv)

    # Authenticate globally with specified client JSON
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = input_args["authpath"]

    start = time.time()
    get_and_save_raw(input_args["path"], input_args["bucket"], input_args["outpath"], input_args["verbosity"])
    end = time.time()

    bin_print(input_args["verbosity"], 0, "Done.")
    bin_print(input_args["verbosity"], 1, "Time elapsed:", (end - start))

if __name__ == "__main__":
    print("")
    main(sys.argv[1:])
    print("")

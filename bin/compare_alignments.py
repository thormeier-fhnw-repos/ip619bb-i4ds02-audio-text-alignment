#!/usr/bin/python
import sys

sys.path.append('.')
from bin._bin import intro, bin_print
from lib.src.align.compare.compare_alignments import compare_alignments
import time
from prettytable import PrettyTable


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
    results = compare_alignments(input_args["path"], input_args["verbosity"], input_args["type1"], input_args["type2"], input_args["training-only"])

    verbosity = input_args["verbosity"]

    for file in results["ious"]["per_file"].items():
        bin_print(verbosity, 3, "IOUs for", file[0], ":", file[1]["all"])
        bin_print(verbosity, 0, file[0], ", " + input_args["type1"] + " vs. " + input_args["type2"] + ":")
        bin_print(verbosity, 0, " - Mean IOU:   ", file[1]["mean"])
        bin_print(verbosity, 0, " - Median IOU: ", file[1]["median"])

    bin_print(verbosity, 3, "All IOUs:", results["ious"]["all"])
    bin_print(verbosity, 0, "========")
    bin_print(verbosity, 0, input_args["type1"] + " vs. " + input_args["type2"] + ":")
    bin_print(verbosity, 0, "Total number of sentences:", results["no_sentences"]["total"])
    bin_print(verbosity, 0, "--------")
    bin_print(verbosity, 0, "IOU")
    bin_print(verbosity, 0, " - Mean IOU:   ", results["ious"]["mean"])
    bin_print(verbosity, 0, " - Median IOU: ", results["ious"]["median"])
    bin_print(verbosity, 0, " - Number of sentences appearing: ", results["no_sentences"]["appearing"])

    bin_print(verbosity, 0, "--------")

    t = PrettyTable()
    t.field_names = ["", "Condition positive", "Condition negative"]
    t.add_row(["Predicted positive", results["appearance"]["true_positives"], results["appearance"]["false_positives"]])
    t.add_row(["Predicted negative", results["appearance"]["false_negatives"], results["appearance"]["true_negatives"]])

    bin_print(verbosity, 0, "Sentences appearing")
    bin_print(verbosity, 0, "\n" + str(t))
    bin_print(verbosity, 0, "Precision: ", results["appearance"]["precision"])
    bin_print(verbosity, 0, "Recall:    ", results["appearance"]["recall"])
    bin_print(verbosity, 0, "F1 score:  ", results["appearance"]["f1_score"])

    if input_args["with-list"]:
        bin_print(verbosity, 0, "Outputting all values as copy/pastable list:")
        print("\n".join([str(v[0]) for v in [v for v in results["ious"]["all"]] if v[0] <= 1.0]))

    if input_args["get-low-means"]:
        bin_print(verbosity, 0, "Outputting copy/pastable list of low (<0.3) mean IOU files:")
        print(results["ious"]["low"])

    end = time.time()

    bin_print(input_args["verbosity"], 0, "Done.")
    bin_print(input_args["verbosity"], 1, "Time elapsed:", (end - start))


if __name__ == "__main__":
    print("")
    main(sys.argv[1:])
    print("")

#!/usr/bin/python
import sys

sys.path.append('.')
from bin._bin import intro, bin_print, load_config
from lib.src.align.compare.compare_alignments import compare_alignments
import time
from prettytable import PrettyTable
from lib.src.measurement.pearsonr_lists import pearsonr_lists
import numpy as np


def main(argv: list) -> None:
    title = "Compare alignments"
    description = """
Compares two kinds of alignments

Usage:
    python compare_alignment.py --path=<path> --type1=basic,hand,random,google --type2=basic,hand,random,google --config=<path> [-v|-vv|-vvv] [--with-list] [--get-low-means] [--training-only]

Args:
    --path:          Path to read alignment data
    --type1:         First type to compare, one of basic, hand, random or google
    --type2:         Second type to compare, one of basic, hand, random or google
    --config         Path to config file
    -v|-vv|-vvv:     Verbosity level of the output
    --with-list:     Include a list with all calculated IOUs for copy/paste (to use in an EXCEL sheet, for example)
    --get-low-means: Includes a list of wav files with a mean IOU < 0.3, for debugging purposes
    --training-only: Only ever compares sentences marked with [TRAINING] in the first type of the alignment
    -h:              Prints this help
    """
    args = ["path=", "type1=", "type2=", "config=",  "with-list", "get-low-means", "training-only"]
    input_args = intro(title, description, args, argv)

    config = load_config(input_args["config"])

    input_args["with-list"] = True if "with-list" in input_args else False
    input_args["get-low-means"] = True if "get-low-means" in input_args else False
    input_args["training-only"] = True if "training-only" in input_args else False

    start = time.time()
    results = compare_alignments(input_args["path"], input_args["verbosity"], input_args["type1"], input_args["type2"], input_args["training-only"], config)

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
    bin_print(verbosity, 0, "--------")
    bin_print(verbosity, 0, "Deviation (absolute)")
    bin_print(verbosity, 0, " - Mean deviation:   ", results["scores"]["deviation"]["mean"])
    bin_print(verbosity, 0, " - Median deviation: ", results["scores"]["deviation"]["median"])
    bin_print(verbosity, 0, "--------")
    bin_print(verbosity, 0, "Calculated score")
    bin_print(verbosity, 0, " - Mean calculated score:   ", np.mean(results["scores"]["calculated"]["all"]))
    bin_print(verbosity, 0, " - Median calculated score: ", np.median(results["scores"]["calculated"]["all"]))
    bin_print(verbosity, 0, "--------")
    bin_print(verbosity, 0, "Number of sentences appearing: ", results["no_sentences"]["appearing"])

    tPrecisionRecall = PrettyTable()
    tPrecisionRecall.field_names = ["", "Condition positive", "Condition negative"]
    tPrecisionRecall.add_row(["Predicted positive", results["appearance"]["true_positives"], results["appearance"]["false_positives"]])
    tPrecisionRecall.add_row(["Predicted negative", results["appearance"]["false_negatives"], results["appearance"]["true_negatives"]])

    bin_print(verbosity, 0, "Sentences appearing")
    bin_print(verbosity, 0, "\n" + str(tPrecisionRecall))
    bin_print(verbosity, 0, "Precision: ", results["appearance"]["precision"])
    bin_print(verbosity, 0, "Recall:    ", results["appearance"]["recall"])
    bin_print(verbosity, 0, "F1 score:  ", results["appearance"]["f1_score"])

    if input_args["with-list"]:
        bin_print(verbosity, 0, "Outputting all values as copy/pastable list:")
        print("\n".join([str(v[0]) for v in [v for v in results["ious"]["all"]] if v[0] <= 1.0]))

    if input_args["get-low-means"]:
        bin_print(verbosity, 0, "Outputting copy/pastable list of low (<0.3) mean IOU files:")
        print(results["ious"]["low"])


    tPearson = PrettyTable()
    tPearson.field_names = ["", "IOU", "Deviation", "Alignment score", "Google confidence", "Calculated confidence", "Google gaps percentage", "Transcript gaps percentage", "Calculated score"]
    tPearson.add_row([
        "IOU",
        pearsonr_lists(results["ious"]["all_only"], results["ious"]["all_only"]),
        pearsonr_lists(results["ious"]["all_only"], results["scores"]["deviation"]["all"]),
        pearsonr_lists(results["ious"]["all_only"], results["scores"]["alignment_scores"]["all"]),
        pearsonr_lists(results["ious"]["all_only"], results["scores"]["google_confidence"]["all"]),
        pearsonr_lists(results["ious"]["all_only"], results["scores"]["calculated"]["all"]),
        pearsonr_lists(results["ious"]["all_only"], results["scores"]["google_gaps"]["all"]),
        pearsonr_lists(results["ious"]["all_only"], results["scores"]["transcript_gaps"]["all"]),
        pearsonr_lists(results["ious"]["all_only"], results["scores"]["calculated"]["all"])
    ])
    tPearson.add_row([
        "Deviation",
        pearsonr_lists(results["scores"]["deviation"]["all"], results["ious"]["all_only"]),
        pearsonr_lists(results["scores"]["deviation"]["all"], results["scores"]["deviation"]["all"]),
        pearsonr_lists(results["scores"]["deviation"]["all"], results["scores"]["alignment_scores"]["all"]),
        pearsonr_lists(results["scores"]["deviation"]["all"], results["scores"]["google_confidence"]["all"]),
        pearsonr_lists(results["scores"]["deviation"]["all"], results["scores"]["calculated"]["all"]),
        pearsonr_lists(results["scores"]["deviation"]["all"], results["scores"]["google_gaps"]["all"]),
        pearsonr_lists(results["scores"]["deviation"]["all"], results["scores"]["transcript_gaps"]["all"]),
        pearsonr_lists(results["scores"]["deviation"]["all"], results["scores"]["calculated"]["all"])
    ])
    tPearson.add_row([
        "Alignment score",
        pearsonr_lists(results["scores"]["alignment_scores"]["all"], results["ious"]["all_only"]),
        pearsonr_lists(results["scores"]["alignment_scores"]["all"], results["scores"]["deviation"]["all"]),
        pearsonr_lists(results["scores"]["alignment_scores"]["all"], results["scores"]["alignment_scores"]["all"]),
        pearsonr_lists(results["scores"]["alignment_scores"]["all"], results["scores"]["google_confidence"]["all"]),
        pearsonr_lists(results["scores"]["alignment_scores"]["all"], results["scores"]["calculated"]["all"]),
        pearsonr_lists(results["scores"]["alignment_scores"]["all"], results["scores"]["google_gaps"]["all"]),
        pearsonr_lists(results["scores"]["alignment_scores"]["all"], results["scores"]["transcript_gaps"]["all"]),
        pearsonr_lists(results["scores"]["alignment_scores"]["all"], results["scores"]["calculated"]["all"])
    ])
    tPearson.add_row([
        "Google confidence",
        pearsonr_lists(results["scores"]["google_confidence"]["all"], results["ious"]["all_only"]),
        pearsonr_lists(results["scores"]["google_confidence"]["all"], results["scores"]["deviation"]["all"]),
        pearsonr_lists(results["scores"]["google_confidence"]["all"], results["scores"]["alignment_scores"]["all"]),
        pearsonr_lists(results["scores"]["google_confidence"]["all"], results["scores"]["google_confidence"]["all"]),
        pearsonr_lists(results["scores"]["google_confidence"]["all"], results["scores"]["calculated"]["all"]),
        pearsonr_lists(results["scores"]["google_confidence"]["all"], results["scores"]["google_gaps"]["all"]),
        pearsonr_lists(results["scores"]["google_confidence"]["all"], results["scores"]["transcript_gaps"]["all"]),
        pearsonr_lists(results["scores"]["google_confidence"]["all"], results["scores"]["calculated"]["all"])
    ])
    tPearson.add_row([
        "Calculated confidence",
        pearsonr_lists(results["scores"]["calculated"]["all"], results["ious"]["all_only"]),
        pearsonr_lists(results["scores"]["calculated"]["all"], results["scores"]["deviation"]["all"]),
        pearsonr_lists(results["scores"]["calculated"]["all"], results["scores"]["alignment_scores"]["all"]),
        pearsonr_lists(results["scores"]["calculated"]["all"], results["scores"]["google_confidence"]["all"]),
        pearsonr_lists(results["scores"]["calculated"]["all"], results["scores"]["calculated"]["all"]),
        pearsonr_lists(results["scores"]["calculated"]["all"], results["scores"]["google_gaps"]["all"]),
        pearsonr_lists(results["scores"]["calculated"]["all"], results["scores"]["transcript_gaps"]["all"]),
        pearsonr_lists(results["scores"]["calculated"]["all"], results["scores"]["calculated"]["all"])
    ])
    tPearson.add_row([
        "Google gaps percentage",
        pearsonr_lists(results["scores"]["google_gaps"]["all"], results["ious"]["all_only"]),
        pearsonr_lists(results["scores"]["google_gaps"]["all"], results["scores"]["deviation"]["all"]),
        pearsonr_lists(results["scores"]["google_gaps"]["all"], results["scores"]["alignment_scores"]["all"]),
        pearsonr_lists(results["scores"]["google_gaps"]["all"], results["scores"]["google_confidence"]["all"]),
        pearsonr_lists(results["scores"]["google_gaps"]["all"], results["scores"]["calculated"]["all"]),
        pearsonr_lists(results["scores"]["google_gaps"]["all"], results["scores"]["google_gaps"]["all"]),
        pearsonr_lists(results["scores"]["google_gaps"]["all"], results["scores"]["transcript_gaps"]["all"]),
        pearsonr_lists(results["scores"]["google_gaps"]["all"], results["scores"]["calculated"]["all"])
    ])
    tPearson.add_row([
        "Transcript gaps percentage",
        pearsonr_lists(results["scores"]["transcript_gaps"]["all"], results["ious"]["all_only"]),
        pearsonr_lists(results["scores"]["transcript_gaps"]["all"], results["scores"]["deviation"]["all"]),
        pearsonr_lists(results["scores"]["transcript_gaps"]["all"], results["scores"]["alignment_scores"]["all"]),
        pearsonr_lists(results["scores"]["transcript_gaps"]["all"], results["scores"]["google_confidence"]["all"]),
        pearsonr_lists(results["scores"]["transcript_gaps"]["all"], results["scores"]["calculated"]["all"]),
        pearsonr_lists(results["scores"]["transcript_gaps"]["all"], results["scores"]["google_gaps"]["all"]),
        pearsonr_lists(results["scores"]["transcript_gaps"]["all"], results["scores"]["transcript_gaps"]["all"]),
        pearsonr_lists(results["scores"]["transcript_gaps"]["all"], results["scores"]["calculated"]["all"])
    ])
    tPearson.add_row([
        "Calculated score",
        pearsonr_lists(results["scores"]["calculated"]["all"], results["ious"]["all_only"]),
        pearsonr_lists(results["scores"]["calculated"]["all"], results["scores"]["deviation"]["all"]),
        pearsonr_lists(results["scores"]["calculated"]["all"], results["scores"]["alignment_scores"]["all"]),
        pearsonr_lists(results["scores"]["calculated"]["all"], results["scores"]["google_confidence"]["all"]),
        pearsonr_lists(results["scores"]["calculated"]["all"], results["scores"]["calculated"]["all"]),
        pearsonr_lists(results["scores"]["calculated"]["all"], results["scores"]["google_gaps"]["all"]),
        pearsonr_lists(results["scores"]["calculated"]["all"], results["scores"]["transcript_gaps"]["all"]),
        pearsonr_lists(results["scores"]["calculated"]["all"], results["scores"]["calculated"]["all"])
    ])

    bin_print(verbosity, 0, "Score correlations")
    bin_print(verbosity, 0, "\n" + str(tPearson))

    end = time.time()

    bin_print(input_args["verbosity"], 0, "Done.")
    bin_print(input_args["verbosity"], 1, "Time elapsed:", (end - start))


if __name__ == "__main__":
    print("")
    main(sys.argv[1:])
    print("")

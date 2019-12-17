from bin._bin import bin_print
from os import listdir
from os.path import isfile, join
from lib.src.align.compare.load_alignment import load_alignment
from lib.src.measurement.intersection_over_union import intersection_over_union
import numpy as np


def compare_alignments(input_path: str, verbosity: int, type1: str, type2: str, with_list: bool, get_low_means: bool, test_only: bool) -> None:
    """
    Compares all found alignments
    :param input_path: Input path
    :param verbosity: Verbosity level
    :param type1: First type for comparison
    :param type2: Second type for comparison
    :param with_list: If a list should be shown
    :param get_low_means: If only the low ones should be shown (0-0.05)
    :param test_only: Determines if a sentence has to be prefixed with [TEST] in order to be considered.
    :return: None
    """
    bin_print(verbosity, 1, "Reading files from", input_path)

    bin_print(verbosity, 2, "Trying to find all .txt files...")
    txt_files = [input_path + f for f in listdir(input_path) if isfile(join(input_path, f)) and f.split('.')[1] == "txt"]
    bin_print(verbosity, 3, "Found txt files:", txt_files)

    bin_print(verbosity, 2, "Filtering found files by ones containing alignment by " + type1 + "...")
    type1_alignments = [f for f in txt_files if "audacity_" + type1 in f]
    bin_print(verbosity, 3, "Found txt files containing alingment via " + type1 + ":", type1_alignments)

    ious = []
    low_ious = []

    bin_print(verbosity, 2, "Processing all " + type1 + " alignments...")
    for type1_alignment in type1_alignments:
        file_name = type1_alignment.replace("audacity_" + type1, "").replace(input_path, "").replace("_.txt", "")
        bin_print(verbosity, 3, "Processing", file_name)
        type1_aligned_sentences = load_alignment(type1_alignment)
        type2_aligned_sentences = load_alignment(type1_alignment.replace("audacity_" + type1, "audacity_" + type2))
        current_ious = [
            (intersection_over_union(pair[0].interval, pair[1].interval), pair[0].interval.get_length(), pair[1].interval.get_length(), pair[0].sentence, file_name) for pair in list(zip(type1_aligned_sentences, type2_aligned_sentences))
            if (not test_only or pair[0].sentence.startswith('[TEST]')) and (pair[0].interval.get_length() > 0.0001 and pair[1].interval.get_length() > 0.0001)
        ]

        if len(current_ious) == 0:
            bin_print(verbosity, 2, "No sentences found, skipping...")
            continue

        mean_iou = np.mean([v[0] for v in current_ious])
        median_iou = np.median([v[0] for v in current_ious])

        bin_print(verbosity, 3, "IOUs for", file_name, ":", current_ious)
        bin_print(verbosity, 0, file_name, ", " + type1 + " vs. " + type2 + ":")
        bin_print(verbosity, 0, " - Mean IOU:   ", mean_iou)
        bin_print(verbosity, 0, " - Median IOU: ", median_iou)

        if mean_iou <= 0.3:
            low_ious.append(file_name + ".wav")

        ious += current_ious

    bin_print(verbosity, 3, "All IOUs:", ious)
    bin_print(verbosity, 0, "--------")
    bin_print(verbosity, 0, type1 + " vs. " + type2 + ":")
    bin_print(verbosity, 0, " - Mean IOU:   ", np.mean([v[0] for v in ious]))
    bin_print(verbosity, 0, " - Median IOU: ", np.median([v[0] for v in ious]))
    bin_print(verbosity, 0, " - Number of sentences: ", len(ious))

    if with_list:
        bin_print(verbosity, 0, "Outputting all values as copy/pastable list:")
        print("\n".join([str(v[0]) for v in [v for v in ious] if v[0] <= 1.0]))

        for v in ious:
            if v[0] <= 0.1:
                print(v[4])

    if get_low_means:
        bin_print(verbosity, 0, "Outputting copy/pastable list of low (<0.3) mean IOU files:")
        print(low_ious)
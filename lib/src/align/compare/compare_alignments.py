from bin._bin import bin_print
from os import listdir
from os.path import isfile, join
from lib.src.align.compare.load_alignment import load_alignment
from lib.src.measurement.intersection_over_union import intersection_over_union
import numpy as np


def compare_alignments(input_path: str, verbosity: int, type1: str, type2: str) -> None:
    """
    Compares all found alignments
    :param input_path: Input path
    :param verbosity: Verbosity level
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
    bin_print(verbosity, 2, "Processing all " + type1 + " alignments...")
    for type1_alignment in type1_alignments:
        file_name = type1_alignment.replace("audacity_" + type1, "").replace(input_path, "").replace("_.txt", "")
        bin_print(verbosity, 3, "Processing", file_name)
        type1_aligned_sentences = load_alignment(type1_alignment)
        type2_aligned_sentences = load_alignment(type1_alignment.replace("audacity_" + type1, "audacity_" + type2))
        current_ious = [intersection_over_union(pair[0].interval, pair[1].interval) for pair in list(zip(type1_aligned_sentences, type2_aligned_sentences))]

        bin_print(verbosity, 3, "IOUs for", file_name, ":", current_ious)
        bin_print(verbosity, 0, file_name, ", " + type1 + " vs. " + type2 + ":")
        bin_print(verbosity, 0, " - Mean IOU:   ", np.mean(current_ious))
        bin_print(verbosity, 0, " - Median IOU: ", np.median(current_ious))

        ious += current_ious

    bin_print(verbosity, 3, "All IOUs:", ious)
    bin_print(verbosity, 0, "--------")
    bin_print(verbosity, 0, type1 + " vs. " + type2 + ":")
    bin_print(verbosity, 0, " - Mean IOU:   ", np.mean(ious))
    bin_print(verbosity, 0, " - Median IOU: ", np.median(ious))

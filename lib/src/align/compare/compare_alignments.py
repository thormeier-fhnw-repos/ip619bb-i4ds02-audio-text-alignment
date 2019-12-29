from bin._bin import bin_print
from os import listdir
from os.path import isfile, join
from lib.src.align.compare.load_alignment import load_alignment
from lib.src.measurement.intersection_over_union import intersection_over_union
import numpy as np


def compare_alignments(input_path: str, verbosity: int, type1: str, type2: str, with_list: bool, get_low_means: bool, training_only: bool) -> None:
    """
    Compares all found alignments
    :param input_path: Input path
    :param verbosity: Verbosity level
    :param type1: First type for comparison
    :param type2: Second type for comparison
    :param with_list: If a list should be shown
    :param get_low_means: If only the low ones should be shown (0-0.05)
    :param training_only: Determines if a sentence has to be prefixed with [TEST] in order to be considered.
    :return: None
    """
    epsilon = 0.0001

    bin_print(verbosity, 1, "Reading files from", input_path)

    bin_print(verbosity, 2, "Trying to find all .txt files...")
    txt_files = [input_path + f for f in listdir(input_path) if isfile(join(input_path, f)) and f.split('.')[1] == "txt"]
    bin_print(verbosity, 3, "Found txt files:", txt_files)

    bin_print(verbosity, 2, "Filtering found files by ones containing alignment by " + type1 + "...")
    type1_alignments = [f for f in txt_files if "audacity_" + type1 in f]
    bin_print(verbosity, 3, "Found txt files containing alingment via " + type1 + ":", type1_alignments)

    ious = []
    low_ious = []
    total_sentences = 0
    sentences_appearing_true_positives = 0
    sentences_appearing_false_positives = 0
    sentences_appearing_true_negatives = 0
    sentences_appearing_false_negatives = 0

    bin_print(verbosity, 2, "Processing all " + type1 + " alignments...")
    for type1_alignment in type1_alignments:
        file_name = type1_alignment.replace("audacity_" + type1, "").replace(input_path, "").replace("_.txt", "")
        bin_print(verbosity, 3, "Processing", file_name)
        type1_aligned_sentences = load_alignment(type1_alignment)
        type2_aligned_sentences = load_alignment(type1_alignment.replace("audacity_" + type1, "audacity_" + type2))

        sentence_pairs = [pair for pair in list(zip(type1_aligned_sentences, type2_aligned_sentences)) if (not training_only or pair[0].sentence.startswith('[TRAINING]'))]

        total_sentences += len(sentence_pairs)

        current_ious = [
            (intersection_over_union(pair[0].interval, pair[1].interval), pair[0].interval.get_length(), pair[1].interval.get_length(), pair[0].sentence, file_name) for pair in sentence_pairs
            if (pair[0].interval.get_length() > epsilon and pair[1].interval.get_length() > epsilon)
        ]

        # Find sentences that are marked on either side as not appearing at all.
        pairs_sentence_not_appearing = [
            pair for pair in sentence_pairs if (pair[0].interval.get_length() <= epsilon or pair[1].interval.get_length() <= epsilon)
        ]

        #print(len(pairs_sentence_not_appearing))

        # Count those sentences: which of those don't appear in both oder in either one?
        for pair in pairs_sentence_not_appearing:
            if pair[0].interval.get_length() <= epsilon and pair[1].interval.get_length() <= epsilon:
                sentences_appearing_true_negatives += 1
            elif pair[0].interval.get_length() <= epsilon and pair[1].interval.get_length() > epsilon:
                sentences_appearing_false_positives += 1
            elif pair[0].interval.get_length() > epsilon and pair[1].interval.get_length() <= epsilon:
                sentences_appearing_false_negatives += 1

        # All sentences appearing in both are considered true negatives
        sentences_appearing_true_positives += len(current_ious)

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

    precision = sentences_appearing_true_positives / (sentences_appearing_true_positives + sentences_appearing_false_positives)
    recall = sentences_appearing_true_positives / (sentences_appearing_true_positives + sentences_appearing_false_negatives)
    f1_score = 2 * ((precision * recall) / (precision + recall))

    bin_print(verbosity, 3, "All IOUs:", ious)
    bin_print(verbosity, 0, "========")
    bin_print(verbosity, 0, type1 + " vs. " + type2 + ":")
    bin_print(verbosity, 0, "Total number of sentences:", total_sentences)
    bin_print(verbosity, 0, "--------")
    bin_print(verbosity, 0, "IOU")
    bin_print(verbosity, 0, " - Mean IOU:   ", np.mean([v[0] for v in ious]))
    bin_print(verbosity, 0, " - Median IOU: ", np.median([v[0] for v in ious]))
    bin_print(verbosity, 0, " - Number of sentences appearing: ", len(ious))

    bin_print(verbosity, 0, "--------")
    bin_print(verbosity, 0, "Sentences appearing")
    bin_print(verbosity, 0, " - true negatives:  ", sentences_appearing_true_negatives)
    bin_print(verbosity, 0, " - false negatives: ", sentences_appearing_false_negatives)
    bin_print(verbosity, 0, " - true positives:  ", sentences_appearing_true_positives)
    bin_print(verbosity, 0, " - false positives: ", sentences_appearing_false_positives)
    bin_print(verbosity, 0, "Precision: ", precision)
    bin_print(verbosity, 0, "Recall:    ", recall)
    bin_print(verbosity, 0, "F1 score:  ", f1_score)

    if with_list:
        bin_print(verbosity, 0, "Outputting all values as copy/pastable list:")
        print("\n".join([str(v[0]) for v in [v for v in ious] if v[0] <= 1.0]))

        for v in ious:
            if v[0] <= 0.1:
                print(v[4])

    if get_low_means:
        bin_print(verbosity, 0, "Outputting copy/pastable list of low (<0.3) mean IOU files:")
        print(low_ious)
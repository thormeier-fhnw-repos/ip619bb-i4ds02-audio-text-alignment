from bin._bin import bin_print
from os import listdir
from os.path import isfile, join
from lib.src.align.compare.load_alignment import load_alignment
from lib.src.measurement.intersection_over_union import intersection_over_union
from lib.src.model.Sentence import Sentence
from lib.src.align.utils.calculate_overall_score import calculate_overall_score
import numpy as np
from typing import Dict, Any
import os
from memory_profiler import profile


# @profile
def compare_alignments(input_path: str, verbosity: int, type1: str, type2: str, training_only: bool, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compares all found alignments

    :param input_path:    Input path
    :param verbosity:     Verbosity level
    :param type1:         First type for comparison
    :param type2:         Second type for comparison
    :param training_only: Determines if a sentence has to be prefixed with [TEST] in order to be considered.
    :param config:        Configuration dict, see README

    :return: Dict of all results
    """

    if input_path.endswith(os.sep):
        input_path = input_path[:-1]

    epsilon = config["no_appearance"]["interval_length"]

    bin_print(verbosity, 1, "Reading files from", input_path)

    bin_print(verbosity, 2, "Trying to find all .txt files...")
    txt_files = [input_path + os.sep + f for f in listdir(input_path) if
                 isfile(join(input_path, f)) and f.split(".")[1] == "txt"]
    bin_print(verbosity, 3, "Found txt files:", txt_files)

    bin_print(verbosity, 2, "Filtering found files by ones containing alignment by " + type1 + "...")
    type1_alignments = [f for f in txt_files if "audacity_" + type1 in f]
    bin_print(verbosity, 3, "Found txt files containing alingment via " + type1 + ":", type1_alignments)

    ious = []
    low_ious = []
    google_confidences = []
    sentence_scores = []
    deviations = []
    google_gaps = []
    transcript_gaps = []
    total_sentences = 0
    sentences_appearing_true_positives = 0
    sentences_appearing_false_positives = 0
    sentences_appearing_true_negatives = 0
    sentences_appearing_false_negatives = 0

    ious_per_file = {}

    bin_print(verbosity, 2, "Processing all " + type1 + " alignments...")
    for type1_alignment in type1_alignments:
        file_name = type1_alignment.replace("audacity_" + type1, "").replace(input_path, "").replace("_.txt", "")
        bin_print(verbosity, 3, "Processing", file_name)
        type1_aligned_sentences = load_alignment(type1_alignment)
        try:
            type2_aligned_sentences = load_alignment(type1_alignment.replace("audacity_" + type1, "audacity_" + type2))
        except FileNotFoundError:
            # Corresponding file doesn't exist, skip it completely
            continue

        sentence_pairs = [pair for pair in list(zip(type1_aligned_sentences, type2_aligned_sentences))
                          if (not training_only or pair[0].sentence.startswith("[TRAINING]"))
                          and not pair[1].sentence.startswith("[BAD]")  # Filter out "bad" sentences.
                          ]

        total_sentences += len(sentence_pairs)

        current_ious = [
            (intersection_over_union(pair[0].interval, pair[1].interval), pair[0].interval.get_length(),
             pair[1].interval.get_length(), pair[0].sentence, file_name) for pair in sentence_pairs
            if (pair[0].interval.get_length() > epsilon and pair[1].interval.get_length() > epsilon)
        ]

        current_google_confidence = [
            (pair[1].additional_data.google_confidence if pair[1].additional_data else 0.001) for pair in sentence_pairs
            if (pair[0].interval.get_length() > epsilon and pair[1].interval.get_length() > epsilon)
        ]

        current_sentence_scores = [
            (pair[1].additional_data.normalized_sentence_score if pair[1].additional_data else 0.001) for pair in sentence_pairs
            if (pair[0].interval.get_length() > epsilon and pair[1].interval.get_length() > epsilon)
        ]

        current_transcript_gaps = [
            (pair[1].additional_data.gaps_transcript if pair[1].additional_data else 0.001) for pair in sentence_pairs
            if (pair[0].interval.get_length() > epsilon and pair[1].interval.get_length() > epsilon)
        ]

        current_google_gaps = [
            (pair[1].additional_data.gaps_google if pair[1].additional_data else 0.001) for pair in sentence_pairs
            if (pair[0].interval.get_length() > epsilon and pair[1].interval.get_length() > epsilon)
        ]

        current_deviations = [
            pair[0].interval.get_deviation(pair[1].interval) for pair in sentence_pairs
            if (pair[0].interval.get_length() > epsilon and pair[1].interval.get_length() > epsilon)
        ]

        # Find sentences that are marked on either side as not appearing at all.
        pairs_sentence_not_appearing = [
            pair for pair in sentence_pairs if
            (pair[0].interval.get_length() <= epsilon or pair[1].interval.get_length() <= epsilon)
        ]

        # Count those sentences: which of those don't appear in both oder in either one?
        for pair in pairs_sentence_not_appearing:
            if not does_sentence_appear(pair[0], epsilon) and not does_sentence_appear(pair[1], epsilon):
                sentences_appearing_true_negatives += 1
            elif not does_sentence_appear(pair[0], epsilon) and does_sentence_appear(pair[1], epsilon):
                sentences_appearing_false_positives += 1
            elif does_sentence_appear(pair[0], epsilon) and not does_sentence_appear(pair[1], epsilon):
                sentences_appearing_false_negatives += 1

        # All sentences appearing in both are considered true negatives
        sentences_appearing_true_positives += len(current_ious)

        if len(current_ious) == 0:
            bin_print(verbosity, 2, "No sentences found, skipping...")
            continue

        if len(current_ious) > 0:
            mean_iou = np.mean([v[0] for v in current_ious])
            median_iou = np.median([v[0] for v in current_ious])
        else:
            mean_iou = np.nan
            median_iou = np.nan

        ious_per_file[file_name] = {
            "mean": mean_iou,
            "median": median_iou,
            "all": current_ious
        }

        if mean_iou <= 0.3:
            low_ious.append(file_name + ".wav")

        ious += current_ious
        google_confidences += current_google_confidence
        sentence_scores += current_sentence_scores
        deviations += current_deviations
        google_gaps += current_google_gaps
        transcript_gaps += current_transcript_gaps

    try:
        precision = sentences_appearing_true_positives / (
                    sentences_appearing_true_positives + sentences_appearing_false_positives)
    except ZeroDivisionError:
        precision = 0.0

    try:
        recall = sentences_appearing_true_positives / (
                    sentences_appearing_true_positives + sentences_appearing_false_negatives)
    except ZeroDivisionError:
        recall = 0.0

    try:
        f1_score = 2 * ((precision * recall) / (precision + recall))
    except ZeroDivisionError:
        f1_score = 0.0

    return {
        "no_sentences": {
            "appearing": len(ious),
            "total": total_sentences,
        },
        "ious": {
            "all": ious,
            "all_only": [iou[0] for iou in ious],
            "low": low_ious,
            "mean": np.mean([v[0] for v in ious]) if len(ious) > 0 else np.nan,
            "median": np.median([v[0] for v in ious]) if len(ious) > 0 else np.nan,
            "per_file": ious_per_file
        },
        "scores": {
            "deviation": {
                "all": deviations,
                "mean": np.mean(deviations) if len(deviations) > 0 else np.nan,
                "median": np.median(deviations) if len(deviations) > 0 else np.nan,
            },
            "google_confidence": {
                "all": google_confidences,
                "mean": np.mean(google_confidences) if len(google_confidences) > 0 else np.nan,
                "median": np.median(google_confidences) if len(google_confidences) > 0 else np.nan
            },
            "alignment_scores": {
                "all": sentence_scores,
                "mean": np.mean(sentence_scores) if len(sentence_scores) > 0 else np.nan,
                "median": np.median(sentence_scores) if len(sentence_scores) > 0 else np.nan
            },
            "google_gaps": {
                "all": google_gaps,
                "mean": np.mean(google_gaps) if len(google_gaps) > 0 else np.nan,
                "median": np.median(google_gaps) if len(google_gaps) > 0 else np.nan
            },
            "transcript_gaps": {
                "all": transcript_gaps,
                "mean": np.mean(transcript_gaps) if len(transcript_gaps) > 0 else np.nan,
                "median": np.median(transcript_gaps) if len(transcript_gaps) > 0 else np.nan
            },
            "calculated": {
                "all": [
                    calculate_overall_score(tuple[0], tuple[1], tuple[2], tuple[3],
                                            config["score_weights"]["gaps_google"],
                                            config["score_weights"]["gaps_transcript"],
                                            config["score_weights"]["alignment_score"],
                                            config["score_weights"]["google_confidence"],
                                            )
                    for tuple in zip(google_gaps, transcript_gaps, google_confidences, sentence_scores)
                ]
            }
        },
        "appearance": {
            "true_positives": sentences_appearing_true_positives,
            "false_positives": sentences_appearing_false_positives,
            "true_negatives": sentences_appearing_true_negatives,
            "false_negatives": sentences_appearing_false_negatives,
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
        }
    }


def does_sentence_appear(sentence: Sentence, epsilon: float) -> bool:
    """
    Checks if a sentence is marked as appearing

    :param sentence: The sentence under check
    :param epsilon:  Interval length epsilon to check

    :return: True if sentence exists, else false
    """
    if isinstance(sentence.interval.start, float) and isinstance(sentence.interval.end, float):
        return sentence.interval.get_length() > epsilon

    return sentence.interval.start != "-" and sentence.interval.end != "-"

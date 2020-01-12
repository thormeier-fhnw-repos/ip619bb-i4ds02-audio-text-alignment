from bin._bin import bin_print
from os import listdir
from os.path import isfile, join
from lib.src.align.compare.load_alignment import load_alignment
from typing import Dict, Any
import numpy as np


def fix_hand_alignments(input_path: str, fix_nonexisting: bool, reshuffle_training: bool, verbosity: int) -> None:
    """
    "Fixes" hand alignment by either reshuffling training or assigning some different
    :param input_path:         Where to find and write the data
    :param fix_nonexisting:    If nonexisting sentences should be makred with "-" instead
    :param reshuffle_training: If the training data should be reshuffled
    :param verbosity:          Verbosity of the output
    :return: None
    """
    bin_print(verbosity, 1, "Reading files from", input_path)

    bin_print(verbosity, 2, "Trying to find all .txt files...")
    txt_files = [input_path + f for f in listdir(input_path) if isfile(join(input_path, f)) and f.split(".")[1] == "txt"]
    bin_print(verbosity, 3, "Found txt files:", txt_files)

    bin_print(verbosity, 2, "Filtering found files by ones containing alignment by hand...")
    alignments = [f for f in txt_files if "audacity_hand" in f]
    bin_print(verbosity, 3, "Found txt files containing alingment by hand:", alignments)

    # Create random array of 1 and 0 to determine which sentences are part of training set.
    total_no_sentences = 1480
    testset_size = int(np.ceil(0.70 * total_no_sentences))
    positives = np.ones((testset_size,), dtype=int)
    negatives = np.zeros((total_no_sentences - testset_size,))
    testset_pattern = list(positives) + list(negatives)

    np.random.shuffle(testset_pattern)

    total = 0

    i = 0
    for file_name in alignments:
        bin_print(verbosity, 3, "Processing", file_name)
        sentences = load_alignment(file_name)

        total += len(sentences)

        for sentence in sentences:
            if fix_nonexisting:
                if sentence.interval.get_length() <= 0.01:
                    sentence.interval.start = "-"
                    sentence.interval.end = "-"

            if reshuffle_training:
                # Mark all as not training by default.
                sentence.sentence = sentence.sentence.replace("[TRAINING]", "")

                if testset_pattern[i] == 1:
                    sentence.sentence = "[TRAINING]"+sentence.sentence

            i += 1

        with open(file_name, "w+", encoding="utf-8") as f:
            f.write("\n".join([sentence.to_audacity_label_format().replace("\r\n", "").strip().encode("utf8", "replace").decode("utf8") for sentence in sentences]))
            bin_print(verbosity, 2, "Wrote " + file_name)
            f.close()

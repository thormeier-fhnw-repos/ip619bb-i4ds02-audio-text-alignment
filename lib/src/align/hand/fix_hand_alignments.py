from bin._bin import bin_print
from os import listdir
from os.path import isfile, join
from lib.src.align.compare.load_alignment import load_alignment
import numpy as np


def fix_hand_alignments(input_path: str, verbosity: int) -> None:
    """
    Moves non-existing sentences to beginning of file with length 0.0001
    :param input_path: Path to read files from
    :param verbosity: Verbosity
    :return: None
    """
    bin_print(verbosity, 1, "Reading files from", input_path)

    bin_print(verbosity, 2, "Trying to find all .txt files...")
    txt_files = [input_path + f for f in listdir(input_path) if isfile(join(input_path, f)) and f.split('.')[1] == "txt"]
    bin_print(verbosity, 3, "Found txt files:", txt_files)

    bin_print(verbosity, 2, "Filtering found files by ones containing alignment by hand...")
    alignments = [f for f in txt_files if "audacity_hand" in f]
    bin_print(verbosity, 3, "Found txt files containing alingment by hand:", alignments)

    # Create random array of 1 and 0 to determine which sentences are part of test set.
    total_no_sentences = 1480
    testset_size = int(np.ceil(0.70 * total_no_sentences))
    positives = np.ones((testset_size,), dtype=int)
    negatives = np.zeros((total_no_sentences - testset_size,))
    testset_pattern = list(positives) + list(negatives)

    np.random.shuffle(testset_pattern)

    print(testset_pattern, len(testset_pattern))

    total = 0

    i = 0
    for file_name in alignments:
        bin_print(verbosity, 3, "Processing", file_name)
        sentences = load_alignment(file_name)

        total += len(sentences)

        for sentence in sentences:
            if sentence.interval.get_length() <= 0.0001:
                sentence.interval.start = 0.0
                sentence.interval.end = 0.0001

            # Mark all as not test by default.
            sentence.sentence = sentence.sentence.replace('[TEST]', '')

            if testset_pattern[i] == 1:
                sentence.sentence = '[TEST]'+sentence.sentence

            print(testset_pattern[i])
            i += 1

        with open(file_name, "w+", encoding="utf-8") as f:
            f.write("\n".join([sentence.to_audacity_label_format().replace('\r\n', '').strip().encode('utf8', 'replace').decode('utf8') for sentence in sentences]))
            bin_print(verbosity, 2, "Wrote " + file_name)
            f.close()

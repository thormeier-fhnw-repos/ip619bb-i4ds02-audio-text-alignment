from lib.src.align.basic.create_basic_alignment import create_basic_alignment
from bin._bin import bin_print
from os import listdir
from os.path import isfile, join


def create_basic_alignments(input_path: str, output_path: str, verbosity: int) -> None:
    """
    Create basic alignments for all WAVE files in a given directory and write them to a given output directory.
    :param input_path: Path to load the WAVE files and transcript from
    :param output_path: Path to write the basic alignment to
    :param verbosity: Verbosity level
    :return: None
    """
    bin_print(verbosity, 1, "Reading files from", input_path)

    files = [f for f in listdir(input_path) if isfile(join(input_path, f)) and f.split('.')[1] == "wav"]
    bin_print(verbosity, 2, "WAVE files found:", "\n    -", "\n    - ".join(files))

    file_pairs = [(f, f + ".wav", f + ".txt") for f in [input_path + f.split('.')[0] for f in files]]

    for file_pair in file_pairs:
        bin_print(verbosity, 2, "Creating alignment for " + file_pair[0] + ".*")
        alignment = create_basic_alignment(file_pair[1], file_pair[2], verbosity)

        output_filename = file_pair[0] + "_audacity_basic.txt"
        with open(output_filename, "w+", encoding="utf-8") as f:
            f.write("\n".join([sentence.to_audacity_label_format() for sentence in alignment]))
            bin_print(verbosity, 2, "Wrote " + output_filename)
            f.close()

    bin_print(verbosity, 1, "Writing files to", output_path)





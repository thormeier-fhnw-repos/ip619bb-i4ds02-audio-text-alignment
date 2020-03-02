from typing import Type
from lib.src.align.aligner.AbstractAlignerStrategy import AbstractAlignerStrategy
from bin._bin import bin_print
from os import listdir
from os.path import isfile, join


class FilesAligner:
    """
    Base FilesAligner: Takes an arbitrary AbstractAlignerStrategy, that should not be google related.
    """

    def __init__(self, aligner: Type[AbstractAlignerStrategy], alignment_type: str):
        """
        Constructor
        :param aligner:        AbstractAlignerStrategy to use in order to create alignments
        :param alignment_type: Type of the alignment, used for naming files.
        """
        self.aligner = aligner
        self.alignment_type = alignment_type

    def align_files(self, input_path: str, output_path: str, verbosity: int) -> None:
        """
        Aligns all given files in input_path and writes alignments into output_path
        :param input_path:  Where to look for transcript files
        :param output_path: Where to write alignment files
        :param verbosity:   Verbosity of debugging output
        :return: None
        """
        bin_print(verbosity, 1, "Reading files from", input_path)

        files = [f for f in listdir(input_path) if isfile(join(input_path, f)) and f.split(".")[1] == "wav"]
        bin_print(verbosity, 2, "WAVE files found:", "\n    -", "\n    - ".join(files))

        file_pairs = [(f, f + ".txt", f + ".wav") for f in [input_path + f.split(".")[0] for f in files]]

        for file_pair in file_pairs:
            bin_print(verbosity, 2, "Creating alignment for " + file_pair[0] + ".*")
            alignment = self.aligner.align(file_pair[1], file_pair[2], verbosity)

            output_filename = file_pair[0] + "_audacity_" + self.alignment_type + ".txt"
            with open(output_filename, "w+", encoding="utf-8") as f:
                f.write("\n".join([sentence.to_audacity_label_format() for sentence in alignment]))
                bin_print(verbosity, 2, "Wrote " + output_filename)
                f.close()

        bin_print(verbosity, 1, "Writing files to", output_path)
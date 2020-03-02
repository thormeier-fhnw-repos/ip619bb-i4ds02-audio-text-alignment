from typing import Dict, Type, Any
from lib.src.align.aligner.FilesAligner import FilesAligner
from lib.src.align.aligner.google.AbstractGoogleAlignerStrategy import AbstractGoogleAlignerStrategy
from lib.src.model.Struct import Struct
from bin._bin import bin_print
from os import listdir
from os.path import isfile, join
from json import load
import numpy as np


class GoogleFilesAligner(FilesAligner):
    """
    Aligns files with Google output specifically
    """

    def __init__(self, aligner: Type[AbstractGoogleAlignerStrategy], alignment_parameters = Dict[str, Any]):
        """
        Constructor
        :param aligner: AbstractAlignerStrategy to use in order to create alignments
        :param alignment_parameters: Dict of parameters loaded from a given YAML file. See README.
        """
        super(GoogleFilesAligner, self).__init__(aligner, "google")
        self.aligner = aligner
        self.alignment_parameters = alignment_parameters

    def align_files(self, input_path: str, output_path: str, verbosity: int) -> None:
        """
        Aligns all given files in input_path and writes alignments into output_path
        :param input_path:           Where to look for transcript files
        :param output_path:          Where to write alignment files
        :param verbosity:            Verbosity of debugging output
        :return: None
        """
        bin_print(verbosity, 1, "Loading all transcript files from " + input_path + "...")
        file_names = [f.replace(".wav", "") for f in listdir(input_path) if
                      isfile(join(input_path, f)) and f.split(".")[1] == "wav"
                      # and (
                      #     f.startswith("podclub") or f.startswith("stadt_zuerich")
                      # )
                      ]

        bin_print(verbosity, 3, "Found files:", file_names)

        for file in file_names:
            bin_print(verbosity, 2, "Aligning " + file + "...")
            transcript_file = file + ".txt"

            with open(join(input_path, transcript_file), encoding="utf-8-sig") as read_file:
                transcript = read_file.read()

            with open(join(input_path, file + "_google_output.json"), "r", encoding="utf-8-sig") as read_file:
                # Convert back to object-like structure, so the underlying
                # alignment function doesn't imply non-object like structures,
                # such as dicts. This is particularly useful when working with
                # Googles output directly.
                google_output = load(read_file)
                google_output = Struct(**google_output)
                google_output.results = [Struct(**r) for r in google_output.results]

            alignment = self.aligner.align(google_output, transcript, verbosity, self.alignment_parameters)

            output_filename = output_path + "/" + file + "_audacity_" + self.alignment_type + ".txt"
            with open(output_filename, "w+", encoding="utf-8") as f:
                f.write("\n".join([sentence.to_audacity_label_format() for sentence in alignment]))
                bin_print(verbosity, 2, "Wrote " + output_filename)
                f.close()

        bin_print(verbosity, 0, "Execution time per sentence (mean): ", (np.mean(self.aligner.execution_times) + np.mean(self.aligner.alignment_times)))
        bin_print(verbosity, 0, "Execution time per sentence (max):  ", (np.max(self.aligner.execution_times) + np.max(self.aligner.alignment_times)))

from bin._bin import bin_print
from os import listdir
from os.path import isfile, join
from json import load
from lib.src.model.Struct import Struct
from lib.src.align.google.create_google_alignment_global import create_google_alignment_global
from lib.src.align.google.create_google_alignment_global_character import create_google_alignment_global_character
from lib.src.align.google.create_google_alignment_semiglobal_character import create_google_alignment_semiglobal_character
from lib.src.align.google.create_google_alignment_local_character import create_google_alignment_local_character
from lib.src.align.google.create_google_alignment_local import create_google_alignment_local
from lib.src.align.google.create_google_alignment_semiglobal import create_google_alignment_semiglobal
from lib.src.align.google.create_google_alignment_biopython import create_google_alignment_biopython


# @profile
def create_google_alignments(input_path: str, output_path: str, verbosity: int) -> None:
    """
    Aligns all outputs of Google STT API with their given transcripts.
    :param input_path:
    :param output_path:
    :param verbosity:
    :return:
    """

    bin_print(verbosity, 1, "Loading all transcript files from " + input_path + "...")
    file_names = [f.replace(".wav", "") for f in listdir(input_path) if isfile(join(input_path, f)) and f.split('.')[1] == "wav"] # and f == 'gemeinde_wettingen_3.wav'] # and f in ['gemeinde_wettingen_12.wav', 'gemeinde_wettingen_16.wav', 'gemeinde_wettingen_17.wav', 'gemeinde_wettingen_19.wav', 'gemeinde_wettingen_1.wav', 'gemeinde_wettingen_20.wav', 'gemeinde_wettingen_21.wav', 'gemeinde_wettingen_22.wav', 'gemeinde_wettingen_23.wav', 'gemeinde_wettingen_24.wav', 'gemeinde_wettingen_26.wav', 'gemeinde_wettingen_28.wav', 'gemeinde_wettingen_3.wav', 'gemeinde_wettingen_4.wav', 'gemeinde_wettingen_5.wav', 'gemeinde_wettingen_6.wav', 'gemeinde_wettingen_7.wav', 'kanton_ar_kantonsrat_11.wav', 'kanton_ar_kantonsrat_7.wav', 'kanton_ar_kantonsrat_8.wav', 'kanton_ow_kantonsrat_12.wav', 'kanton_ow_kantonsrat_14.wav', 'kanton_ow_kantonsrat_16.wav', 'kanton_ow_kantonsrat_17.wav', 'kanton_ow_kantonsrat_4.wav', 'kanton_ow_kantonsrat_7.wav', 'kanton_ow_kantonsrat_8.wav', 'stadt_zuerich_gemeinderat_10.wav', 'stadt_zuerich_gemeinderat_13.wav', 'stadt_zuerich_gemeinderat_15.wav', 'stadt_zuerich_gemeinderat_17.wav', 'stadt_zuerich_gemeinderat_18.wav', 'stadt_zuerich_gemeinderat_19.wav', 'stadt_zuerich_gemeinderat_1.wav', 'stadt_zuerich_gemeinderat_3.wav', 'stadt_zuerich_gemeinderat_4.wav', 'stadt_zuerich_gemeinderat_5.wav', 'stadt_zuerich_gemeinderat_6.wav']]

    transcript_filenames = [f + ".txt" for f in file_names]
    google_output_filenames = [f + "_google_output.json" for f in file_names]

    bin_print(verbosity, 3, "Found files:", file_names)

    for file in file_names:
        bin_print(verbosity, 2, "Aligning " + file + "...")
        transcript_file = file + ".txt"

        with open(join(input_path, transcript_file), encoding='utf-8-sig') as read_file:
            transcript = read_file.read()

        with open(join(input_path, file + "_google_output.json"), "r", encoding='utf-8-sig') as read_file:
            # Convert back to object-like structure, so the underlying
            # alignment function doesn't imply non-object like structures,
            # such as dicts. This is particularly useful when working with
            # Googles output directly.
            google_output = load(read_file)
            google_output = Struct(**google_output)
            google_output.results = [Struct(**r) for r in google_output.results]

        alignment = create_google_alignment_semiglobal_character(google_output, transcript, verbosity)

        output_filename = output_path + "/" + file + "_audacity_google.txt"
        with open(output_filename, "w+", encoding="utf-8") as f:
            f.write("\n".join([sentence.to_audacity_label_format() for sentence in alignment]))
            bin_print(verbosity, 2, "Wrote " + output_filename)
            f.close()

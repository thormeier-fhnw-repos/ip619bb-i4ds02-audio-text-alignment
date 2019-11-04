from bin._bin import bin_print
from os import listdir
from os.path import isfile, join
from google.cloud import speech
from lib.src.align.google.get_raw import get_raw
from google.api_core.future.polling import _OperationNotComplete


def get_and_save_raw(input_path: str, bucket_name: str, out_path: str, verbosity: int) -> None:
    """
    Gets raw JSON from Google Cloud Speech-to-text API
    :param input_path: str Path to read files from
    :param bucket_name: str Name of the GCS bucket
    :param verbosity: int Verbosity level
    :return:
    """

    bin_print(verbosity, 1, "Reading files from", input_path)

    bin_print(verbosity, 2, "Trying to find all .flac files...")
    flac_files = [f for f in listdir(input_path) if isfile(join(input_path, f)) and f.split('.')[1] == "flac"]
    bin_print(verbosity, 3, "Found flac files:", flac_files)
    bin_print(verbosity, 3, "Total flac files:", len(flac_files))

    client = speech.SpeechClient()

    bin_print(verbosity, 1, "Running Google STT...")
    for flac_file in flac_files:
        if "stadt_zuerich" in flac_file:
            bin_print(verbosity, 2, "Processing " + flac_file)
            try:
                json = get_raw("gs://" + bucket_name + "/" + flac_file, client)
                json_path = out_path + "/" + flac_file.replace('.flac', '_google_output') + ".json"
                bin_print(verbosity, 2, "Writing " + json_path)
                f = open(json_path, "w")
                f.write(json)
                f.close()
            except _OperationNotComplete:
                bin_print(verbosity, 1, "Timeout for " + flac_file)
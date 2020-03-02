from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.protobuf.json_format import MessageToJson


def get_raw(file_name: str, client: speech.SpeechClient) -> str:
    """
    Get the raw Speech to text result from Google Cloud API
    :param file_name: str File name + path
    :param client: speech.SpeechClient Google Cloud API Speech client
    :return: str JSON encoded response
    """

    audio = types.RecognitionAudio(uri=file_name)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code="de-DE",
        enable_word_time_offsets=True
    )

    operation = client.long_running_recognize(config, audio)

    response = operation.result(timeout=900)

    return MessageToJson(response)

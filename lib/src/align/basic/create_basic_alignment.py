from pydub import AudioSegment
from lib.src.model.transform.transcript_to_sentences import transcricpt_to_sentences
import time
from bin._bin import bin_print


def create_basic_alignment(path_to_wav: str, path_to_transcript: str, verbosity: int) -> None:
    """
    Creates a basic alignment
    :param path_to_wav: Path to WAV file to create an alignment for
    :param path_to_transcript: Path to transcript
    :param verbosity: Verbosity level
    :return: None
    """
    start_time = time.time()
    audio_segment = AudioSegment.from_wav(path_to_wav)
    duration = audio_segment.duration_seconds

    with open(path_to_transcript, encoding='utf-8') as f:
        transcript = f.read()
    transcript = transcript.replace('\n', ' ')

    sentences = transcricpt_to_sentences(transcript)

    number_of_chars_total = sum([len(sentence.sentence) for sentence in sentences])

    start = 0.0
    for sentence in sentences:
        end = start + len(sentence.sentence) / number_of_chars_total * duration
        sentence.interval.start = start
        sentence.interval.end = end
        start = end
    end_time = time.time()

    bin_print(verbosity, 2, "Time elapsed for", path_to_wav, ":", (end_time - start_time))

    return sentences

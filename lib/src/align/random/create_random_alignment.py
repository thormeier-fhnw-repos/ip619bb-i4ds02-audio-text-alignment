from pydub import AudioSegment
from lib.src.model.transform.transcript_to_sentences import transcricpt_to_sentences
import time
from bin._bin import bin_print
import random


def create_random_alignment(path_to_wav: str, path_to_transcript: str, verbosity: int) -> None:
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

    precision = 1_000_000
    borders = random.sample(range(0, precision), len(sentences) * 2)
    borders.sort()
    borders = [border / precision * duration for border in borders]

    bin_print(verbosity, 3, "Borders for", path_to_wav, "are", borders)

    index = 0
    for sentence in sentences:
        sentence.interval.start = borders[index]
        sentence.interval.end = borders[index + 1]
        index += 2

    end_time = time.time()

    bin_print(verbosity, 2, "Time elapsed for", path_to_wav, ":", (end_time - start_time))

    return sentences

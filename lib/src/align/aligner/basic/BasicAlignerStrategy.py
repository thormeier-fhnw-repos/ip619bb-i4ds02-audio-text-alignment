from typing import List
from lib.src.align.aligner.AbstractAlignerStrategy import AbstractAlignerStrategy
from lib.src.align.utils.transcript_to_sentences import transcript_to_sentences
from lib.src.model.Sentence import Sentence
from pydub import AudioSegment
import time
from bin._bin import bin_print


class BasicAlignerStrategy(AbstractAlignerStrategy):
    """
    Basic alignment based on sentence length.
    """
    @staticmethod
    def perform_alignment(transcript: str, wav_path: str, verbosity: int) -> List[Sentence]:
        start_time = time.time()
        audio_segment = AudioSegment.from_wav(wav_path)
        duration = audio_segment.duration_seconds

        with open(transcript, encoding="utf-8") as f:
            transcript = f.read()
        transcript = transcript.replace("\n", " ")

        sentences = transcript_to_sentences(transcript)

        number_of_chars_total = sum([len(sentence.sentence) for sentence in sentences])

        start = 0.0
        for sentence in sentences:
            end = start + len(sentence.sentence) / number_of_chars_total * duration
            sentence.interval.start = start
            sentence.interval.end = end
            start = end
        end_time = time.time()

        bin_print(verbosity, 2, "Time elapsed for", wav_path, ":", (end_time - start_time))

        return sentences

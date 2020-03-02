from typing import List
from lib.src.align.aligner.AbstractAlignerStrategy import AbstractAlignerStrategy
from lib.src.align.utils.transcript_to_sentences import transcript_to_sentences
from lib.src.model.Sentence import Sentence
from pydub import AudioSegment
import time
from bin._bin import bin_print
import random


class RandomAlignerStrategy(AbstractAlignerStrategy):
    """
    Random alignment
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

        precision = 1_000_000
        borders = random.sample(range(0, precision), len(sentences) * 2)
        borders.sort()
        borders = [border / precision * duration for border in borders]

        bin_print(verbosity, 3, "Borders for", wav_path, "are", borders)

        index = 0
        for sentence in sentences:
            sentence.interval.start = borders[index]
            sentence.interval.end = borders[index + 1]
            index += 2

        end_time = time.time()

        bin_print(verbosity, 2, "Time elapsed for", wav_path, ":", (end_time - start_time))

        return sentences
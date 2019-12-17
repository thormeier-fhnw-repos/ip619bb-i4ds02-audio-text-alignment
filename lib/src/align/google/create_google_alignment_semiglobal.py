from typing import List
from lib.src.model.Sentence import Sentence
from lib.src.model.transform.transcript_to_sentences import transcricpt_to_sentences
from lib.src.align.similarity.bag_distance_similarity import bag_distance_similarity
from bin._bin import bin_print
from nltk.tokenize import word_tokenize
from lib.src.align.sequence_alignment.needleman_wunsch import needleman_wunsch
from lib.src.align.sequence_alignment.smith_waterman import smith_waterman
from lib.src.align.sequence_alignment.semi_global import semi_global
from lib.src.align.debugging.prettify_alignment import prettify_alignment
from lib.src.align.google.preprocess_string import preprocess_string
from lib.src.align.google.get_sentence_confidence import get_sentence_confidence
from num2words import num2words
from string import punctuation
from nltk.metrics.distance import edit_distance
import re


def create_google_alignment_semiglobal(google_output: object, transcript: str, verbosity: int) -> List[Sentence]:
    """
    Aligns the output of Googles STT api with a given transcript
    :param google_output: Dict/Object of the Google Output
    :param transcript: The gioven transcript, as full text
    :param verbosity: Verbosity of debugging output
    :return: List of aligned sentences
    """

    # Some pre-processing: Create sentence objects of transcript, so we can align those later on.
    transcript = transcript.replace('\n', ' ')
    sentences = transcricpt_to_sentences(transcript)

    base_confidences = [r.alternatives[0]["confidence"] for r in google_output.results]
    bin_print(verbosity, 2, "Confidences of all results:", base_confidences)

    google_words = [{'word': preprocess_string(w["word"]), "startTime": w["startTime"], "endTime": w["endTime"]} for w in sum([r.alternatives[0]["words"] for r in google_output.results], [])]

    google_word_list = [w["word"] for w in google_words]
    transcript_word_list = [preprocess_string(w) for w in word_tokenize(transcript, 'german') if not all(c in punctuation for c in w)] # Filter out all punctuation "words"

    def compare(a: str, b: str) -> bool:
        """
        Uses a string similarity function to determine if a match was made
        :param a: String to compare
        :param b: String to compare
        :return: True if a certain similarity threshold was reached
        """
        if b.isdigit():
            b = num2words(b, lang='de')

        if a["word"].isdigit():
            a["word"] = num2words(a["word"], lang='de')

        return bag_distance_similarity(a["word"], b) >= 0.6

    def is_mostly_none(l: List) -> bool:
        """
        Determines if a a given list consists of mostly gaps.
        :param l: List of aligned words
        :return: True if threshold is reached
        """
        return len(l) == 0 or (l.count(None)) / len(l) > 0.8

    alignment = semi_global(google_words, transcript_word_list, 5, -1, -1, compare)
    google_alignment = alignment[0]
    transcript_alignment = alignment[1]

    bin_print(verbosity, 3, "Alignment:", prettify_alignment([w["word"] if w is not None else None for w in google_alignment], transcript_alignment))

    # Assign start and end times to sentences
    last_end_time = 0.0
    for sentence in sentences:
        sentence_words = [preprocess_string(w) for w in word_tokenize(sentence.sentence, 'german') if not all(c in punctuation for c in w)]

        transcript_start_word = sentence_words[0]
        transcript_end_word = sentence_words[-1]

        start_word_index = transcript_alignment.index(transcript_start_word)
        end_word_index = transcript_alignment.index(transcript_end_word)

        if is_mostly_none(google_alignment[start_word_index:end_word_index]):
            sentence.interval.start = 0.0
            sentence.interval.end = 0.0001
            last_end_time = sentence.interval.end
            continue

        lookup_threshold = 3

        google_start_word = None
        lookup_position = 0
        while True:
            google_start_word = google_alignment[start_word_index + lookup_position if start_word_index + lookup_position > 0 else 0]
            if google_start_word is not None or lookup_position == lookup_threshold:
                break

            # Shift forward or backward: index +1, -1, +2, -2 etc. ensuring we get the next best match.
            lookup_position *= -1

            if lookup_position >= 0:
                lookup_position += 1

        # Same for the end word
        google_end_word = None
        lookup_position = 0
        while True:
            google_end_word = google_alignment[end_word_index + lookup_position if (end_word_index + lookup_position < (len(google_alignment) - 1)) else len(google_alignment) - 1]
            if google_end_word is not None or lookup_position == lookup_threshold:
                break

            lookup_position *= -1

            if lookup_position >= 0:
                lookup_position += 1

        if google_start_word is None:
            sentence.interval.start = last_end_time
        else:
            sentence.interval.start = float(google_start_word["startTime"].replace('s', ''))

        if google_end_word is None:
            if google_start_word is None:
                sentence.interval.start = 0.0
                sentence.interval.end = 0.0001
            else:
                sentence.interval.end = sentence.interval.start + 0.0001
        else:
            sentence.interval.end = float(google_end_word["endTime"].replace('s', ''))

        last_end_time = sentence.interval.end

    return sentences

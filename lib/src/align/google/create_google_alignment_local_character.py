from typing import List
from lib.src.model.Sentence import Sentence
from lib.src.model.transform.transcript_to_sentences import transcricpt_to_sentences
from lib.src.align.similarity.bag_distance_similarity import bag_distance_similarity
from bin._bin import bin_print
from nltk.tokenize import word_tokenize
from lib.src.align.sequence_alignment.needleman_wunsch import needleman_wunsch
from lib.src.align.sequence_alignment.semi_global import semi_global
from lib.src.align.sequence_alignment.smith_waterman import smith_waterman
from lib.src.align.debugging.prettify_alignment import prettify_alignment
from lib.src.align.google.preprocess_string import preprocess_string
from string import punctuation
from nltk.metrics.distance import edit_distance
from num2words import num2words
import re


def create_google_alignment_local_character(google_output: object, transcript: str, verbosity: int) -> List[Sentence]:
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

    google_words = sum([r.alternatives[0]["words"] for r in google_output.results], [])
    google_word_list = [w["word"] for w in google_words]
    google_character_list = list(preprocess_string(' '.join(google_word_list)))

    transcript_word_list = [w for w in word_tokenize(transcript, 'german') if not all(c in punctuation for c in w)] # Filter out all punctuation "words"
    transcript_character_list = list(preprocess_string(' '.join(transcript_word_list)))

    def compare(a: str, b: str) -> bool:
        """
        Uses a string similarity function to determine if a match was made
        :param a: String to compare
        :param b: String to compare
        :return: Equality of strings
        """
        return a == b

    bin_print(verbosity, 0, 'Start')
    alignment = smith_waterman(google_character_list, transcript_character_list, 5, -1, -1, compare)
    bin_print(verbosity, 0, 'End')

    google_alignment = ''.join([c if c is not None else '-' for c in alignment[0]])
    transcript_alignment = ''.join([c if c is not None else '-' for c in alignment[1]])

    #bin_print(verbosity, 3, prettify_alignment(list(google_alignment), list(transcript_alignment)))

    def is_mostly_none(l: List) -> bool:
        """
        Determines if a a given list consists of mostly gaps.
        :param l: List of aligned words
        :return: True if threshold is reached
        """
        return len(l) == 0 or (l.count('-')) / len(l) > 0.8

    # Assign start and end times to sentences
    last_end_point = 0
    last_end_time = 0.0

    for sentence in sentences:
        sentence_words = ' '.join([w for w in word_tokenize(sentence.sentence, 'german') if not all(c in punctuation for c in w)])
        sentence_characters = list(preprocess_string(sentence_words))

        regex_required_start = round(len(sentence_characters) * 0.2)
        regex_required_end = round(len(sentence_characters) * 0.8)

        sentence_regex = \
            '?-*'.join(sentence_characters[0:regex_required_start]) + \
            '-*'.join(sentence_characters[regex_required_start + 1:regex_required_end]) + \
            '?-*'.join(sentence_characters[regex_required_end + 1:len(sentence_characters) - 1]) + '?'

        try:
            alignment_match = re.search(sentence_regex, transcript_alignment[last_end_point:])

            alignment_start_point = last_end_point + alignment_match.start()
            alignment_end_point = last_end_point + alignment_match.end()

            last_end_point = last_end_point + alignment_match.end()
        except AttributeError:
            print('nope 1')
            sentence.interval.start = 0.0
            sentence.interval.end = 0.0001
            continue

        # Mostly none values on either side indicates a false positive, move to beginning of sentence with
        if is_mostly_none(google_alignment[alignment_start_point:alignment_end_point]) \
                or is_mostly_none(transcript_alignment[alignment_start_point:alignment_end_point]):
            print('nope 2')
            sentence.interval.start = 0.0
            sentence.interval.end = 0.0001
            continue

        google_sub_start = len([c for c in google_alignment[0:alignment_start_point] if c is not '-' and c is not ' '])
        google_sub_end = len([c for c in google_alignment[0:alignment_end_point] if c is not '-' and c is not ' '])

        character_count = 0
        found_start = False

        startWord = None
        endWord = None

        for word in google_words:
            character_count += len(preprocess_string(word["word"]))
            word_start_time = float(word["startTime"].replace('s', ''))

            # Guarantee that there's no overlapping sentences
            if character_count >= google_sub_start and last_end_time <= word_start_time and not found_start:
                sentence.interval.start = word_start_time
                startWord = word["word"]
                found_start = True

            if found_start and character_count >= google_sub_end:
                sentence.interval.end = float(word["endTime"].replace('s', ''))
                last_end_time = sentence.interval.end
                endWord = word["word"]
                break

    return sentences

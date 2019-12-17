# -*- coding: utf-8 -*-

from typing import List
from lib.src.model.Sentence import Sentence
from lib.src.model.transform.transcript_to_sentences import transcricpt_to_sentences
from lib.src.align.similarity.bag_distance_similarity import bag_distance_similarity
from bin._bin import bin_print
from nltk.tokenize import word_tokenize
from lib.src.align.sequence_alignment.needleman_wunsch import needleman_wunsch
from lib.src.align.sequence_alignment.smith_waterman import smith_waterman
from lib.src.align.debugging.prettify_alignment import prettify_alignment
from string import punctuation
from nltk.metrics.distance import edit_distance
from num2words import num2words
import re
import string
from Bio import pairwise2
from Bio import Align
import faulthandler; faulthandler.enable()


def preprocess_string(input: str) -> str:
    """
    Preprocesses a given string to be fit for alignment.
    :param input: String to process
    :return: Processed string
    """
    input = input.replace('ä', 'ae')
    input = input.replace('ö', 'oe')
    input = input.replace('ü', 'ue')
    input = input.replace('Ä', 'Ae')
    input = input.replace('Ö', 'Oe')
    input = input.replace('Ü', 'Ue')
    input = input.replace('*', '')
    input = ''.join([c for c in list(input) if c not in punctuation])
    input = input.encode('ascii', 'ignore')

    return str(input).replace("b'", '').replace("'", '').lower()


def create_google_alignment_biopython(google_output: object, transcript: str, verbosity: int) -> List[Sentence]:
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
    google_word_list = [w["word"] for w in google_words if not all(c in punctuation for c in w["word"])]
    google_text = preprocess_string(' '.join(google_word_list))

    transcript_text = ' '.join([w for w in word_tokenize(transcript, 'german') if not all(c in punctuation for c in w)]) # Filter out all punctuation "words"
    transcript_text = ''.join([c for c in list(transcript_text) if c not in punctuation])
    transcript_text = preprocess_string(transcript_text)
    bin_print(verbosity, 3, transcript_text)

    alignments = pairwise2.align.localms(google_text, transcript_text, 5, -1, -1, -1,
                                          penalize_end_gaps=(True, True),
                                          one_alignment_only=True,
                                          )

    alignment = alignments[0]

    google_alignment = alignment[0]
    transcript_alignment = alignment[1]

    bin_print(verbosity, 3, prettify_alignment(google_alignment, transcript_alignment))

    def is_mostly_none(l: List) -> bool:
        """
        Determines if a a given list consists of mostly gaps.
        :param l: List of aligned words
        :return: True if threshold is reached
        """
        return len(l) == 0 or (l.count('-')) / len(l) > 0.8

    # Assign start and end times to sentences
    last_end_time = 0.0
    # Assign start and end times to sentences
    last_end_point = 0
    last_end_time = 0.0

    for sentence in sentences:
        sentence_words = ' '.join([w for w in word_tokenize(sentence.sentence, 'german') if not all(c in punctuation for c in w)])
        sentence_characters = list(preprocess_string(sentence_words))

        sentence_regex = '-*'.join(sentence_characters)

        try:
            alignment_match = re.search(sentence_regex, transcript_alignment[last_end_point:])

            alignment_start_point = last_end_point + alignment_match.start()
            alignment_end_point = last_end_point + alignment_match.end()

            last_end_point = last_end_point + alignment_match.end()
        except AttributeError:
            # _Shouldn't_ happen, as the regexp is basically part of the transcript we're
            # looking at. Character's don't vanish from the transcript, so there's always a match.
            sentence.interval.start = 0.0
            sentence.interval.end = 0.0001
            continue

        # Mostly none values on either side indicates a false positive, move to beginning of sentence with
        if is_mostly_none(google_alignment[alignment_start_point:alignment_end_point]) \
                or is_mostly_none(transcript_alignment[alignment_start_point:alignment_end_point]):
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

    # offset = 0
    # last_end_time = 0
    # for sentence in sentences:
    #     alignment_left = transcript_alignment[offset:]
    #
    #     # if sentence.sentence == 'Doch als sie den Teufel sahen, erschraken sie und fragen: "Was willst Du von uns?"':
    #     #     debug = True
    #     # else:
    #     #     debug = False
    #
    #     # Figure out start and end word of the current sentence.
    #     # Those need to be aligned with the Google transcript
    #     sentence_words = [w for w in word_tokenize(sentence.sentence, 'german') if not all(c in punctuation for c in w)]
    #     transcript_start_word = sentence_words[0]
    #     transcript_end_word = sentence_words[-1]
    #
    #     # if debug:
    #     #     print(transcript_start_word, transcript_end_word, alignment_left)
    #
    #     # Define global indices of the start and end words in the alignment
    #     start_word_index = alignment_left.index(transcript_start_word) + offset
    #     end_word_index = alignment_left.index(transcript_end_word) + offset
    #
    #     # if debug:
    #     #     print(start_word_index, end_word_index, is_mostly_none(google_alignment[start_word_index:end_word_index]))
    #
    #     # Only consider a matched sentence if the match is less than 50% None values
    #     # OR: If the sentence in the aligned transcript is mostly None (>50% Nones), it's likely misaligned, skip.
    #     if is_mostly_none(google_alignment[start_word_index:end_word_index]): # or is_mostly_none(transcript_alignment[start_word_index:end_word_index]):
    #         sentence.interval.start = last_end_time
    #         sentence.interval.end = last_end_time + 0.0001
    #         offset = end_word_index
    #         last_end_time = sentence.interval.end
    #         continue
    #
    #     # Maximum of 3 before and 3 after will be considered.
    #     lookup_threshold = 5
    #
    #     # We start of not knowing which word is aligned
    #     google_start_word = None
    #     lookup_position = 0
    #     while True:
    #         google_start_word = google_alignment[start_word_index + lookup_position if start_word_index + lookup_position > 0 else 0]
    #         if google_start_word is not None or lookup_position == lookup_threshold:
    #             break
    #
    #         # Shift forward or backward: index +1, -1, +2, -2 etc. ensuring we get the next best match.
    #         lookup_position *= -1
    #
    #         if lookup_position >= 0:
    #             lookup_position += 1
    #
    #     # Same for the end word
    #     google_end_word = None
    #     lookup_position = 0
    #     while True:
    #         google_end_word = google_alignment[end_word_index + lookup_position if (end_word_index + lookup_position < (len(google_alignment) - 1)) else len(google_alignment) - 1]
    #         if google_end_word is not None or lookup_position == lookup_threshold:
    #             break
    #
    #         lookup_position *= -1
    #
    #         if lookup_position >= 0:
    #             lookup_position += 1
    #
    #     # if debug:
    #     #     print(google_start_word)
    #     #     print(google_end_word)
    #
    #     if google_start_word is None:
    #         sentence.interval.start = last_end_time
    #     else:
    #         sentence.interval.start = float(google_start_word["startTime"].replace('s', ''))
    #
    #     if google_end_word is None:
    #         if google_start_word is None:
    #             sentence.interval.end = last_end_time + 0.0001
    #         else:
    #             sentence.interval.end = sentence.interval.start + 0.0001
    #     else:
    #         sentence.interval.end = float(google_end_word["endTime"].replace('s', ''))
    #
    #     offset = end_word_index
    #     last_end_time = sentence.interval.end
    #
    # return sentences

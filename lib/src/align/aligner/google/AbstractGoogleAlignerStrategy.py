import abc
from lib.src.align.aligner.AbstractAlignerStrategy import AbstractAlignerStrategy
from bin._bin import bin_print
from typing import List, Dict, Any
from string import punctuation
from lib.src.model.Sentence import Sentence
from lib.src.align.utils.preprocess_string import preprocess_string
from lib.src.align.utils.transcript_to_sentences import transcript_to_sentences
from lib.src.align.utils.prettify_alignment import prettify_alignment
from lib.src.align.utils.get_sentence_confidence import get_sentence_confidence
from lib.src.align.utils.is_mostly_none import is_mostly_none
from lib.src.align.utils.get_none_part import get_none_part
from lib.src.align.utils.calculate_overall_score import calculate_overall_score
import re
from lib.src.model.AdditionalData import AdditionalData
from memory_profiler import profile
from time import time
import numpy as np


class AbstractGoogleAlignerStrategy(AbstractAlignerStrategy):
    """
    Abstract base class to allow typehinting.
    """

    @staticmethod
    @abc.abstractmethod
    @profile
    def perform_alignment(transcript: str, google_output: object, verbosity: int,
                          alignment_parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aligns a given transcript to a given wav
        :param transcript:           The transcript as string
        :param google_output:        Google's general output as JSON object
        :param verbosity:            Verbosity of the output
        :param alignment_parameters: Dict of parameters loaded from a given YAML file. See README for full config.
        :return: List of aligned Sentences
        """""
        pass

    @classmethod
    def align(cls, google_output: object, transcript: str, verbosity: int,
              alignment_parameters: Dict[str, Any]) -> List[Sentence]:
        """
        Adjusted way of actually aligning with Google output.
        :param transcript:           Transcript as string
        :param google_output:        Google output as JSON object
        :param verbosity:            Verbosity of output
        :param alignment_parameters: Dict of parameters loaded from a given YAML file. See README for full config.
        :return: List of aligned sentences
        """
        sentences = cls.get_sentences(transcript)
        transcript_text = cls.get_transcript_text(transcript)

        google_words = cls.get_google_words(google_output)
        google_text = cls.get_google_text(google_words)

        base_confidences = [r.alternatives[0]["confidence"] for r in google_output.results]
        bin_print(verbosity, 2, "Confidences of all results:", base_confidences)

        bin_print(verbosity, 3, "Preprocessed transcript text:", transcript_text)
        bin_print(verbosity, 3, "Preprocessed google text:", google_text)

        # Call actual implementation of the alignment.
        alignment = cls.perform_alignment(transcript_text, google_text, verbosity, alignment_parameters)

        google_alignment = alignment["google"]
        transcript_alignment = alignment["transcript"]
        alignment_score = alignment["score"]

        bin_print(verbosity, 3, prettify_alignment(google_alignment, transcript_alignment))

        return cls.align_per_sentence(sentences, transcript_alignment, google_alignment,
                           google_words, alignment_parameters, alignment_score, verbosity)

    @staticmethod
    def get_google_words(google_output: object) -> List[dict]:
        """
        Preprocesses the Google output to further work with it.
        :param google_output: JSON object
        :return: List of dict for all words in a google_output.
        """
        words = []
        for result in google_output.results:
            alternative = result.alternatives[0]
            for word in alternative["words"]:
                words.append({
                    "word": preprocess_string(word["word"]),
                    "startTime": word["startTime"],
                    "endTime": word["endTime"],
                    "confidence": alternative["confidence"]
                })

        return words

    @staticmethod
    def get_sentences(transcript: str) -> List[Sentence]:
        """
        Create a list of Sentence objects from a given transcript
        :param transcript: Transcript as string
        :return: List of Sentence instances
        """
        return transcript_to_sentences(transcript.replace('\n', ' '))

    @staticmethod
    def get_google_text(google_words: List) -> str:
        """
        Get a complete text out of Google output.
        :param google_words: List of Google output words, straight from JSON object.
        :return: Google output as string
        """
        google_word_list = [w["word"] for w in google_words if not all(c in punctuation for c in w["word"])]
        return preprocess_string(' '.join(google_word_list))

    @staticmethod
    def get_transcript_text(transcript: str) -> str:
        """
        Get preprocessed transcript as string
        :param transcript: Transcript string
        :return: Preprocessed transcript
        """
        return preprocess_string(transcript)



    @staticmethod
    def mark_sentence_not_appearing(sentence: Sentence, alignment_parameters: Dict[str, Any],
                                    last_end_time: float) -> None:
        """
        Mark a sentence as "no appearing"
        :param sentence:             Sentence to mark
        :param alignment_parameters: Dict of parameters loaded from a given YAML file. See README for full config.
        :param last_end_time:        Last end time that has been assigned to a given sentence
        :return: None
        """
        if alignment_parameters["no_appearance"]["type"] == "time":
            sentence.interval.start = last_end_time
            sentence.interval.end = last_end_time + alignment_parameters["no_appearance"]["interval_length"]
        else:
            sentence.interval.start = "-"
            sentence.interval.end = "-"


    @classmethod
    def align_per_sentence(cls, sentences: List[Sentence], transcript_alignment: str, google_alignment: str,
                           google_words: List[object], alignment_parameters: Dict[str, Any], alignment_score: int, verbosity: int) -> List[Sentence]:
        """
        Assigns start and end times to sentences based on given alignments.
        :param sentences:            All sentences
        :param transcript_alignment: Aligned transcript
        :param google_alignment:     Aligned google output
        :param google_words:         Google words, to get startTime and endTime
        :param alignment_parameters: Dict of parameters loaded from a given YAML file. See README for full config.
        :param alignment_score:      Score of the alignment
        :param verbosity:            Verbosity of output
        :return: None
        """
        last_end_point = 0
        last_end_time = 0.0

        sentence_index = 0

        track_time = alignment_parameters["benchmark"]["exec_time"]
        execution_times = []

        for sentence in sentences:
            start_time = time()

            sentence_characters = list(preprocess_string(sentence.sentence))

            sentence_regex = '-*'.join(sentence_characters)

            try:
                alignment_match = re.search(sentence_regex, transcript_alignment[last_end_point:])

                alignment_start_point = last_end_point + alignment_match.start()
                alignment_end_point = last_end_point + alignment_match.end()

                last_end_point = last_end_point + alignment_match.end()
            except AttributeError as e:
                bin_print(0, 0, "--------------------------------------------------------------------------")
                bin_print(0, 0, transcript_alignment[last_end_point:])
                bin_print(0, 0, "Attribute error", e, "".join(sentence_characters), sentence_regex)
                # _Shouldn't_ happen, as the regexp is basically part of the transcript we're
                # looking at. Character's don't vanish from the transcript, so there's always a match.
                cls.mark_sentence_not_appearing(sentence, alignment_parameters, last_end_time)
                last_end_time = last_end_time + alignment_parameters["no_appearance"]["interval_length"]
                continue

            # Mostly none values on either side indicates a false positive, move to beginning of sentence with
            if is_mostly_none(list(google_alignment[alignment_start_point:alignment_end_point])) \
                    or is_mostly_none(list(transcript_alignment[alignment_start_point:alignment_end_point])):
                cls.mark_sentence_not_appearing(sentence, alignment_parameters, last_end_time)
                last_end_time = last_end_time + alignment_parameters["no_appearance"]["interval_length"]
                continue

            google_sub_start = len(
                [c for c in google_alignment[0:alignment_start_point] if c is not '-' and c is not ' '])
            google_sub_end = len([c for c in google_alignment[0:alignment_end_point] if c is not '-' and c is not ' '])

            character_count = 0
            found_start = False

            start_word_confidence = 0.0
            end_word_confidence = 0.0

            for word in google_words:
                character_count += len(preprocess_string(word["word"]))
                word_start_time = float(word["startTime"].replace("s", ""))

                # Guarantee that there's no overlapping sentences
                if character_count >= google_sub_start and last_end_time <= word_start_time and not found_start:
                    sentence.interval.start = word_start_time
                    start_word_confidence = word["confidence"]
                    found_start = True

                if found_start and character_count >= google_sub_end:
                    sentence.interval.end = float(word["endTime"].replace("s", ""))
                    last_end_time = sentence.interval.end
                    end_word_confidence = word["confidence"]
                    break

            sentence_confidence = get_sentence_confidence(
                start_word_confidence,
                end_word_confidence,
                transcript_alignment[alignment_start_point:alignment_end_point],
                google_alignment[alignment_start_point:alignment_end_point],
                alignment_parameters["algorithm"]["match_reward"],
                alignment_parameters["algorithm"]["mismatch_penalty"],
                alignment_parameters["algorithm"]["gap_penalty"]
            )

            google_gaps_percentage = get_none_part(
                list(google_alignment[alignment_start_point:alignment_end_point])
            )
            transcript_gaps_percentage = get_none_part(
                list(transcript_alignment[alignment_start_point:alignment_end_point])
            )

            sentence.additional_data = AdditionalData(
                sentence_confidence["average_google_confidence"],
                sentence_confidence["normalized_sentence_score"],
                google_gaps_percentage,
                transcript_gaps_percentage
            )

            overall_score = calculate_overall_score(
                google_gaps_percentage,
                transcript_gaps_percentage,
                sentence_confidence["average_google_confidence"],
                sentence_confidence["normalized_sentence_score"],
                alignment_parameters["score_weights"]["gaps_google"],
                alignment_parameters["score_weights"]["gaps_transcript"],
                alignment_parameters["score_weights"]["alignment_score"],
                alignment_parameters["score_weights"]["google_confidence"]
            )

            if overall_score > alignment_parameters["filtering"]["threshold"]:
                if alignment_parameters["filtering"]["method"] == "mark":
                    sentence.sentence = "[BAD]" + sentence.sentence
                    sentence_index += 1
                else:
                    del(sentences[sentence_index])
            else:
                sentence_index += 1

            end_time = time()
            execution_times.append(end_time - start_time)

            bin_print(verbosity, 2, "Sentence confidence:", str(sentence_confidence))

        if track_time:
            bin_print(verbosity, 0, "Execution time per sentence (mean): ", np.mean(execution_times))
            bin_print(verbosity, 0, "Execution time per sentence (max):  ", np.max(execution_times))

        return sentences

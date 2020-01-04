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
from nltk import word_tokenize
import re


class AbstractGoogleAlignerStrategy(AbstractAlignerStrategy):
    """
    Abstract base class to allow typehinting.
    """

    @staticmethod
    @abc.abstractmethod
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
                           google_words, alignment_parameters, verbosity)

    @staticmethod
    def get_google_words(google_output: object) -> List[dict]:
        """
        Preprocesses the Google output to further work with it.
        :param google_output: JSON object
        :return:
        """
        return [{'word': preprocess_string(w["word"]), "startTime": w["startTime"], "endTime": w["endTime"]} for w in
            sum([r.alternatives[0]["words"] for r in google_output.results], [])]

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
                           google_words: List[object], alignment_parameters: Dict[str, Any], verbosity: int) -> None:
        """
        Assigns start and end times to sentences based on given alignments.
        :param sentences:            All sentences
        :param transcript_alignment: Aligned transcript
        :param google_alignment:     Aligned google output
        :param google_words:         Google words, to get startTime and endTime
        :param alignment_parameters: Dict of parameters loaded from a given YAML file. See README for full config.
        :param verbosity:            Verbosity of output
        :return: None
        """
        last_end_point = 0
        last_end_time = 0.0

        for sentence in sentences:
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
            if is_mostly_none(google_alignment[alignment_start_point:alignment_end_point]) \
                    or is_mostly_none(transcript_alignment[alignment_start_point:alignment_end_point]):
                cls.mark_sentence_not_appearing(sentence, alignment_parameters, last_end_time)
                last_end_time = last_end_time + alignment_parameters["no_appearance"]["interval_length"]
                continue

            google_sub_start = len(
                [c for c in google_alignment[0:alignment_start_point] if c is not '-' and c is not ' '])
            google_sub_end = len([c for c in google_alignment[0:alignment_end_point] if c is not '-' and c is not ' '])

            character_count = 0
            found_start = False

            startWord = None
            endWord = None

            for word in google_words:
                character_count += len(preprocess_string(word["word"]))
                word_start_time = float(word["startTime"].replace("s", ""))

                # Guarantee that there's no overlapping sentences
                if character_count >= google_sub_start and last_end_time <= word_start_time and not found_start:
                    sentence.interval.start = word_start_time
                    startWord = word["word"]
                    found_start = True

                if found_start and character_count >= google_sub_end:
                    sentence.interval.end = float(word["endTime"].replace("s", ""))
                    last_end_time = sentence.interval.end
                    endWord = word["word"]
                    break

            sentence_confidence = get_sentence_confidence(
                ''.join(sentence_characters),
                0.0,
                transcript_alignment[alignment_start_point:alignment_end_point],
                google_alignment[alignment_start_point:alignment_end_point],
                alignment_parameters["algorithm"]["match_reward"],
                alignment_parameters["algorithm"]["mismatch_penalty"],
                alignment_parameters["algorithm"]["gap_penalty"]
            )

            bin_print(verbosity, 2, "Sentence confidence:", str(sentence_confidence * 2))

        return sentences

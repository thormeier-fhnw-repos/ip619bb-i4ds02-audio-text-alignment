import unittest
from typing import Dict, Any, List, Tuple
from unittest_data_provider import data_provider
from lib.test.test_utils.TempDir import TempDir
from lib.src.align.compare.compare_alignments import compare_alignments
from lib.src.model.Sentence import Sentence
from lib.src.model.Interval import Interval
from numpy import nan


class AlignmentFile:
    """
    Represents a file for alignment
    """

    def __init__(self, name: str, sentences: List[Sentence]):
        self.name = name
        self.sentences = sentences

    def get_name(self) -> str:
        """
        Get the name of the file
        :return: File name
        """
        return self.name

    def get_content(self) -> str:
        """
        Gets the files content as a string
        :return: Content, ready to be written
        """
        return "\n".join([sentence.to_audacity_label_format() for sentence in self.sentences])


def test_compare_alignment_data_provider() -> Tuple:
    """
    Data provider function
    :return: Tuple
    """
    sentence_1 = Sentence("foo", Interval(0.0, 0.1))
    sentence_2 = Sentence("bar", Interval(0.0, 0.2))
    sentence_3 = Sentence("baz", Interval(0.1, 0.2))
    sentence_4 = Sentence("qux", Interval(0.0, 0.2))
    sentence_5 = Sentence("lorem", Interval(0.0001, 0.0002)) # Doesn't appear

    file_1_type1 = AlignmentFile("file_1_audacity_type1.txt", [sentence_1, sentence_2, sentence_5])
    file_2_type1 = AlignmentFile("file_2_audacity_type1.txt", [sentence_1, sentence_2, sentence_5])
    file_3_type1 = AlignmentFile("file_3_audacity_type1.txt", [sentence_1])
    file_4_type1 = AlignmentFile("file_4_audacity_type1.txt", [sentence_1, sentence_2, sentence_3, sentence_4])
    file_1_type2 = AlignmentFile("file_1_audacity_type2.txt", [sentence_1, sentence_2, sentence_5])
    file_2_type2 = AlignmentFile("file_2_audacity_type2.txt", [sentence_1, sentence_2, sentence_5])
    file_3_type2 = AlignmentFile("file_3_audacity_type2.txt", [sentence_3])
    file_4_type2 = AlignmentFile("file_4_audacity_type2.txt", [sentence_1, sentence_3, sentence_4, sentence_5])

    config = {"no_appearance": {"interval_length": 0.0001}}

    return (
        # No data at all, should fallback to zeros etc., no warnings or erros
        ([], config, {"no_sentences": {"appearing": 0, "total": 0, }, "ious": {"all": [], "low": [], "mean": nan, "median": nan, "per_file": {}}, "appearance": {"true_positives": 0, "false_positives": 0, "true_negatives": 0, "false_negatives": 0, "precision": 0.0, "recall": 0.0, "f1_score": 0.0}}),
        # Worst possible score with data
        ([file_3_type1, file_3_type2], config, {'no_sentences': {'appearing': 1, 'total': 1}, 'ious': {'all': [(0, 0.1, 0.1, 'foo', '\\file_3')], 'low': ['\\file_3.wav'], 'mean': 0.0, 'median': 0.0, 'per_file': {'\\file_3': {'mean': 0.0, 'median': 0.0, 'all': [(0, 0.1, 0.1, 'foo', '\\file_3')]}}}, 'appearance': {'true_positives': 1, 'false_positives': 0, 'true_negatives': 0, 'false_negatives': 0, 'precision': 1.0, 'recall': 1.0, 'f1_score': 1.0}}),
        # Perfect scores
        ([file_1_type1, file_2_type1, file_1_type2, file_2_type2], config, {'no_sentences': {'appearing': 4, 'total': 6}, 'ious': {'all': [(1.0, 0.1, 0.1, 'foo', '\\file_1'), (1.0, 0.2, 0.2, 'bar', '\\file_1'), (1.0, 0.1, 0.1, 'foo', '\\file_2'), (1.0, 0.2, 0.2, 'bar', '\\file_2')], 'low': [], 'mean': 1.0, 'median': 1.0, 'per_file': {'\\file_1': {'mean': 1.0, 'median': 1.0, 'all': [(1.0, 0.1, 0.1, 'foo', '\\file_1'), (1.0, 0.2, 0.2, 'bar', '\\file_1')]}, '\\file_2': {'mean': 1.0, 'median': 1.0, 'all': [(1.0, 0.1, 0.1, 'foo', '\\file_2'), (1.0, 0.2, 0.2, 'bar', '\\file_2')]}}}, 'appearance': {'true_positives': 4, 'false_positives': 0, 'true_negatives': 2, 'false_negatives': 0, 'precision': 1.0, 'recall': 1.0, 'f1_score': 1.0}}),
        # Some intermediate score
        ([file_4_type1, file_4_type2], config, {'no_sentences': {'appearing': 3, 'total': 4}, 'ious': {'all': [(1.0, 0.1, 0.1, 'foo', '\\file_4'), (0.5, 0.2, 0.1, 'bar', '\\file_4'), (0.5, 0.1, 0.2, 'baz', '\\file_4')], 'low': [], 'mean': 0.66666666666666663, 'median': 0.5, 'per_file': {'\\file_4': {'mean': 0.66666666666666663, 'median': 0.5, 'all': [(1.0, 0.1, 0.1, 'foo', '\\file_4'), (0.5, 0.2, 0.1, 'bar', '\\file_4'), (0.5, 0.1, 0.2, 'baz', '\\file_4')]}}}, 'appearance': {'true_positives': 3, 'false_positives': 0, 'true_negatives': 0, 'false_negatives': 1, 'precision': 1.0, 'recall': 0.75, 'f1_score': 0.8571428571428571}}),
        # One file exists, the other one doesn't, hence no data
        ([file_1_type1], config, {"no_sentences": {"appearing": 0, "total": 0, }, "ious": {"all": [], "low": [], "mean": nan, "median": nan, "per_file": {}}, "appearance": {"true_positives": 0, "false_positives": 0, "true_negatives": 0, "false_negatives": 0, "precision": 0.0, "recall": 0.0, "f1_score": 0.0}}),
    )


class TestCompareAlignments(unittest.TestCase):
    """
    Tests lib.src.align.compare.compare_alignments
    """

    @data_provider(test_compare_alignment_data_provider)
    def test_compare_alignment(self, files: List[AlignmentFile], config: Dict[str, Any],
                               expected_result: Dict[str, Any]) -> None:
        """
        Tests the whole comparison of alignments
        :param files:           List of files to create for type1
        :param config:          Mocked config dict
        :param expected_result: Expected result as dict
        :return: None
        """
        temp_dir = TempDir()
        for file in files:
            temp_dir.create_file(file.get_name(), file.get_content())

        input_path = temp_dir.get_path()

        result = compare_alignments(input_path, 0, "type1", "type2", False, config)

        self.assertDictEqual(expected_result, result)

    pass


if __name__ == '__main__':
    unittest.main()

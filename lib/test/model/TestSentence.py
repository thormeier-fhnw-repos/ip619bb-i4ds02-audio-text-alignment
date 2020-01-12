import unittest
from unittest_data_provider import data_provider
from typing import Any
from lib.src.model.Interval import Interval
from lib.src.model.Sentence import Sentence, sentence_from_string


class IntervalMock(Interval):
    """
    Mocks an Interval
    """

    def __init__(self, start, end):
        super().__init__(start, end)
        self.start = start
        self.end = end

    def to_formatted(self):
        """
        To formatted mock
        :return: Some hardcoded string to test against
        """
        return "mocked_interval"


class TestSentence(unittest.TestCase):
    """
    Test class lib.src.model.Sentence
    """

    audacity_label_format_data_provider = lambda: (
        ("Lorem ipsum dolor", IntervalMock(0.0, 0.0), "mocked_interval\tLorem ipsum dolor"),  # Sanity check
        (None, IntervalMock(0.0, 0.0), "mocked_interval\tNone"),  # Sentence is None
        ("", IntervalMock(0.0, 0.0), "mocked_interval\t"),  # Empty sentence
    )

    @data_provider(audacity_label_format_data_provider)
    def test_to_audacity_label_format(self, sentence: Any, interval: IntervalMock, expected_format: str) -> None:
        """
        Tests to_audacity_label_format method's behaviour
        :param sentence:        Inner sentence
        :param interval:        Mocked interval
        :param expected_format: Expected audacity label format
        :return: None
        """
        s = Sentence(sentence, interval)
        self.assertEqual(s.to_audacity_label_format(), expected_format)

    merge_sentence_data_provider = lambda: (
        ("foo", IntervalMock(0.0, 0.1), "bar", IntervalMock(0.1, 0.2), Sentence("foo bar", Interval(0.0, 0.2))),  # Sanity check
        ("foo", IntervalMock(0.1, 0.2), "bar", IntervalMock(0.0, 0.1), Sentence("bar foo", Interval(0.0, 0.2))),  # Flipped intervals
        ("   foo   ", IntervalMock(0.0, 0.1), "   bar   ", IntervalMock(0.1, 0.2), Sentence("foo bar", Interval(0.0, 0.2))),  # Additional spaces around sentences
        (None, IntervalMock(0.0, 0.1), "bar", IntervalMock(0.1, 0.2), Sentence("None bar", Interval(0.0, 0.2))),  # One sentence is None
        ("foo", IntervalMock(0.0, 0.1), None, IntervalMock(0.1, 0.2), Sentence("foo None", Interval(0.0, 0.2))),  # Other sentence is None
        (None, IntervalMock(0.0, 0.1), None, IntervalMock(0.1, 0.2), Sentence("None None", Interval(0.0, 0.2))),  # Both sentences are none
    )

    @data_provider(merge_sentence_data_provider)
    def test_merge_with(self, sentence: str, interval: IntervalMock, other_sentence: str, other_interval: IntervalMock,
                        expected_sentence: Sentence) -> None:
        """
        Tests the merge_with method's behaviour
        :param sentence:          First sentence as string
        :param interval:          First interval
        :param other_sentence:    Other sentence as string
        :param other_interval:    Other interval
        :param expected_sentence: Expected merged sentence
        :return: None
        """
        a = Sentence(sentence, interval)
        b = Sentence(other_sentence, other_interval)
        self.assertEqual(a.merge_with(b).to_audacity_label_format(), expected_sentence.to_audacity_label_format())
        pass

    from_string_data_provider = lambda: (
        ("0.0000\t1.0000\tfoo bar baz", float, 0.0, float, 1.0, "foo bar baz"),  # Sanity check
        ("-\t0.00\tfoo bar baz", str, "-", float, 0.0, "foo bar baz"),  # One interval part isn't float
        ("0.00\t-\tfoo bar baz", float, 0.0, str, "-", "foo bar baz"),  # Other interval part isn't float
        ("-\t-\tfoo bar baz", str, "-", str, "-", "foo bar baz"),  # Both interval parts aren't float
    )

    @data_provider(from_string_data_provider)
    def test_sentence_from_string(self, input_string: str, expected_start_type: Any, expected_start: Any,
                                  expected_end_type: Any, expected_end: Any, expected_sentence: str) -> None:
        """
        Tests sntence_from_string function's behaviour.
        :param input_string:        Formatted string to parse
        :param expected_start_type: Type of the inner Interval's start property
        :param expected_start:      Value of the inner Interval's start property
        :param expected_end_type:   Type of the inner Interval's end property
        :param expected_end:        Value of the inner Interval's end property
        :param expected_sentence:   Expected inner sentence as string
        :return: None
        """
        s = sentence_from_string(input_string)
        self.assertIsInstance(s.interval.start, expected_start_type)
        self.assertEqual(s.interval.start, expected_start)
        self.assertIsInstance(s.interval.end, expected_end_type)
        self.assertEqual(s.interval.end, expected_end)
        self.assertEqual(s.sentence, expected_sentence)

if __name__ == '__main__':
    unittest.main()

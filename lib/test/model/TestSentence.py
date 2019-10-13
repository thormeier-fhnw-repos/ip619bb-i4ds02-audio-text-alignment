import unittest
from lib.src.model.Sentence import Sentence, sentence_from_string


class IntervalMock:
    """
    Mocks an Interval
    """

    def __init__(self, start, end):
        self.start = start
        self.end = end


class TestSentence(unittest.TestCase):
    """
    Tests src.model.Sentence
    """

    def test_get_audacity_label_format(self):
        interval = IntervalMock(12.0, 13.5)
        text = "Lorem Ipsum"
        sentence = Sentence(text, interval)

        self.assertEqual("12.000000000000000\t13.500000000000000\tLorem Ipsum", sentence.to_audacity_label_format())

    def test_sentence_from_string(self):
        string = "12.123\t13.445\tFoobar"
        sentence = sentence_from_string(string)

        self.assertEqual("Foobar", sentence.sentence)
        self.assertEqual(12.123, sentence.interval.start)
        self.assertEqual(13.445, sentence.interval.end)

    def test_merge(self):
        sentence1 = Sentence("Lorem ", IntervalMock(0.0, 0.1))
        sentence2 = Sentence(" Ipsum", IntervalMock(0.1, 0.2))
        sentence_merged_1 = sentence1.merge_with(sentence2)
        sentence_merged_2 = sentence2.merge_with(sentence1)

        self.assertEqual(sentence_merged_1.sentence, sentence_merged_2.sentence)
        self.assertEqual(sentence_merged_1.interval.start, sentence_merged_2.interval.start)
        self.assertEqual(sentence_merged_1.interval.end, sentence_merged_2.interval.end)

        self.assertEqual("LoremIpsum", sentence_merged_1.sentence)
        self.assertEqual(0.0, sentence_merged_1.interval.start)
        self.assertEqual(0.2, sentence_merged_1.interval.end)


if __name__ == '__main__':
    unittest.main()

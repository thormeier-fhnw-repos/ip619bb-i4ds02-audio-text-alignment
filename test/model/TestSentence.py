import unittest

from src.model.Sentence import Sentence


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

        self.assertEqual("12.000000\t13.500000\tLorem Ipsum", sentence.to_audacity_label_format())


if __name__ == '__main__':
    unittest.main()

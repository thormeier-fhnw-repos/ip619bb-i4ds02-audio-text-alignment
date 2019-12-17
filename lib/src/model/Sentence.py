from lib.src.model.Interval import Interval


class Sentence:
    def __init__(self, sentence: str, interval: Interval):
        """
        Defines a sentence with corresponding interval
        :param sentence: String
        :param interval: Interval
        """
        self.sentence = sentence
        self.interval = interval

    def to_audacity_label_format(self) -> str:
        """
        Transforms this sentence to Audacity Label Format
        :return: str
        """
        return "\t".join([
            "%.15f" % (self.interval.start if self.interval.start is not None else 0.0),
            "%.15f" % (self.interval.end if self.interval.end is not None else 0.0),
            str(self.sentence)
        ])

    def merge_with(self, other: 'Sentence') -> 'Sentence':
        """
        Merges two sentences
        :param other:
        :return:
        """
        if self.interval.start < other.interval.start:
            sentence = self.sentence.strip() + other.sentence.strip()
            start_time = self.interval.start
            end_time = other.interval.end
        else:
            sentence = other.sentence.strip() + self.sentence.strip()
            start_time = other.interval.start
            end_time = self.interval.end

        return Sentence(sentence, Interval(start_time, end_time))


def sentence_from_string(string: str) -> Sentence:
    """
    Creates a Sentence object from a given single line of an alignment
    :param string:
    :return: Sentence
    """
    parts = string.split("\t")

    return Sentence(parts[2], Interval(float(parts[0]), float(parts[1])))
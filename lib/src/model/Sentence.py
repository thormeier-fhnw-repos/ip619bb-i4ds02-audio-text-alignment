from lib.src.model.Interval import Interval
from lib.src.model.AdditionalData import AdditionalData


class Sentence:
    """
    Represents a sentence ith all its related data
    """

    def __init__(self, sentence: str, interval: Interval, additional_data: AdditionalData):
        """
        Defines a sentence with corresponding interval
        :param sentence:        String
        :param interval:        Interval
        :param additional_data: AdditionalData
        """
        self.sentence = sentence
        self.interval = interval
        self.additional_data = additional_data

    def to_audacity_label_format(self) -> str:
        """
        Transforms this sentence to Audacity Label Format
        :return: str
        """
        formatted = self.interval.to_formatted() + "\t" + str(self.sentence)

        if self.additional_data is not None:
            formatted = formatted + "\t" + self.additional_data.to_formatted()

        return formatted

    def merge_with(self, other: 'Sentence') -> 'Sentence':
        """
        Merges two sentences
        :param other:
        :return:
        """
        if not (isinstance(self.interval.start, float) and isinstance(other.interval.start, float)) or self.interval.start < other.interval.start:
            sentence = str(self.sentence).strip() + " " + str(other.sentence).strip()
            start_time = self.interval.start
            end_time = other.interval.end
        else:
            sentence = str(other.sentence).strip() + " " + str(self.sentence).strip()
            start_time = other.interval.start
            end_time = self.interval.end

        return Sentence(sentence, Interval(start_time, end_time), self.additional_data)


def sentence_from_string(string: str) -> Sentence:
    """
    Creates a Sentence object from a given single line of an alignment
    :param string: Input string to parse
    :return: Sentence
    """
    parts = string.split("\t")

    try:
        interval_start = float(parts[0])
    except ValueError:
        interval_start = parts[0]

    try:
        interval_end = float(parts[1])
    except ValueError:
        interval_end = parts[1]

    additional_data = None
    if len(parts) > 3:
        additional_data = AdditionalData(float(parts[3]), float(parts[4]), float(parts[5]), float(parts[6]))

    return Sentence(parts[2].strip(), Interval(interval_start, interval_end), additional_data)

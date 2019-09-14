class Sentence:
    def __init__(self, sentence, interval):
        """
        Defines a sentence with corresponding interval
        :param sentence: String
        :param interval: Interval
        """
        self.sentence = sentence
        self.interval = interval

    def to_audacity_label_format(self):
        """
        Transforms this sentence to Audacity Label Format
        :return:
        """
        return "\t".join([
            "%.6f" % self.interval.start,
            "%.6f" % self.interval.end,
            self.sentence
        ])
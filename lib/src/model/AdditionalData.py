class AdditionalData:
    """
    Additional data for a Sentence
    """

    def __init__(self, google_confidence: float, normalized_sentence_score: float, gaps_transcript: float,
                 gaps_google: float) -> None:
        """
        Constructor
        :param google_confidence:         Google's average recognition confidence
        :param normalized_sentence_score: Normalized alignment score for the given sentence
        :param gaps_transcript:           Percentage of gaps, relative to total length (characters + gaps)
        :param gaps_google:               Percentage of gaps, relative to total length (characters + gaps)
        """
        self.google_confidence = google_confidence
        self.normalized_sentence_score = normalized_sentence_score
        self.gaps_transcript = gaps_transcript
        self.gaps_google = gaps_google

    def to_formatted(self) -> str:
        """
        Formats itself to audacity label format
        :return: Formatted data
        """
        return str(self.google_confidence) + \
               "\t" + str(self.normalized_sentence_score) + \
               "\t" + str(self.gaps_transcript) + \
               "\t" + str(self.gaps_google)

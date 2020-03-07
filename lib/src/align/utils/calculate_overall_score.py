def calculate_overall_score(
        google_gaps_percentage: float, transcript_gaps_percentage: float,
        google_confidence: float, alignment_score: float,
        weight_google_gaps: float, weight_transcript_gaps: float,
        weight_google_confidence: float, weight_alignment_score: float
    ) -> float:
    """
    Calculates a score to predict if an alignment is "good" or not.

    :param google_gaps_percentage:     Percentage of gaps added to google's STT output
    :param transcript_gaps_percentage: Percentage of gaps added to the transcript
    :param google_confidence:          Confidence of google's STT
    :param alignment_score:            Final score of the alignment algorithm
    :param weight_google_gaps:         Weight for weighted sum
    :param weight_transcript_gaps:     Weight for weighted sum
    :param weight_google_confidence:   Weight for weighted sum
    :param weight_alignment_score:     Weight for weighted sum

    :return: Score between 0 and 1
    """
    return (
        (weight_google_gaps * google_gaps_percentage)
        + (weight_transcript_gaps * transcript_gaps_percentage)
        + (weight_google_confidence * google_confidence)
        + (weight_alignment_score * alignment_score)
    )

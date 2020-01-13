def get_sentence_confidence(transcript_sentence: str, google_start_confidence: float, google_end_confidence: float, transcript_alignment_sentence: str, transcript_google_sentence: str, match_reward: int, mismatch_penalty: int, gap_penalty: int) -> float:
    """
    Calculates an overall confidence for a given sentence
    :param transcript_sentence: Sentence as coming from the transcript
    :param google_start_confidence: Google's confidence for the first word
    :param google_end_confidence:   Google's confidence with the last word
    :param alignment_sentence:      Alignment of this sentence
    :param google_sentence:
    :param match_reward:
    :param mismatch_penalty:
    :param gap_penalty:
    :return: Calculated confidence
    """

    # Count all gaps: they contribute to overall score
    no_gaps_transcript = transcript_alignment_sentence.count('-')
    no_gaps_google = transcript_google_sentence.count('-')

    # Remove all gap characters
    transcript_alignment_sentence_gapless = transcript_alignment_sentence.replace('-', '')
    transcript_google_sentence_gapless = transcript_google_sentence.replace('-', '')

    no_matches = 0
    no_mismatches = 0
    for char_pair in list(zip(transcript_alignment_sentence_gapless, transcript_google_sentence_gapless)):
        if char_pair[0] == char_pair[1]:
            no_matches += 1
        else:
            no_mismatches += 1

    # Calculate the score for this sentence according to Needleman-Wunsch
    sentence_score = (no_gaps_google * gap_penalty) + (no_gaps_transcript * gap_penalty) + (no_mismatches * mismatch_penalty) + (no_matches * match_reward)

    # Calculate a possible maximum score according to Needleman-Wunsch (i.e. every char is a match)

    # Assign the longer of the two sentences to sent_a
    if len(transcript_alignment_sentence_gapless) > len(transcript_google_sentence_gapless):
        sent_a = transcript_alignment_sentence_gapless
        sent_b = transcript_google_sentence_gapless
    else:
        sent_a = transcript_google_sentence_gapless
        sent_b = transcript_alignment_sentence_gapless

    # Every character is a match, but afterwards, gaps are needed, calculate those in.
    max_sentence_score = len(sent_b) * match_reward + ((len(sent_a) - len(sent_b)) * gap_penalty)
    if mismatch_penalty < gap_penalty:
        min_sentence_score = len(sent_b) * mismatch_penalty + ((len(sent_a) - len(sent_b)) * gap_penalty)
    else:
        min_sentence_score = (len(sent_a) * gap_penalty) + (len(sent_b) * gap_penalty)

    adjusted_max_score = max_sentence_score - min_sentence_score
    adjusted_score = sentence_score - min_sentence_score

    alignment_confidence = adjusted_score / adjusted_max_score

    # print(min_sentence_score, max_sentence_score, sentence_score, alignment_confidence * ((google_start_confidence + google_end_confidence) / 2))

    overall_confidence = alignment_confidence * ((google_start_confidence + google_end_confidence) / 2)

    return overall_confidence
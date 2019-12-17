def get_sentence_confidence(transcript_sentence: str, google_sentence_confidence: float, transcript_alignment_sentence: str, transcript_google_sentence: str, match_reward: int, mismatch_penalty: int, gap_penalty: int) -> float:
    """
    Calculates an overall confidence for a given sentence
    :param transcript_sentence:
    :param google_sentence_confidence:
    :param alignment_sentence:
    :param google_sentence:
    :param match_reward:
    :param mismatch_penalty:
    :param gap_penalty:
    :return:
    """

    # Count all gaps: they contribute to overall score
    no_gaps_transcript = transcript_alignment_sentence.count('-')
    no_gaps_google = transcript_google_sentence.count('-')

    # Remove all gap characters
    transcript_alignment_sentence = transcript_alignment_sentence.replace('-', '')
    transcript_google_sentence = transcript_google_sentence.replace('-', '')

    no_matches = 0
    no_mismatches = 0
    for char_pair in list(zip(transcript_alignment_sentence, transcript_google_sentence)):
        if char_pair[0] == char_pair[1]:
            no_matches += 1
        else:
            no_mismatches += 1

    print(no_gaps_transcript, no_gaps_google, no_mismatches, no_matches)

    # Calculate the score for this sentence according to Needleman-Wunsch
    sentence_score = (no_gaps_google * gap_penalty) + (no_gaps_transcript * gap_penalty) + (no_mismatches * mismatch_penalty) + (no_matches * match_reward)

    print(sentence_score, (no_gaps_google * gap_penalty), (no_gaps_transcript * gap_penalty), (no_mismatches * mismatch_penalty), (no_matches * match_reward))

    # Calculate a possible maximum score according to Needleman-Wunsch (i.e. every char is a match)
    max_sentence_score = len(transcript_sentence) * match_reward

    alignment_confidence = sentence_score / max_sentence_score

    overall_confidence = (alignment_confidence + google_sentence_confidence) / 2

    return overall_confidence
from typing import List, Tuple
from lib.src.align.sequence_alignment.create_score_matrix import create_score_matrix
from lib.src.align.sequence_alignment.walk_matrix import walk_matrix
import numpy as np


def smith_waterman(a: List, b: List, match_reward: int, mismatch_penalty: int, gap_penalty: int) -> List[Tuple[List, List, int]]:
    """
    Needleman-Wunsch implementation for global sequence alignment
    :param a: Sequence A, horizontal in score matrix, i.e. cols
    :param b: Sequence B, vertical in score matrix, i.e. rows
    :param match_reward: Reward given for a match
    :param mismatch_penalty: Penalty given for a mismatch
    :param gap_penalty: Penalty given for a gap
    :return: List of possible alignments and their score.
    """
    score_matrix = create_score_matrix(a, b, match_reward, mismatch_penalty, gap_penalty, False, True)

    max_scores = np.where(score_matrix == np.amax(score_matrix))
    max_score_coord_pairs = list(zip(max_scores[0], max_scores[1]))

    return [walk_matrix(score_matrix, pair[0], pair[1], a, b, match_reward, mismatch_penalty, gap_penalty, False) for pair in max_score_coord_pairs]

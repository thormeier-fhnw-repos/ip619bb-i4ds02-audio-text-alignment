from typing import List, Tuple, Callable
from lib.src.align.sequence_alignment.create_score_matrix import create_score_matrix
from lib.src.align.sequence_alignment.walk_matrix import walk_matrix
import numpy as np


def smith_waterman(a: List, b: List, match_reward: int, mismatch_penalty: int, gap_penalty: int,
                   compare_function: Callable) -> Tuple[List, List, int]:
    """
    Smith-Waterman algorithm for local sequence alignment

    :param a:                Sequence A, horizontal in score matrix, i.e. cols
    :param b:                Sequence B, vertical in score matrix, i.e. rows
    :param match_reward:     Reward given for a match
    :param mismatch_penalty: Penalty given for a mismatch
    :param gap_penalty:      Penalty given for a gap
    :param compare_function: Function to compare two elements of sequences

    :return: List of possible alignments and their score.
    """
    score_matrix = create_score_matrix(a, b, match_reward, mismatch_penalty, gap_penalty, compare_function, False, True)

    max_score_coord_pairs = np.unravel_index(score_matrix.argmax(), score_matrix.shape)

    return walk_matrix(score_matrix, int(max_score_coord_pairs[1]), int(max_score_coord_pairs[0]), a, b, match_reward,
                       mismatch_penalty, gap_penalty, compare_function, False)

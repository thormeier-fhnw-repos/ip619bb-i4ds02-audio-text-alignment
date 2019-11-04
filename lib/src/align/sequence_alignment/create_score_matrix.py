from typing import List
import numpy as np


def create_score_matrix(a: List, b: List, match_reward: int, mismatch_penalty: int, gap_penalty: int, allow_negative: bool = True, zero_borders: bool = False) -> np.ndarray:
    """
    Creates a score matrix, fit for all kinds of
    :param a: Sequence A, horizontal in score matrix, i.e. cols
    :param b: Sequence B, vertical in score matrix, i.e. rows
    :param match_reward: Reward to give in case of match
    :param mismatch_penalty: Penalty to give in case of mismatch
    :param gap_penalty: Penalty to give in case of gap introduction
    :param allow_negative: If negative values are allowed. If not, a 0 is used instead.
    :param zero_borders: If the borders should be left at 0. Needed for semi-global and local alignment.
    :return: Score matrix
    """
    cols = len(a) + 1
    rows = len(b) + 1

    # Flipped at first, so we can transpose later.
    score_matrix = np.zeros((cols, rows))

    # Fill score matrix with gap penalties along the axis
    if not zero_borders:
        score_matrix[0] = list(range(0, rows * gap_penalty, gap_penalty))
        score_matrix = score_matrix.transpose()
        score_matrix[0] = list(range(0, cols * gap_penalty, gap_penalty))
    else:
        score_matrix = score_matrix.transpose()

    def get_diag_score(a, b):
        """
        Get score for diagonal move.
        :param a: Sequence element from A
        :param b: Sequence element from B
        :return:
        """
        return mismatch_penalty if a[col - 1] != b[row - 1] else match_reward

    for row in range(1, rows):
        for col in range(1, cols):
            up = score_matrix[row - 1, col] + gap_penalty
            left = score_matrix[row, col - 1] + gap_penalty
            diag = score_matrix[row - 1, col - 1] + get_diag_score(a, b)

            if allow_negative:
                score_matrix[row, col] = max(up, left, diag)
            else:
                score_matrix[row, col] = max(0, up, left, diag)

    return score_matrix

from typing import List, Tuple
import numpy as np


def walk_matrix(score_matrix: np.ndarray, start_col: int, start_row: int, a: List, b: List, match_reward: int, mismatch_penalty: int, gap_penalty: int, allow_negative: bool = True) -> Tuple[List, List, int]:
    aligned_a = []
    aligned_b = []

    col = start_col
    row = start_row

    def get_diag_score(a, b):
        """
        Get score for diagonal move.
        :param a: Sequence element from A
        :param b: Sequence element from B
        :return:
        """
        return mismatch_penalty if a != b else match_reward

    # Build actual alignment.
    while row > 0 or col > 0:
        if not allow_negative and score_matrix[row, col] == 0:
            break

        print(row, col)

        curr = score_matrix[row, col]
        diag = score_matrix[row - 1, col - 1]
        left = score_matrix[row, col - 1]
        up = score_matrix[row - 1, col]

        if row > 0 and col > 0 and curr == diag + get_diag_score(a[col - 1], b[row - 1]):
            # This introduces a bias towards taking matches/mismatches,
            # even if a gap would have yielded the same result.
            aligned_a.insert(0, a[col - 1])
            aligned_b.insert(0, b[row - 1])
            col -= 1
            row -= 1
        elif row > 0 and curr == up + gap_penalty or (allow_negative and curr == up):
            # Up
            aligned_a.insert(0, None)
            aligned_b.insert(0, b[row - 1])
            row -= 1
        elif col > 0 and (curr == left + gap_penalty or (allow_negative and curr == left)):
            # Left
            aligned_a.insert(0, a[col - 1])
            aligned_b.insert(0, None)
            col -= 1

    return aligned_a, aligned_b, score_matrix[start_row][start_col]

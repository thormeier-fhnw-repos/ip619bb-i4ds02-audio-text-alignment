from typing import List
import numpy as np
from scipy.stats import pearsonr


def pearsonr_lists(a: List, b: List) -> float:
    """
    Calculates pearson coefficient for two lists
    :param a: Data sample
    :param b: Data sample
    :return: personr return
    """
    return pearsonr(
        np.array(a).astype(np.float),
        np.array(b).astype(np.float)
    )[0]

from lib.src.model.Interval import Interval


def intersection_over_union(ground_truth: Interval, prediction: Interval) -> float:
    """
    Calculates the IOU score for two pairs, groundtruth and prediction
    :param ground_truth: Interval
    :param prediction: Interval
    :return: float
    """
    intersection = ground_truth.get_intersection(prediction)
    union = ground_truth.get_union(prediction)

    if intersection == 0.0 or union == 0.0:
        return 0

    return intersection / union

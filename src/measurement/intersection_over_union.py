def intersection_over_union(ground_truth, prediction):
    """
    Calculates the IOU score for two pairss, groundtruth and prediction
    :param ground_truth: Interval
    :param prediction: Interval
    :return: Float
    """
    intersection = ground_truth.get_intersection(prediction)
    union = ground_truth.get_union(prediction)

    if intersection is None or union is None:
        return 0

    return intersection / union

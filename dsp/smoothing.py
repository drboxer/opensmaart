import numpy as np


def smooth(
        values,
        width
):

    if width <= 1:

        return values

    kernel = np.ones(
        width
    ) / width

    return np.convolve(
        values,
        kernel,
        mode="same"
    )
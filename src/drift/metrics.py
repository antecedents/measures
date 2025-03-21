import logging

import numpy as np
import scipy.spatial as sp


class JS:

    def __init__(self):
        pass

    @staticmethod
    def exc(matrix: np.ndarray) -> tuple:
        """

        :param matrix:
        :return:
        """

        ultimate = matrix[:-1, :]
        penultimate = matrix[1:, :]

        ultimate = np.fliplr(ultimate)
        penultimate = np.fliplr(penultimate)

        scores = sp.distance.jensenshannon(p=penultimate, q=ultimate, axis=1)
        logging.info(scores)

        return matrix.shape

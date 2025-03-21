import logging

import numpy as np
import scipy.spatial as sp


class Metrics:

    def __init__(self):
        pass

    def __get_js(self, penultimate, ultimate):

        scores = sp.distance.jensenshannon(p=penultimate, q=ultimate, axis=1)
        logging.info(scores)

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



        return matrix.shape

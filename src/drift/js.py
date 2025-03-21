import logging

import numpy as np


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

        logging.info('\n\n%s\n%s\n%s\n', matrix, ultimate, np.fliplr(ultimate))
        logging.info('\n\n%s\n%s\n%s\n', matrix, penultimate, np.fliplr(penultimate))

        return matrix.shape

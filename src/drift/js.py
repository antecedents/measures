import logging

import numpy as np


class JS:

    def __init__(self):
        pass

    @staticmethod
    def exc(matrix: np.ndarray):
        """

        :param matrix:
        :return:
        """

        logging.info(type(matrix.shape))

        return matrix.shape

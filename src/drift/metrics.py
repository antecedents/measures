import logging

import numpy as np
import pandas as pd
import scipy.spatial as spa
import scipy.stats as sta


class Metrics:

    def __init__(self):
        pass

    @staticmethod
    def __get_js(penultimate, ultimate):

        # noinspection PyArgumentList
        scores = spa.distance.jensenshannon(p=penultimate, q=ultimate, axis=1)
        logging.info(scores)


    def __get_wasserstein(self, x: np.ndarray, y: np.ndarray):

        logging.info(sta.wasserstein_distance(x, y))

    def exc(self, matrix: np.ndarray) -> tuple:
        """

        :param matrix:
        :return:
        """

        ultimate = matrix[:-1, :]
        penultimate = matrix[1:, :]

        ultimate = np.fliplr(ultimate)
        penultimate = np.fliplr(penultimate)

        self.__get_js(penultimate=penultimate, ultimate=ultimate)

        scores = [self.__get_wasserstein(penultimate[i,:], ultimate[i,:]) for i in np.arange(ultimate.shape[0])]
        logging.info(scores)


        return matrix.shape

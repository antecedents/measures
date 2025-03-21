import logging

import numpy as np
import pandas as pd
import scipy.spatial as spa
import scipy.stats as sta


class Metrics:

    def __init__(self):
        pass

    @staticmethod
    def __get_js(penultimate: np.ndarray, ultimate: np.ndarray):

        # noinspection PyArgumentList
        return spa.distance.jensenshannon(p=penultimate, q=ultimate, axis=1)

    @staticmethod
    def __get_wasserstein(penultimate: np.ndarray, ultimate: np.ndarray) -> float:

        return sta.wasserstein_distance(penultimate, ultimate).__float__()

    def exc(self, matrix: np.ndarray) -> tuple:
        """

        :param matrix:
        :return:
        """

        ultimate = matrix[:-1, :]
        penultimate = matrix[1:, :]

        ultimate = np.fliplr(ultimate)
        penultimate = np.fliplr(penultimate)

        js = self.__get_js(penultimate=penultimate, ultimate=ultimate)
        logging.info(len(js))

        wasserstein = [self.__get_wasserstein(penultimate[i,:], ultimate[i,:]) for i in np.arange(ultimate.shape[0])]
        logging.info(type(wasserstein))


        return matrix.shape

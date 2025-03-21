import logging
import typing

import numpy as np
import pandas as pd
import scipy.spatial as spa
import scipy.stats as sta


class Metrics:

    def __init__(self):
        pass

    @staticmethod
    def __get_js(penultimate: np.ndarray, ultimate: np.ndarray) -> np.ndarray | float:
        """

        :param penultimate:
        :param ultimate:
        :return:
        """

        # noinspection PyArgumentList
        return spa.distance.jensenshannon(p=penultimate, q=ultimate, axis=1)

    @staticmethod
    def __get_wasserstein(penultimate: np.ndarray, ultimate: np.ndarray) -> float:
        """

        :param penultimate:
        :param ultimate:
        :return:
        """

        # noinspection PyTypeChecker
        return sta.wasserstein_distance(penultimate, ultimate).__float__()

    @staticmethod
    def __get_matrices(matrix: np.ndarray) -> typing.Tuple[np.ndarray, np.ndarray]:
        """

        :param matrix:
        :return:
        """

        penultimate = matrix[1:, :]
        ultimate = matrix[:-1, :]

        return np.fliplr(penultimate), np.fliplr(ultimate)

    def exc(self, matrix: np.ndarray) -> tuple:
        """

        :param matrix:
        :return:
        """

        penultimate, ultimate = self.__get_matrices(matrix=matrix)

        js = self.__get_js(penultimate=penultimate, ultimate=ultimate)
        wasserstein = [self.__get_wasserstein(penultimate[i,:], ultimate[i,:]) for i in np.arange(ultimate.shape[0])]
        logging.info('SCORES: %s, %s', type(js), type(wasserstein))

        return matrix.shape

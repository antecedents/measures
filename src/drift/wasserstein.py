import logging

import numpy as np
import scipy.stats as sta
import scipy.spatial as spa


class Wasserstein:

    def __init__(self, period: int):
        """

        :param period: This is ...
        """

        self.__period = period

    def __get__metric(self, measure: np.ndarray, address: int) -> float:
        """

        :param measure:
        :param address:
        :return:
        """

        left: np.ndarray = measure[(address - 2*self.__period):(address - self.__period)]
        right: np.ndarray = measure[(address - self.__period):address]

        return sta.wasserstein_distance(left, right)

    def exc(self, measure: np.ndarray):
        """

        :param measure: measure = data['n_attendances'].values
        :return:
        """

        # For later test unit
        logging.info(sta.wasserstein_distance(measure[:52], measure[:52]))
        logging.info(sta.wasserstein_distance(measure[:52], measure[52:104]))

        # Pointer addresses
        addresses = np.arange(start=2*self.__period, stop=measure.shape[0])

        # Wasserstein scores vis-à-vis mutually exclusive windows
        scores = [np.apply_along_axis(self.__get__metric, 0, measure, address) for address in addresses]
        logging.info(type(scores))

        return scores

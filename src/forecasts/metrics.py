import logging

import numpy as np
import pandas as pd

import src.elements.parts as pr


class Metrics:

    def __init__(self):
        pass

    @staticmethod
    def __root_mse(data: pd.DataFrame):
        """
        Root of the mean (of the square of the error per point); lower & upper boundary

        :param data:
        :return:
        """

        se: np.ndarray = np.power(data[['l_error', 'u_error']].to_numpy(), 2)
        mse = np.sum(se, axis=0)/se.shape[0]
        logging.info(np.sqrt(mse))

    @staticmethod
    def __average_percentage(data: pd.DataFrame):
        """
        The average of the (percentage absolute error rate per point)

        :return:
        """

        er = np.absolute(data[['l_error_rate', 'u_error_rate']].to_numpy())
        mer = np.sum(er, axis=0)/er.shape[0]
        logging.info(100*mer)

    @staticmethod
    def __median_percentage(data: pd.DataFrame):
        """

        :param data:
        :return:
        """

        er = np.absolute(data[['l_error_rate', 'u_error_rate']].to_numpy())
        logging.info(100*np.median(er, axis=0))

    def exc(self, parts: pr.Parts):
        """

        :param parts:
        :return:
        """

        data = parts.estimates
        self.__root_mse(data=data)
        self.__average_percentage(data=data)
        self.__median_percentage(data=data)

        er = np.absolute(data[['l_error_rate', 'u_error_rate']].to_numpy())
        logging.info(np.percentile(a=er, q=[10, 25, 50, 75, 90], axis=0))

import logging

import numpy as np

import src.elements.parts as pr


class Metrics:

    def __init__(self):
        pass

    @staticmethod
    def __root_mse(references: np.ndarray, forecasts: np.ndarray):
        """
        
        :param references:
        :param forecasts:
        :return:
        """

        sqe: np.ndarray = np.power(references - forecasts, 2)
        logging.info(sqe)

        mse: float = sum(sqe)/sqe.shape[0]
        logging.info(mse)

        logging.info(np.sqrt(mse))

    def __percentage(self):
        """
        100*sum(abs(error./original))/N <- mean absolute percentage error

        :return:
        """

    def exc(self, parts: pr.Parts):
        """

        :param parts:
        :return:
        """

        self.__root_mse(references=parts.estimates['n_attendances'], forecasts=parts.estimates['l_estimate'])

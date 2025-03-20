"""Module measures.py"""
import logging

import numpy as np
import pandas as pd

import src.elements.parts as pr


class Measures:

    def __init__(self):
        pass

    @staticmethod
    def __errors(data: pd.DataFrame) -> pd.DataFrame:
        """
        errors.sort(axis=1)

        :param data: The forecasts w.r.t. training or testing phases.
        :return:
        """

        # ground truth
        ground = data['n_attendances'].to_numpy()[:,None]

        # forecasts
        forecasts = data[['l_estimate', 'u_estimate']].to_numpy()

        # raw errors and error rates
        errors: np.ndarray =  ground - forecasts
        data.loc[:, ['l_e_error', 'u_e_error']] = errors
        data.loc[:, ['l_e_error_rate', 'u_e_error_rate']] = np.true_divide(errors, ground)

        return data

    def exc(self, parts: pr.Parts) -> pr.Parts:
        """

        :param parts: An institution's data object consisting of forecasts w.r.t. training,
                      testing, and futures phases.
        :return:
        """

        parts = parts._replace(estimates=self.__errors(data=parts.estimates.copy()),
                       tests=self.__errors(data=parts.tests.copy()))

        logging.info(parts.estimates.head())
        logging.info(parts.tests.head())
        logging.info(parts.futures.head())

        return parts

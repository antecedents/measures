"""Module boundaries.py"""
import numpy as np
import pandas as pd
import scipy.stats as sta

import src.elements.parts as pr


class Boundaries:
    """
    <b>Notes</b><br>
    ------<br>
    This class determines estimations boundaries vis-à-vis estimations samples.<br>
    """

    def __init__(self):
        """
        Constructor
        """

        self.__span = 0.90

    @staticmethod
    def __metric(period: float, average: float, deviation: float, percentile: float) -> float:
        """
        period + average + (z-score * standard deviation)

        :param period:  An institution's seasonal component estimates.
        :param average: The averages of the samples of an institution's trend component estimates.
        :param deviation: The standard deviations of the trend component estimates samples.
        :param percentile: The percentile boundary of interest.
        :return:
        """

        score = sta.norm.ppf(percentile)

        return period + average + (score * deviation)

    @staticmethod
    def __e_series(data: pd.DataFrame) -> pd.DataFrame:
        """
        Estimates and tests, only.

        :param data: The forecasts w.r.t. training or testing phases.
        :return:
        """

        # ground truth, forecasts
        ground = data['n_attendances'].to_numpy()[:,None]
        forecasts = data[['l_estimate', 'u_estimate']].to_numpy()

        # raw errors and error rates; negative/lower, positive/higher
        errors: np.ndarray =  forecasts - ground
        data.loc[:, ['l_e_error', 'u_e_error']] = errors
        data.loc[:, ['l_e_ep', 'u_e_ep']] = 100 * np.true_divide(errors, ground)

        return data

    @staticmethod
    def __e_trend(data: pd.DataFrame) -> pd.DataFrame:
        """
        Estimates only.

        :param data: The forecasts w.r.t. training or testing phases.
        :return:
        """

        # ground truth, forecasts, error percentages; negative/lower, positive/higher
        ground = data['trend'].to_numpy()[:,None]
        forecasts = data[['l_tc_estimate', 'u_tc_estimate']].to_numpy()
        data.loc[:, ['l_tc_ep', 'u_tc_ep']] = 100 * np.true_divide(forecasts - ground, ground)

        return data

    def __add_boundaries(self, data: pd.DataFrame) -> pd.DataFrame:
        """

        :param data:
        :return:
        """

        data['l_estimate'] = self.__metric(
            period = data['sc_estimate'], average=data['tc_estimate'], deviation=data['tc_estimate_deviation'],
            percentile=0.5 - 0.5*self.__span)
        data['u_estimate'] = self.__metric(
            period = data['sc_estimate'], average=data['tc_estimate'], deviation=data['tc_estimate_deviation'],
            percentile=0.5 + 0.5*self.__span)

        data['l_tc_estimate'] = data['l_estimate'] - data['sc_estimate']
        data['u_tc_estimate'] = data['u_estimate'] - data['sc_estimate']

        return data

    def exc(self, parts: pr.Parts) -> pr.Parts:
        """

        :param parts:
        :return:
        """

        estimates = self.__add_boundaries(data=parts.estimates.copy())
        tests = self.__add_boundaries(data=parts.tests.copy())
        futures = self.__add_boundaries(data=parts.futures.copy())

        estimates = self.__e_series(data=estimates.copy())
        tests = self.__e_series(data=tests.copy())

        estimates = self.__e_trend(data=estimates.copy())

        parts = parts._replace(estimates=estimates, tests=tests, futures=futures)

        return parts

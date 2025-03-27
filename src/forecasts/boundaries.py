"""Module boundaries.py"""
import pandas as pd

import scipy.stats as sta
import src.elements.parts as pr


class Boundaries:
    """
    <b>Notes</b><br>
    ------<br>

    Estimations boundaries.

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

        parts._replace(estimates=estimates, tests=tests, futures=futures)

        return parts

"""Module metrics.py"""
import pandas as pd
import scipy.stats as sta

import src.elements.parts as pr


class Metrics:
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
    def __get_metric(data: pd.DataFrame, percentile: float) -> float:
        """
        period + average + (z-score * standard deviation)

        period:  An institution's seasonal component estimates.
        average: The averages of the samples of an institution's trend component estimates.
        deviation: The standard deviations of the trend component estimates samples.

        :param data: The data
        :param percentile: The percentile boundary of interest.
        :return:
        """

        score = sta.norm.ppf(percentile)

        period = data['sc_estimate']
        average = data['tc_estimate']
        deviation = data['tc_estimate_deviation']

        return period + average + (score * deviation)


    def __get_boundaries(self, data: pd.DataFrame) -> pd.DataFrame:
        """

        :param data:
        :return:
        """

        data['l_estimate'] = self.__get_metric(data=data, percentile=0.5 - 0.5*self.__span)
        data['u_estimate'] = self.__get_metric(data=data, percentile=0.5 + 0.5*self.__span)

        return data

    def exc(self, parts: pr.Parts) -> pr.Parts:
        """

        :param parts:
        :return:
        """

        estimates = self.__get_boundaries(data=parts.estimates.copy())
        tests = self.__get_boundaries(data=parts.tests.copy())
        futures = self.__get_boundaries(data=parts.futures.copy())

        parts = parts._replace(estimates=estimates, tests=tests, futures=futures)

        return parts

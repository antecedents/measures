"""Module parts.py"""
import typing

import numpy as np
import pandas as pd
import scipy.stats as sta

import src.elements.parts as pr
import src.elements.seasonal as sa


class Parts:
    """
    <b>Notes</b><br>
    ------<br>
    """

    def __init__(self):
        """
        Constructor
        """

        self.__span = 0.90

        # The fields in focus, and descriptive names
        self.__fields = ['milliseconds', 'week_ending_date', 'n_attendances', 'seasonal_est', 'mu', 'std']
        self.__rename = {'seasonal_est': 'sc_estimate', 'mu': 'tc_estimate',
                         'std': 'tc_estimate_deviation'}

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

    def __get_parts(self, seasonal: sa.Seasonal, trend: pd.DataFrame) \
            -> typing.Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """

        :param seasonal:
        :param trend:
        :return:
        """

        estimates = seasonal.estimates.merge(trend, how='left', on='week_ending_date')
        tests = seasonal.tests.merge(trend, how='left', on='week_ending_date')
        futures = seasonal.futures.merge(trend, how='left', on='week_ending_date')
        futures['n_attendances'] = np.nan

        return (estimates[self.__fields].rename(columns=self.__rename),
                tests[self.__fields].rename(columns=self.__rename),
                futures[self.__fields].rename(columns=self.__rename))

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

        return data

    def exc(self, seasonal: sa.Seasonal, trend: pd.DataFrame) -> pr.Parts:
        """

        :param seasonal: The seasonal components estimations.
        :param trend: The trend components estimations.
        :return:
        """

        estimates, tests, futures = self.__get_parts(seasonal=seasonal, trend=trend)

        estimates = self.__add_boundaries(data=estimates.copy())
        tests = self.__add_boundaries(data=tests.copy())
        futures = self.__add_boundaries(data=futures.copy())

        return pr.Parts(estimates=estimates, tests=tests, futures=futures)

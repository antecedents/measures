
import pandas as pd
import numpy as np

import scipy.stats as sta

import src.elements.seasonal as sa

class Points:

    def __init__(self):

        self.__span = 0.90

        self.__fields = ['week_ending_date', 'n_attendances', 'seasonal_est', 'mu', 'std']
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

    def __set_data(self, seasonal: sa.Seasonal, trend: pd.DataFrame) -> pd.DataFrame:
        """

        :param seasonal:
        :param trend:
        :return:
        """

        training = seasonal.estimates.merge(trend, how='left', on='week_ending_date')
        testing = seasonal.tests.merge(trend, how='left', on='week_ending_date')
        futures = seasonal.futures.merge(trend, how='left', on='week_ending_date')
        futures['n_attendances'] = np.nan

        data = pd.concat((training[self.__fields], testing[self.__fields], futures[self.__fields]),
                         axis=0, ignore_index=True)

        return data.rename(columns=self.__rename)

    def exc(self, seasonal: sa.Seasonal, trend: pd.DataFrame) -> pd.DataFrame:
        """

        :param seasonal:
        :param trend:
        :return:
        """

        data = self.__set_data(seasonal=seasonal, trend=trend)

        data['u_estimate'] = self.__metric(
            period = data['sc_estimate'], average=data['tc_estimate'], deviation=data['tc_estimate_deviation'],
            percentile=(0.5 + 0.5*self.__span))
        data['l_estimate'] = self.__metric(
            period = data['sc_estimate'], average=data['tc_estimate'], deviation=data['tc_estimate_deviation'],
            percentile=(0.5 - 0.5*self.__span))

        return data

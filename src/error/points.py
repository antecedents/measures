
import pandas as pd
import numpy as np

import scipy.stats as sta

import src.elements.seasonal as sa

class Points:

    def __init__(self):

        self.__span = 0.90

        # self__rename = {'seasonal_est': 'sc_estimate', 'mu': 'tc_estimate',
        #                'std': 'tc_estimate_deviation'}

    @staticmethod
    def __milliseconds(blob: pd.DataFrame):

        frame = blob.copy()
        frame['milliseconds']  = (
                frame['week_ending_date'].to_numpy().astype(np.int64) / (10 ** 6)
        ).astype(np.longlong)
        frame.sort_values(by='week_ending_date', inplace=True)

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

    def exc(self, seasonal: sa.Seasonal, trend: pd.DataFrame):
        """
        
        :param seasonal:
        :param trend:
        :return:
        """

        training = seasonal.estimates.merge(trend, how='left', on='week_ending_date')
        testing = seasonal.tests.merge(trend, how='left', on='week_ending_date')
        futures = seasonal.futures.merge(trend, how='left', on='week_ending_date')
        futures['n_attendances'] = np.nan

        fields = ['week_ending_date', 'n_attendances', 'seasonal_est', 'mu', 'std']
        data = pd.concat((training[fields], testing[fields], futures[fields]), axis=0, ignore_index=True)

        data['u_estimate'] = self.__metric(
            period = data['seasonal_est'], average=data['mu'], deviation=data['std'], percentile=(0.5 + 0.5*self.__span))
        data['l_estimate'] = self.__metric(
            period = data['seasonal_est'], average=data['mu'], deviation=data['std'], percentile=(0.5 - 0.5*self.__span))

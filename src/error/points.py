import logging
import pandas as pd


import scipy.stats as sta

import src.elements.seasonal as sa

class Points:

    def __init__(self):
        pass

    @staticmethod
    def __metric(period: float, average: float, deviation: float, percentile: float) -> float:

        score = sta.norm.ppf(percentile)

        return period + average + (score * deviation)


    def exc(self, seasonal: sa.Seasonal, trend: pd.DataFrame):
        """
        Focus
            estimated mean + (z-score * standard deviation)
        whereby
            z-score = sci.norm.ppf(percentile value)

        :return:
        """

        training = seasonal.estimates.merge(trend, how='left', on='week_ending_date')
        # _tests = seasonal.tests.merge(trend, how='left', on='week_ending_date')
        # _futures = seasonal.futures.merge(trend, how='left', on='week_ending_date')

        training['upper'] = self.__metric(
            period = training['seasonal_est'], average=training['mu'], deviation=training['std'], percentile=0.75)
        logging.info(training)

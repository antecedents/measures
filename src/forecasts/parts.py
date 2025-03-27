"""Module parts.py"""
import typing

import numpy as np
import pandas as pd

import config
import src.elements.parts as pr
import src.elements.seasonal as sa
import src.elements.text_attributes as txa
import src.functions.streams


class Parts:
    """
    <b>Notes</b><br>
    ------<br>
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

        # ...
        self.__streams = src.functions.streams.Streams()

        # The fields in focus, and descriptive names
        self.__fields = ['milliseconds', 'week_ending_date', 'n_attendances', 'seasonal_est', 'mu', 'std']
        self.__rename = {'seasonal_est': 'sc_estimate', 'mu': 'tc_estimate',
                         'std': 'tc_estimate_deviation'}

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

    def __append_features(self, uri: str):
        """

        :param uri:
        :return:
        """

        text = txa.TextAttributes(uri=uri, header=0)
        self.__streams.read(text=text)

    def exc(self, seasonal: sa.Seasonal, trend: pd.DataFrame) -> pr.Parts:
        """

        :param seasonal: The seasonal components estimations.
        :param trend: The trend components estimations.
        :return:
        """

        estimates, tests, futures = self.__get_parts(seasonal=seasonal, trend=trend)

        return pr.Parts(estimates=estimates, tests=tests, futures=futures)

"""Module """
import glob
import logging
import os
import pathlib

import config
import src.elements.seasonal as sa
import src.error.seasonal
import src.error.trend


class Interface:
    """
    Interface
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

        self.__trend = src.error.trend.Trend()

    def __get_codes(self) -> list[str] | None:
        """

        :return:
        """

        listings = glob.glob(pathname=os.path.join(self.__configurations.data_, 'models', '**'))

        codes = []
        for listing in listings:
            state = (pathlib.Path(os.path.join(listing, 'scf_estimates.json')).exists() &
                     pathlib.Path(os.path.join(listing, 'tcf_forecasts.csv')).exists())
            if state:
                codes.append(os.path.basename(listing))

        return codes

    def exc(self):
        """

        :return:
        """

        codes = self.__get_codes()

        for code in codes:
            seasonal: sa.Seasonal = src.error.seasonal.Seasonal(code=code).exc()
            trend = self.__trend.exc(code=code)

            _estimates = seasonal.estimates.merge(trend, how='left', on='week_ending_date')
            _tests = seasonal.tests.merge(trend, how='left', on='week_ending_date')
            _futures = seasonal.futures.merge(trend, how='left', on='week_ending_date')

            logging.info(_estimates.head())
            logging.info(_tests.head())
            logging.info(_futures.head())

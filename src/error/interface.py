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
        logging.info(codes)

        for code in codes:
            seasonal: sa.Seasonal = src.error.seasonal.Seasonal(code=code).exc()
            logging.info(seasonal.estimates.head())
            logging.info(seasonal.tests.head())
            logging.info(seasonal.futures.head())

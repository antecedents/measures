import glob
import logging
import os
import pathlib

import pandas as pd

import config
import src.functions.objects


class Error:
    """
    Steps
    """

    def __init__(self):
        """

        """

        self.__configurations = config.Config()
        self.__objects = src.functions.objects.Objects()

    def exc(self):
        """

        :return:
        """

        listings = glob.glob(pathname=os.path.join(self.__configurations.data_, 'models', '**'))
        logging.info(listings)

        codes = []
        for listing in listings:
            state = (pathlib.Path(os.path.join(listing, 'scf_estimates.json')).exists() &
                     pathlib.Path(os.path.join(listing, 'tcf_forecasts.csv')).exists())
            if state:
                codes.append(os.path.basename(listing))

        logging.info(codes)

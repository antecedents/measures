"""Module interface.py"""
import os
import logging
import glob

import config


class Interface:

    def __init__(self):
        """

        """

        self.__configurations = config.Config()

    def exc(self):
        """

        :return:
        """

        listings = glob.glob(
            pathname=os.path.join(self.__configurations.data_, 'data', '**', 'features.csv'))
        logging.info(listings)

        codes = [os.path.basename(os.path.dirname(listing)) for listing in listings]
        logging.info(codes)

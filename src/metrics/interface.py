import glob
import logging
import os

import pandas as pd

import config
import src.functions.objects


class Interface:

    def __init__(self):

        self.__configurations = config.Config()
        self.__objects = src.functions.objects.Objects()

    def exc(self):

        logging.info('Starting ....')

        listings = glob.glob(
            pathname=os.path.join(self.__configurations.data_, 'models', '**', 'scf_estimates.json'))
        logging.info(listings)

        for listing in listings:

            nodes = self.__objects.read(uri=listing)
            estimates = pd.DataFrame.from_dict(nodes['estimates'], orient='index')
            logging.info(estimates.head())

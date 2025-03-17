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

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n\n',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def exc(self):

        self.__logger.info('Starting ....')

        listings = glob.glob(
            pathname=os.path.join(self.__configurations.data_, 'models', '**', 'scf_estimates.json'))
        self.__logger.info(listings)

        for listing in listings:

            nodes = self.__objects.read(uri=listing)
            estimates = pd.DataFrame.from_dict(nodes['estimates'], orient='index')
            self.__logger.info(estimates.head())

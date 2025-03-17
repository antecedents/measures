import glob
import logging
import os
import pathlib

import config
import src.elements.seasonal as sa
import src.error.seasonal


class Error:
    """
    Steps
    """

    def __init__(self):
        """

        """

        self.__configurations = config.Config()

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
        for code in codes:

            seasonal: sa.Seasonal = src.error.seasonal.Seasonal(code=code).exc()
            logging.info(seasonal.estimates.head())



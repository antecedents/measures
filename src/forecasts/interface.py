"""Module """
import glob
import os
import pathlib

import pandas as pd

import config
import src.elements.parts as pr
import src.elements.seasonal as sa
import src.forecasts.metrics
import src.forecasts.parts
import src.forecasts.seasonal
import src.forecasts.trend
import src.forecasts.measures


class Interface:
    """
    Interface
    """

    def __init__(self, arguments: dict):
        """

        :param arguments: A set of model development, and supplementary, arguments.
        """

        self.__arguments = arguments

        # Configurations
        self.__configurations = config.Config()

        # Instances
        self.__seasonal = src.forecasts.seasonal.Seasonal()
        self.__trend = src.forecasts.trend.Trend()
        self.__parts = src.forecasts.parts.Parts()
        self.__measures = src.forecasts.measures.Measures()
        self.__metrics = src.forecasts.metrics.Metrics()

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
            seasonal: sa.Seasonal = self.__seasonal.exc(code=code)
            trend: pd.DataFrame = self.__trend.exc(code=code)
            parts: pr.Parts = self.__parts.exc(seasonal=seasonal, trend=trend)
            parts: pr.Parts = self.__measures.exc(parts=parts)
            self.__metrics.exc(parts=parts)

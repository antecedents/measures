"""Module """
import logging
import os

import dask
import pandas as pd

import config
import src.elements.parts as pr
import src.elements.seasonal as sa
import src.elements.specifications as se
import src.forecasts.parts
import src.forecasts.seasonal
import src.forecasts.trend
import src.functions.directories
import src.noise.quantiles


class Interface:
    """
    Interface
    """

    def __init__(self, reference: pd.DataFrame):
        """

        :param reference:
        """

        self.__reference = reference

        # Configurations
        self.__configurations = config.Config()

        # Instances
        self.__seasonal = dask.delayed(src.forecasts.seasonal.Seasonal().exc)
        self.__trend = dask.delayed(src.forecasts.trend.Trend().exc)
        self.__parts = dask.delayed(src.forecasts.parts.Parts().exc)

    def __directories(self):
        """

        :return:
        """

        directories = src.functions.directories.Directories()

        for section in ['quantiles', 'adjusting']:
            path = os.path.join(self.__configurations.points_, section)
            directories.create(path)

    def exc(self, specifications_: list[se.Specifications]):
        """

        :return:
        """

        # Ensure the storage directories exist; measures -> forecasts, metrics -> errors
        self.__directories()

        # Delayed task
        __quantiles = dask.delayed(src.noise.quantiles.Quantiles().exc)

        # Hence
        computations = []
        for specifications in specifications_:

            seasonal: sa.Seasonal = self.__seasonal(code=specifications.hospital_code)
            trend: pd.DataFrame = self.__trend(code=specifications.hospital_code)
            parts: pr.Parts = self.__parts(seasonal=seasonal, trend=trend, code=specifications.hospital_code)
            quantiles: pd.Series = __quantiles(code=specifications.hospital_code)

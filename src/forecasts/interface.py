"""Module """
import glob
import os

import dask
import pandas as pd

import config
import src.elements.parts as pr
import src.elements.seasonal as sa
import src.forecasts.measures
import src.forecasts.metrics
import src.forecasts.parts
import src.forecasts.seasonal
import src.forecasts.trend
import src.functions.directories
import src.specifications


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
        self.__seasonal = dask.delayed(src.forecasts.seasonal.Seasonal().exc)
        self.__trend = dask.delayed(src.forecasts.trend.Trend().exc)
        self.__parts = dask.delayed(src.forecasts.parts.Parts().exc)
        self.__measures = dask.delayed(src.forecasts.measures.Measures().exc)
        self.__metrics = dask.delayed(src.forecasts.metrics.Metrics().exc)

    def __directories(self):
        """

        :return:
        """

        directories = src.functions.directories.Directories()

        for section in ['forecasts', 'errors']:
            self.__path = os.path.join(self.__configurations.points_, section)
            directories.create(self.__path)

    def exc(self, reference: pd.DataFrame):
        """

        :param reference:
        :return:
        """

        # Ensure the storage directories exist; measures -> forecasts, metrics -> errors
        self.__directories()

        # Specifications
        specifications = dask.delayed(src.specifications.Specifications(reference=reference))

        # Hence
        codes = reference['hospital_code'].unique()
        for code in codes:
            specifications = specifications(code=code)
            seasonal: sa.Seasonal = self.__seasonal(code=code)
            trend: pd.DataFrame = self.__trend(code=code)
            parts: pr.Parts = self.__parts(seasonal=seasonal, trend=trend)
            parts: pr.Parts = self.__measures(parts=parts, specifications=specifications)
            self.__metrics(parts=parts, specifications=specifications)

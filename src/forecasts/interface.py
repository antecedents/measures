"""Module """
import logging
import os

import dask
import pandas as pd

import config
import src.elements.parts as pr
import src.elements.seasonal as sa
import src.elements.specifications as se
import src.forecasts.measures
import src.forecasts.metrics
import src.forecasts.parts
import src.forecasts.seasonal
import src.forecasts.trend
import src.functions.directories


class Interface:
    """
    Interface
    """

    def __init__(self, reference: pd.DataFrame, arguments: dict):
        """

        :param reference:
        :param arguments: A set of model development, and supplementary, arguments.
        """

        self.__reference = reference
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

    @dask.delayed
    def __get__specifications(self, code: str) -> se.Specifications:
        """

        :param code:
        :return:
        """

        values: pd.Series =  self.__reference.loc[self.__reference['hospital_code'] == code, :].squeeze(axis=0)
        dictionary = values.to_dict()

        return se.Specifications(**dictionary)

    def exc(self):
        """

        :return:
        """

        # Ensure the storage directories exist; measures -> forecasts, metrics -> errors
        self.__directories()

        # Hence
        codes = self.__reference['hospital_code'].unique()
        computations = []
        for code in codes:
            specifications = self.__get__specifications(code=code)
            seasonal: sa.Seasonal = self.__seasonal(code=code)
            trend: pd.DataFrame = self.__trend(code=code)
            parts: pr.Parts = self.__parts(seasonal=seasonal, trend=trend)
            parts_: pr.Parts = self.__measures(parts=parts, specifications=specifications)
            message = self.__metrics(parts=parts_, specifications=specifications)
            computations.append(message)
        messages = dask.compute(computations, scheduler='threads')[0]

        logging.info(messages)

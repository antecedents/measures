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

        for section in ['forecasts', 'errors']:
            path = os.path.join(self.__configurations.points_, section)
            directories.create(path)

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

        # Delayed tasks
        measures = dask.delayed(src.forecasts.measures.Measures().exc)
        metrics = dask.delayed(src.forecasts.metrics.Metrics().exc)

        # Hence
        codes = self.__reference['hospital_code'].unique()
        computations = []
        for code in codes:
            specifications = self.__get__specifications(code=code)
            seasonal: sa.Seasonal = self.__seasonal(code=code)
            trend: pd.DataFrame = self.__trend(code=code)
            parts: pr.Parts = self.__parts(seasonal=seasonal, trend=trend)
            parts_: pr.Parts = measures(parts=parts, specifications=specifications)
            message = metrics(parts=parts_, specifications=specifications)
            computations.append(message)
        messages = dask.compute(computations, scheduler='threads')[0]

        logging.info(messages)

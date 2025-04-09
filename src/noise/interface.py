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
import src.noise.boundaries
import src.noise.persist
import src.noise.quantiles


class Interface:
    """
    Interface
    """

    def __init__(self):
        """
        Constructor
        """

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

        :param specifications_: A list of attributes per institution/hospital.
        :return:
        """

        # Ensure the storage directories exist; measures -> forecasts, metrics -> errors
        self.__directories()

        # Delayed task
        __quantiles = dask.delayed(src.noise.quantiles.Quantiles().exc)
        __boundaries = dask.delayed(src.noise.boundaries.Boundaries().exc)
        __persist = dask.delayed(src.noise.persist.Persist().exc)

        # Hence
        computations = []
        for specifications in specifications_:
            seasonal: sa.Seasonal = self.__seasonal(code=specifications.hospital_code)
            trend: pd.DataFrame = self.__trend(code=specifications.hospital_code)
            parts: pr.Parts = self.__parts(seasonal=seasonal, trend=trend, code=specifications.hospital_code)
            quantiles: pd.DataFrame = __quantiles(specifications=specifications)
            parts_ = __boundaries(parts=parts, quantiles=quantiles)
            message = __persist(parts=parts_)
            computations.append(message)

        messages = dask.compute(computations, scheduler='threads')[0]

        logging.info(messages)

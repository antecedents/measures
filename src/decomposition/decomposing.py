import logging

import dask
import numpy as np
import pandas as pd
import statsmodels.tsa.seasonal as stl

import config
import src.decomposition.structuring


class Decomposing:

    def __init__(self, data: pd.DataFrame):
        """

        :param data: The index is a DatetimeIndex, which is necessary for the decomposition algorithm
        """

        self.__data = data

        self.__configurations = config.Config()
        self.__structuring = src.decomposition.structuring.Structuring()

    @dask.delayed
    def __get_data(self, code: str) -> pd.DataFrame:

        return self.__data.copy()[self.__data['hospital_code'] == code, :]

    @dask.delayed
    def __decompose(self, frame: pd.DataFrame) -> stl.DecomposeResult:

        parts = stl.seasonal_decompose(
            x=frame['n_attendances'], model='additive', period=self.__configurations.seasons)

        return parts

    @dask.delayed
    def __exc_structuring(self, parts: stl.DecomposeResult) -> pd.DataFrame:

        return self.__structuring.exc(parts=parts)

    def exc(self):

        codes: np.ndarray = self.__data['hospital_code'].unique()

        computations = []
        for code in codes:
            logging.info(code)

            frame = self.__get_data(code=code)
            parts = self.__decompose(frame=frame)
            data = self.__exc_structuring(parts=parts)

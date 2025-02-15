import logging

import dask
import numpy as np
import pandas as pd
import statsmodels.tsa.seasonal as stl

import config


class Decomposing:

    def __init__(self, data: pd.DataFrame):
        """

        :param data: The index is a DatetimeIndex, which is necessary for the decomposition algorithm
        """

        self.__data = data

        self.__configurations = config.Config()

    @dask.delayed
    def __get_data(self, code: str) -> pd.DataFrame:

        return self.__data.copy()[self.__data['hospital_code'] == code, :]

    @dask.delayed
    def __decompose(self, blob: pd.DataFrame) -> stl.DecomposeResult:

        parts = stl.seasonal_decompose(
            x=blob['n_attendances'], model='additive', period=self.__configurations.seasons)

        return parts

    def exc(self):

        codes: np.ndarray = self.__data['hospital_code'].unique()

        computations = []
        for code in codes:
            logging.info(code)

            data = self.__get_data(code=code)
            parts = self.__decompose(blob=data)



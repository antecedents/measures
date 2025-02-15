import logging
import pandas as pd
import numpy as np
import dask

import statsmodels.tsa.seasonal as stl

import config

class Decompose:

    def __init__(self, data: pd.DataFrame):

        self.__data = data

        self.__configurations = config.Config()

    @dask.delayed
    def __slice(self, code: str) -> pd.DataFrame:

        return self.__data.copy()[self.__data['hospital_code'] == code, :]

    @dask.delayed
    def __decompose(self, blob: pd.DataFrame):

        parts = stl.seasonal_decompose(
            x=blob['n_attendances'], model='additive', period=self.__configurations.seasons)

    def exc(self):

        codes: np.ndarray = self.__data['hospital_code'].unique()

        for code in codes:
            logging.info(code)


import pandas as pd
import numpy as np
import dask

import statsmodels.tsa.seasonal as stsl

class Decompose:

    def __init__(self, data: pd.DataFrame):

        self.__data = data

    def exc(self):

        codes: np.ndarray = self.__data['hospital_code'].unique()

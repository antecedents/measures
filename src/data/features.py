"""Module features.py"""
import dask
import numpy as np
import pandas as pd

import config


class Features:
    """
    Features
    """

    def __init__(self, data: pd.DataFrame):
        """

        :param data: The data.
        """

        self.__data = data.copy()

        # Configurations
        self.__configurations = config.Config()

    @dask.delayed
    def __features(self, code: str):
        """

        :param code:
        :return:
        """

        blob = self.__data.copy().loc[self.__data['hospital_code'] == code, :]

        blob['ln'] = np.log(blob['n_attendances'].to_numpy())
        blob['d_of_ln'] = blob['ln'].diff(periods=self.__configurations.seasons)
        blob['d_of_ln'] = blob['d_of_ln'].diff(periods=self.__configurations.trends)

        # Sort
        blob.sort_values(by='week_ending_date', ascending=True, inplace=True)

        return blob

    def exc(self) -> pd.DataFrame:
        """

        :return:
        """

        # The institution, hospital, codes.
        codes = self.__data['hospital_code'].unique()

        # Add features per institution.
        computations = []
        for code in codes:
            computations.append(self.__features(code=code))
        calculations = dask.compute(computations, scheduler='threads')[0]

        # Structure
        blob = pd.concat(calculations, axis=0, ignore_index=True)

        return blob

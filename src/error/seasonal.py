"""Module seasonal.py"""
import os

import pandas as pd

import config
import src.elements.seasonal as sa
import src.functions.objects


class Seasonal:
    """
    <b>Notes</b><br>
    ------<br>

    Retrieves the seasonal component forecasting estimations<br>
    """

    def __init__(self, code: str):
        """

        :param code: The identification code of an institution/hospital.
        """

        self.__configurations = config.Config()

        # Data path
        uri = os.path.join(self.__configurations.data_, 'models', code, 'scf_estimates.json')

        # Reading-in the seasonal component forecasting data
        self.__data = src.functions.objects.Objects().read(uri=uri)

    def __get_section(self, section: str) ->pd.DataFrame:
        """

        :param section: A data section of the estimations dictionary
        :return:
        """

        frame = pd.DataFrame.from_dict(self.__data[section], orient='tight')

        frame['week_ending_date'] = pd.to_datetime(
            frame['date'].astype(str), errors='coerce', format='%Y-%m-%d')
        frame.drop(columns='date', inplace=True)
        frame.sort_values(by='week_ending_date', ascending=True, inplace=True)

        return frame

    def exc(self) -> sa.Seasonal:
        """

        :return:
        """

        return sa.Seasonal(
            estimates=self.__get_section(section='estimates').drop(columns='seasonal'),
            tests=self.__get_section(section='tests'),
            futures=self.__get_section(section='futures'))

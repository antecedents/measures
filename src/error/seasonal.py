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

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

    @staticmethod
    def __get_section(data: dict, section: str) ->pd.DataFrame:
        """

        :param data:
        :param section: A data section of the estimations dictionary
        :return:
        """

        frame = pd.DataFrame.from_dict(data[section], orient='tight')

        frame['week_ending_date'] = pd.to_datetime(
            frame['date'].astype(str), errors='coerce', format='%Y-%m-%d')
        frame.drop(columns='date', inplace=True)
        frame.sort_values(by='week_ending_date', ascending=True, inplace=True)

        return frame

    def exc(self, code: str) -> sa.Seasonal:
        """

        :param code: The identification code of an institution/hospital.
        :return:
        """

        # Reading-in the seasonal component forecasting data
        uri = os.path.join(self.__configurations.data_, 'models', code, 'scf_estimates.json')
        data = src.functions.objects.Objects().read(uri=uri)

        return sa.Seasonal(
            estimates=self.__get_section(data=data, section='estimates').drop(columns='seasonal'),
            tests=self.__get_section(data=data, section='tests'),
            futures=self.__get_section(data=data, section='futures'))

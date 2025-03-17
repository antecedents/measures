import os
import logging

import pandas as pd

import config
import src.elements.seasonal as sa
import src.functions.objects


class Seasonal:
    """

    """

    def __init__(self, code: str):
        """

        :param code: The identification code of an institution/hospital
        """

        self.__configurations = config.Config()

        # For reading JSON files
        self.__objects = src.functions.objects.Objects()

        # Reading-in the seasonal component forecasting data
        uri = os.path.join(self.__configurations.data_, 'models', code, 'scf_estimates.json')
        logging.info(uri)
        self.__data = self.__objects.read(uri=uri)

    def __get_section(self, section: str):

        frame = pd.DataFrame.from_dict(self.__data[section], orient='tight')

        frame['week_ending_date'] = pd.to_datetime(
            frame['date'].astype(str), errors='coerce', format='%Y-%m-%d')

        frame.drop(columns='date', inplace=True)
        frame.sort_values(by='week_ending_date', ascending=True, inplace=True)

        return frame

    def exc(self):

        return sa.Seasonal(
            estimates=self.__get_section(section='estimates'),
            tests=self.__get_section(section='tests'),
            futures=self.__get_section(section='futures'))

"""Module persist.py"""
import logging
import os
import numpy as np
import pandas as pd
import json

import config
import src.functions.objects
import src.functions.directories


class Persist:

    def __init__(self):
        """

        """

        self.__fields = ['milliseconds', 'js', 'wasserstein', 'date']

        self.__configurations = config.Config()
        self.__objects = src.functions.objects.Objects()

        # Storage
        self.__path = os.path.join(self.__configurations.warehouse, 'drift')
        src.functions.directories.Directories().create(self.__path)

    def __get_dictionary(self, frame: pd.DataFrame):
        """

        :param frame:
        :param code:
        :return:
        """

        string: str = frame[self.__fields].to_json(orient='split')
        dictionary: dict = json.loads(string)

        code: pd.Series = frame[['health_board_code', 'hospital_code']].drop_duplicates().squeeze()
        dictionary['health_board_code'] = code.health_board_code
        dictionary['hospital_code'] = code.hospital_code

        return dictionary

    def exc(self, frame: pd.DataFrame, code: str) -> str:
        """

        :param frame:
        :param code:
        :return:
        """

        # Dictionary
        dictionary = self.__get_dictionary(frame=frame)

        message = self.__objects.write(
            nodes=dictionary, path=os.path.join(self.__path, f'{code}'))

        return message

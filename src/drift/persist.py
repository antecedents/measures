"""Module persist.py"""
import json
import os

import pandas as pd

import config
import src.functions.directories
import src.functions.objects


class Persist:
    """
    <b>Notes</b><br>
    -------<br>

    Structures and saves each institution's drift data.
    """

    def __init__(self):
        """
        Beware, .to_json() will automatically convert the values of a datetime64[] field
        to milliseconds epoch, therefore <milliseconds> ≡ <date>

        """

        self.__fields = ['milliseconds', 'js', 'wasserstein']

        # Instances
        self.__configurations = config.Config()
        self.__objects = src.functions.objects.Objects()

        # Storage
        self.__path = os.path.join(self.__configurations.warehouse, 'drift')
        src.functions.directories.Directories().create(self.__path)

    def __get_dictionary(self, frame: pd.DataFrame):
        """


        :param frame:
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
            nodes=dictionary, path=os.path.join(self.__path, f'{code}.json'))

        return message

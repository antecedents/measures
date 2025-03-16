"""Module persist.py"""
import json
import os

import pandas as pd

import config
import src.functions.directories
import src.functions.objects


class Persist:
    """
    Notes<br>
    ------<br>
    
    Saves an institution's attendance series decompositions in a stocks graphs format.
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()
        self.__objects = src.functions.objects.Objects()

        self.__path = os.path.join(self.__configurations.warehouse, 'decompositions')
        src.functions.directories.Directories().create(self.__path)

        # Fields in focus
        self.__fields = ['milliseconds', 'n_attendances', 'ln', 'trend', 'seasonal', 'residue']

    def __get_nodes(self, blob: pd.DataFrame) -> dict:
        """
        nodes = blob[self.__fields].to_dict(orient='split')

        :param blob:
        :return:
        """

        string: str = blob[self.__fields].to_json(orient='split')
        nodes: dict = json.loads(string)

        return nodes

    def exc(self, data: pd.DataFrame) -> str:
        """

        :param data: The decomposition data.

        :return:
        """

        # health_board_code: A board's unique identification code.
        # hospital_code: An institution's unique identification code.
        code = data[['health_board_code', 'hospital_code']].drop_duplicates().squeeze(axis=0)

        nodes: dict = self.__get_nodes(blob=data)
        nodes['health_board_code'] = code.health_board_code
        nodes['hospital_code'] = code.hospital_code

        message = self.__objects.write(
            nodes=nodes, path=os.path.join(self.__path, f'{code.hospital_code}.json'))

        return message

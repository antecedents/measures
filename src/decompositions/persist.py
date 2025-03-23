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

        self.__path = os.path.join(self.__configurations.points_, 'decompositions')
        src.functions.directories.Directories().create(self.__path)

        # Fields in focus
        self.__fields = ['milliseconds', 'n_attendances', 'trend', 'seasonal', 'residue']

    def __get_nodes(self, blob: pd.DataFrame) -> dict:
        """
        nodes = blob[self.__fields].to_dict(orient='split')

        :param blob:
        :return:
        """

        string: str = blob[self.__fields].to_json(orient='split')
        nodes: dict = json.loads(string)

        return nodes

    def exc(self, data: pd.DataFrame, specifications: pd.Series) -> str:
        """

        :param data: The decomposition data.
        :param specifications: health_board_code -> A board's unique identification code. | hospital_code -> An
                               institution's unique identification code.
        :return:
        """

        nodes: dict = self.__get_nodes(blob=data)
        nodes['health_board_code'] = specifications.health_board_code
        nodes['health_board_name'] = specifications.health_board_name
        nodes['hospital_code'] = specifications.hospital_code
        nodes['hospital_name'] = specifications.hospital_name

        message = self.__objects.write(
            nodes=nodes, path=os.path.join(self.__path, f'{specifications.hospital_code}.json'))

        return message

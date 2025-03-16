"""Module persist.py"""
import json
import os

import pandas as pd

import config
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

        # Fields in focus
        self.__fields = ['milliseconds', 'observation', 'trend', 'seasonal', 'residue', 'weight']

    def __get_nodes(self, blob: pd.DataFrame) -> dict:
        """
        nodes = blob[self.__fields].to_dict(orient='split')

        :param blob:
        :return:
        """


        string: str = blob[self.__fields].to_json(orient='split')
        nodes: dict = json.loads(string)

        return nodes

    def exc(self, data: pd.DataFrame, health_board_code: str, hospital_code: str) -> str:
        """

        :param data: The decomposition data.
        :param health_board_code: A board's unique identification code.
        :param hospital_code: An institution's unique identification code.
        :return:
        """

        nodes: dict = self.__get_nodes(blob=data)
        nodes['health_board_code'] = health_board_code
        nodes['hospital_code'] = hospital_code

        message = self.__objects.write(
            nodes=nodes, path=os.path.join(self.__configurations.decomposition_, f'{hospital_code}.json'))

        return message

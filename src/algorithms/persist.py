"""Module persist.py"""
import json
import os

import pandas as pd

import config
import src.elements.specifications as se
import src.functions.directories
import src.functions.objects


class Persist:
    """
    Notes<br>
    ------<br>

    Saves an institution's attendance series data in a stocks graphs format.
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()
        self.__objects = src.functions.objects.Objects()

        src.functions.directories.Directories().create(self.__configurations.points_)

        # Fields in focus
        self.__fields = ['milliseconds', 'n_attendances']

    def __get_nodes(self, blob: pd.DataFrame) -> dict:
        """
        nodes = blob[self.__fields].to_dict(orient='split')

        :param blob:
        :return:
        """

        string: str = blob[self.__fields].to_json(orient='split')
        nodes: dict = json.loads(string)

        return nodes

    def exc(self, data: pd.DataFrame, specifications: se.Specifications) -> str:
        """

        :param data: The data of an institution.
        :param specifications: health_board_code -> A board's unique identification code. | hospital_code -> An
                               institution's unique identification code. | etc.
        :return:
        """

        nodes: dict = self.__get_nodes(blob=data)
        nodes['attributes'] = specifications._asdict()

        message = self.__objects.write(
            nodes=nodes, path=os.path.join(self.__configurations.points_, f'{specifications.hospital_code}.json'))

        return message

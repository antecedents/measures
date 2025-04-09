"""Module persist.py"""
import json
import os

import pandas as pd

import config
import src.elements.parts as pr
import src.elements.specifications as se
import src.functions.objects


class Persist:
    """
    Saves
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()
        self.__objects = src.functions.objects.Objects()

        # Storage path
        self.__path = os.path.join(self.__configurations.points_, 'adjusting')

    @staticmethod
    def __dictionary(data: pd.DataFrame) -> dict:
        """

        :param data: The dataframe that would be converted into a dict
        :return:
        """

        string = data.to_json(orient='split')

        return json.loads(string)


    def exc(self, parts: pr.Parts, specifications: se.Specifications) -> str:
        """

        :param parts: An object of dataframes, refer to src.elements.parts
        :param specifications: A set of institution/hospital attributes.
        :return:
        """

        nodes = {
            'estimates': self.__dictionary(data=parts.estimates),
            'tests': self.__dictionary(data=parts.tests),
            'futures': self.__dictionary(data=parts.futures)}
        nodes.update(specifications._asdict())

        message: str = self.__objects.write(
            nodes=nodes, path=os.path.join(self.__path, f'{specifications.hospital_code}.json'))

        return message

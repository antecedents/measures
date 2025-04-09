"""Module persist.py"""
import json
import os

import pandas as pd

import config
import src.elements.parts as pr
import src.elements.specifications as se
import src.functions.objects


class Persist:

    def __init__(self):
        """

        """

        self.__configurations = config.Config()
        self.__objects = src.functions.objects.Objects()

        self.__path = os.path.join(self.__configurations.points_, 'adjusting')

    @staticmethod
    def __dictionary(data: pd.DataFrame):
        """

        :param data:
        :return:
        """

        string = data.to_json(orient='split')

        return json.loads(string)


    def exc(self, parts: pr.Parts, specifications: se.Specifications) -> str:
        """

        :param parts:
        :param specifications:
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

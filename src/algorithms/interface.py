"""Module interface.py"""
import pandas as pd

import src.algorithms.initial
import src.elements.specifications as se


class Interface:
    """
    The interface to the seasonal & trend component modelling steps.
    """

    def __init__(self, data: pd.DataFrame):
        """

        :param data: The weekly accidents & emergency data of institutions/hospitals
        """

        self.__data = data

    def exc(self, specifications_: list[se.Specifications]) -> list[str]:
        """
        Each instance of codes consists of the health board & institution/hospital codes of an institution/hospital.

        :param specifications_:
        :return:
        """

        # ...
        messages = src.algorithms.initial.Initial(
            data=self.__data, specifications_=specifications_).exc()

        return messages

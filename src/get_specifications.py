"""Module specifications.py"""
import pandas as pd

import src.elements.specifications as se


class Specifications:
    """
    <b>Notes</b><br>
    ------<br>

    For extracting details by institution
    """

    def __init__(self, reference: pd.DataFrame):
        """

        :param reference: The institutions/hospitals & health board reference.
        """

        self.__reference = reference

    def exc(self, code: str) -> se.Specifications:
        """

        :param code: An institution/hospital code
        :return:
        """

        values: pd.Series =  self.__reference.loc[
               self.__reference['hospital_code'] == code, :].squeeze(axis=0)
        dictionary = values.to_dict()


        return se.Specifications(**dictionary)

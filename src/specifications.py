"""Module specifications.py"""
import pandas as pd


class Specifications:
    """
    <b>Notes</b><br>
    ------<br>

    For extracting details by institution
    """

    def __init__(self, reference: pd.DataFrame):
        """

        :param reference:
        """

        self.__reference = reference

    def __call__(self, code: str) -> pd.Series:
        """

        :param code:
        :return:
        """

        return self.__reference.loc[
               self.__reference['hospital_code'] == code, :].squeeze(axis=0)

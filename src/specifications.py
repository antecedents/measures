
import pandas as pd


class Specifications:

    def __init__(self, reference: pd.DataFrame):

        self.__reference = reference

    def __call__(self, code: str):

        return self.__reference.loc[
               self.__reference['hospital_code'] == code, :].squeeze(axis=0)

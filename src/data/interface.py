"""Module interface.py"""
import datetime
import typing

import pandas as pd

import config
import src.data.menu
import src.data.reference
import src.data.specifications
import src.elements.s3_parameters as s3p
import src.elements.specifications as se
import src.elements.text_attributes as txa
import src.functions.streams


class Interface:
    """
    Notes<br>
    ------<br>

    Reads-in the data in focus.
    """

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        """

        self.__s3_parameters = s3_parameters

        # Configurations
        self.__configurations = config.Config()

        # An instance for writing/reading CSV (comma-separated values) files
        self.__streams = src.functions.streams.Streams()

    def __get_data(self) -> pd.DataFrame:
        """

        :return:
        """

        uri = ('s3://' + self.__s3_parameters.internal + '/' + self.__s3_parameters.path_internal_data +
               self.__configurations.source)
        text = txa.TextAttributes(uri=uri, header=0)
        data = self.__streams.read(text=text)

        return data[self.__configurations.fields]

    @staticmethod
    def __date_formatting(blob: pd.DataFrame) -> pd.DataFrame:
        """

        :param blob:
        :return:
        """

        blob['week_ending_date'] = pd.to_datetime(
            blob['week_ending_date'].astype(dtype=str), errors='coerce', format='%Y-%m-%d')

        return blob


    def exc(self) -> typing.Tuple[pd.DataFrame, list[se.Specifications]]:
        """

        :return:
        """

        # The data
        data = self.__get_data()
        data = self.__date_formatting(blob=data.copy())

        # ...
        doublet = data[['health_board_code', 'hospital_code']].drop_duplicates()

        # Menu
        reference = src.data.reference.Reference(
            s3_parameters=self.__s3_parameters).exc(identifiers=doublet['hospital_code'].to_list())
        src.data.menu.Menu().exc(reference=reference)

        # Structure for computations: ref. src.elements.specifications.py
        specifications_: list[se.Specifications] = src.data.specifications.Specifications().exc(
            reference=reference)

        return data, specifications_

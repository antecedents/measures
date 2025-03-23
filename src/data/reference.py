"""Module reference.py"""
import pandas as pd

import src.elements.s3_parameters as s3p
import src.elements.text_attributes as txa
import src.functions.streams


class Reference:
    """
    Reference
    """

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters: The overarching S3 (Simple Storage Service) parameters
                              settings of this project, e.g., region code name, buckets, etc.
        """

        self.__s3_parameters: s3p.S3Parameters = s3_parameters
        self.__endpoint = 's3://' + self.__s3_parameters.internal + '/' + 'references' + '/'

        # An instance for reading & writing CSV (comma-separated values) data
        self.__stream = src.functions.streams.Streams()

    def __boards(self):
        """

        :return:
        """

        uri = self.__endpoint + 'boards.csv'
        text = txa.TextAttributes(uri=uri, header=0, usecols=['health_board_code', 'health_board_name'])

        return self.__stream.read(text=text)

    def __institutions(self):
        """

        :return:
        """

        uri = self.__endpoint + 'institutions.csv'
        text = txa.TextAttributes(uri=uri, header=0, usecols=['health_board_code', 'hospital_code', 'hospital_name'])

        return self.__stream.read(text=text)

    def exc(self, codes: list[str]) -> pd.DataFrame:
        """

        :param codes:
        :return:
        """

        boards = self.__boards()
        institutions = self.__institutions()
        reference = institutions.merge(boards, on='health_board_code', how='left')

        return reference.loc[reference['hospital_code'].isin(codes), :]

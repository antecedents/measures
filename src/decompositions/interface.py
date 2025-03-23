"""Module interface.py"""
import glob
import logging
import os

import dask
import pandas as pd

import config
import src.decompositions.persist
import src.decompositions.structuring
import src.elements.text_attributes as txa
import src.functions.streams
import src.specifications


class Interface:
    """
    The interface to the programs that prepare the appropriate data structures for graphing the decompositions.
    """

    def __init__(self):
        """

        """

        self.__configurations = config.Config()
        self.__streams = src.functions.streams.Streams()

        self.__structuring = dask.delayed(src.decompositions.structuring.Structuring().exc)
        self.__persist = dask.delayed(src.decompositions.persist.Persist().exc)

    @dask.delayed
    def __get_data(self, uri: str) -> pd.DataFrame:
        """

        :param uri:
        :return:
        """

        text = txa.TextAttributes(uri=uri, header=0)

        frame = self.__streams.read(text=text)
        frame['week_ending_date'] = pd.to_datetime(
            frame['week_ending_date'].astype(dtype=str), errors='coerce', format='%Y-%m-%d')

        return frame

    def exc(self, reference: pd.DataFrame):
        """

        :param reference:
        :return:
        """

        path = os.path.join(self.__configurations.data_, 'data', '{code}', 'features.csv')

        # Identification Codes
        codes = reference['hospital_code'].unique()

        # Specifications
        specifications = dask.delayed(src.specifications.Specifications(reference=reference))

        # Compute
        computations = []
        for code in codes:
            specifications = specifications(code=code)
            data = self.__get_data(uri=path.format(code=code))
            data = self.__structuring(blob=data.copy())
            message = self.__persist(data=data, specifications=specifications)
            computations.append(message)
        messages = dask.compute(computations, scheduler='threads')[0]

        logging.info(messages)

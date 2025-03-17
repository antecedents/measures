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


class Interface:
    """
    The interface to the programs that prepare the appropriate data structures for graphing the decompositions.
    """

    def __init__(self):
        """
        Constructor
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

    def exc(self):
        """

        :return:
        """

        listings = glob.glob(
            pathname=os.path.join(self.__configurations.data_, 'data', '**', 'features.csv'))


        computations = []
        for listing in listings:
            data = self.__get_data(uri=listing)
            data = self.__structuring(blob=data.copy())
            message = self.__persist(data=data)
            computations.append(message)
        messages = dask.compute(computations, scheduler='threads')[0]

        logging.info(messages)

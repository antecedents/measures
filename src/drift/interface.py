"""Module interface.py"""
import glob
import logging
import os

import dask
import pandas as pd

import config
import src.drift.hankel
import src.drift.metrics
import src.drift.persist
import src.elements.specifications as se
import src.elements.text_attributes as txa
import src.functions.streams


class Interface:
    """
    <b>Notes</b><br>
    ------<br>
    The interface to drift score programs.<br>
    """

    def __init__(self, reference: pd.DataFrame, arguments: dict):
        """

        :param reference:
        :param arguments: A set of model development, and supplementary, arguments.
        """

        self.__reference = reference
        self.__arguments = arguments

        # Instances
        self.__configurations = config.Config()
        self.__streams = src.functions.streams.Streams()

        # Listings
        self.__listings = glob.glob(
            pathname=os.path.join(self.__configurations.data_, 'data', '**', 'data.csv'))

    @dask.delayed
    def __get_data(self, uri: str) -> pd.DataFrame:
        """

        :param uri: The uniform resource identifier of an institution's raw attendances data
        :return:
        """

        text = txa.TextAttributes(uri=uri, header=0)
        frame = self.__streams.read(text=text)

        frame['week_ending_date'] = pd.to_datetime(
            frame['week_ending_date'].astype(str), errors='coerce', format='%Y-%m-%d')

        return frame

    @dask.delayed
    def __get__specifications(self, code: str) -> se.Specifications:
        """

        :param code:
        :return:
        """

        values: pd.Series =  self.__reference.loc[self.__reference['hospital_code'] == code, :].squeeze(axis=0)
        dictionary = values.to_dict()

        return se.Specifications(**dictionary)

    def exc(self):
        """

        :return:
        """

        path = os.path.join(self.__configurations.data_, 'data', '{code}', 'data.csv')

        # Delayed Functions
        hankel = dask.delayed(src.drift.hankel.Hankel(arguments=self.__arguments).exc)
        metrics = dask.delayed(src.drift.metrics.Metrics(arguments=self.__arguments).exc)
        persist = dask.delayed(src.drift.persist.Persist().exc)

        # Compute
        codes = self.__reference['hospital_code'].unique()
        computations = []
        for code in codes:
            specifications = self.__get__specifications(code=code)
            data = self.__get_data(uri=path.format(code=code))
            matrix = hankel(data=data)
            frame = metrics(matrix=matrix, data=data)
            message = persist(frame=frame, specifications=specifications)
            computations.append(message)
        messages = dask.compute(computations, scheduler='threads')[0]
        logging.info('Drift -> \n%s', messages)

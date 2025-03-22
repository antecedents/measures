import logging
import glob
import os

import dask
import pandas as pd

import config
import src.drift.hankel
import src.drift.metrics
import src.elements.text_attributes as txa
import src.functions.streams


class Interface:
    """
    <b>Notes</b><br>
    ------<br>
    The interface to drift score programs.<br>
    """

    def __init__(self, arguments: dict):
        """

        :param arguments: A set of model development, and supplementary, arguments.
        """

        self.__arguments = arguments

        # Instances
        self.__configurations = config.Config()
        self.__streams = src.functions.streams.Streams()

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

    def exc(self):
        """

        :return:
        """

        listings = glob.glob(
            pathname=os.path.join(self.__configurations.data_, 'data', '**', 'data.csv'))
        codes = [os.path.basename(os.path.dirname(listing)) for listing in listings]
        logging.info(codes)

        hankel = dask.delayed(src.drift.hankel.Hankel(arguments=self.__arguments).exc)
        metrics = dask.delayed(src.drift.metrics.Metrics(arguments=self.__arguments).exc)

        computations = []
        for listing in listings:
            data = self.__get_data(uri=listing)
            matrix = hankel(data=data)
            shapes = metrics(matrix=matrix, data=data)
            computations.append(shapes)
        calculations = dask.compute(computations, scheduler='threads')[0]
        logging.info(calculations)

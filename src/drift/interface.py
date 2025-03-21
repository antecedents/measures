import datetime
import glob
import os

import pandas as pd

import config
import src.drift.wasserstein
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

        :param arguments:
        """

        self.__configurations = config.Config()
        self.__streams = src.functions.streams.Streams()

        self.__arguments = arguments
        self.__period = self.__arguments.get('seasons')
        self.__boundary = datetime.datetime.strptime(
            self.__arguments.get('boundary'), '%Y-%m-%d')

    def __get_data(self, uri: str) -> pd.DataFrame:
        """

        :param uri:
        :return:
        """

        text = txa.TextAttributes(uri=uri, header=0)
        frame = self.__streams.read(text=text)

        frame['week_ending_date'] = pd.to_datetime(
            frame['week_ending_date'].astype(str), errors='coerce', format='%Y-%m-%d')

        return frame.copy().loc[frame['week_ending_date'] >= self.__boundary, : ]

    def exc(self):
        """

        :return:
        """

        listings = glob.glob(pathname=os.path.join(self.__configurations.data_, 'data', '**', 'data.csv'))
        for listing in listings[:1]:

            data = self.__get_data(uri=listing)
            data.info()

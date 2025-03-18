"""Module trend.py"""
import os

import pandas as pd

import config
import src.elements.text_attributes as txa
import src.functions.streams


class Trend:
    """
    <b>Notes</b><br>
    ------<br>

    Reads-in the trend component forecasting estimations<br>
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

        self.__streams = src.functions.streams.Streams()



    def __get_data(self, uri: str) -> pd.DataFrame:
        """

        :param uri:
        :return:
        """

        text = txa.TextAttributes(uri=uri, header=0)

        frame = self.__streams.read(text=text)
        frame['date'] = pd.to_datetime(
            frame['date'].astype(str), errors='coerce', format='%Y-%m-%d')
        frame.rename(columns={'date': 'week_ending_date'}, inplace=True)
        frame.sort_values(by='week_ending_date', ascending=True, inplace=True)

        return frame

    def exc(self, code: str):
        """

        :param code:
        :return:
        """

        uri = os.path.join(self.__configurations.data_, 'models', code, 'tcf_forecasts.csv')

        return self.__get_data(uri=uri)

import os
import glob
import datetime

import pandas as pd

import config
import src.functions.streams
import src.elements.text_attributes as txa


class Interface:

    def __init__(self, arguments: dict):

        self.__configurations = config.Config()
        self.__streams = src.functions.streams.Streams()

        self.__boundary = datetime.datetime.strptime(
            arguments.get('boundary'), '%Y-%m-%d')

    def __get_data(self, uri: str) -> pd.DataFrame:

        text = txa.TextAttributes(uri=uri, header=0)
        frame = self.__streams.read(text=text)

        frame['week_ending_date'] = pd.to_datetime(
            frame['week_ending_date'].astype(str), errors='coerce', format='%Y-%m-%d')

        return frame.copy().loc[frame['week_ending_date'] >= self.__boundary, : ]


    def exc(self):

        listings = glob.glob(pathname=os.path.join(self.__configurations.data_, 'data', '**', 'data.csv'))

        for listing in listings:

            data = self.__get_data(uri=listing)
            data.info()

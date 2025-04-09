
import logging
import os

import numpy as np
import pandas as pd

import config
import src.elements.text_attributes as txa
import src.functions.streams


class Quantiles:

    def __init__(self):

        self.__configurations = config.Config()

    def exc(self, code: str) -> pd.Series:
        """

        :param code: The identification code of an institution/hospital.
        :return:
        """

        # Reading-in the ...
        uri = os.path.join(self.__configurations.data_, 'data', code, 'features.csv')

        text = txa.TextAttributes(uri=uri, header=0, usecols=['residue'])
        data = src.functions.streams.Streams().read(text=text)

        quantiles: pd.Series = data['residue'].quantile(q=np.array([0.1, 0.25, 0.5, 0.75, 0.9]))

        logging.info(quantiles)

        return quantiles


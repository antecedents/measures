"""Module metrics.py"""
import logging
import os
import json

import numpy as np
import pandas as pd

import config
import src.elements.specifications as se
import src.elements.parts as pr
import src.functions.objects


class Metrics:

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()
        self.__path = os.path.join(self.__configurations.points_, 'errors')

        self.__objects = src.functions.objects.Objects()

    @staticmethod
    def __root_mse(data: pd.DataFrame) -> pd.DataFrame:
        """
        This function calculates
            square root (mean ( a set of square errors ) )
        per set of square errors.

        :param data:
        :return:
        """

        se: np.ndarray = np.power(data[['l_e_error', 'u_e_error']].to_numpy(), 2)
        mse: np.ndarray = np.expand_dims(
            np.sum(se, axis=0)/se.shape[0], axis=0)

        frame = pd.DataFrame(data=np.sqrt(mse),
                             columns=['l_e_metrics', 'u_e_metrics'], index=['r_mse'])

        return frame

    @staticmethod
    def __pe(data: pd.DataFrame) -> pd.DataFrame:
        """

        :param data:
        :return:
        """

        er: np.ndarray = data[['l_e_error_rate', 'u_e_error_rate']].to_numpy()
        tiles: np.ndarray = np.percentile(a=er, q=[10, 25, 50, 75, 90], axis=0)
        frame = pd.DataFrame(data=100*tiles, columns=['l_e_metrics', 'u_e_metrics'],
                             index=['l_whisker', 'l_quarter', 'median', 'u_quarter', 'u_whisker'])

        return frame

    def __get_metrics(self, data: pd.DataFrame) -> dict:
        """

        :param data:
        :return:
        """

        frame = pd.concat((self.__root_mse(data=data), self.__pe(data=data)),
                          axis=0, ignore_index=False)
        string = frame.to_json(orient='split')

        return json.loads(string)

    def exc(self, parts: pr.Parts, specifications: se.Specifications):
        """

        :param parts:
        :param specifications:
        :return:
        """

        nodes = {
            'estimates': self.__get_metrics(data=parts.estimates),
            'tests': self.__get_metrics(data=parts.tests)}
        logging.info(nodes)

        message = self.__objects.write(nodes=nodes, path=os.path.join(self.__path, f'{specifications.hospital_code}.json'))
        logging.info('Forecasts Metrics -> %s', message)

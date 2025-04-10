"""Module metrics.py"""
import json
import os

import numpy as np
import pandas as pd

import config
import src.elements.parts as pr
import src.elements.specifications as se
import src.functions.objects


class Metrics:
    """
    Notes<br>
    ------

    <ul><li>l_e_: lower estimate</li>
        <li>u_e_: upper estimate</li>
        <li>r_mse: square root of the mean of the squared errors</li><ul>
    """

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

        square_error: np.ndarray = np.power(data[['l_tc_error', 'u_tc_error']].to_numpy(), 2)
        mse: np.ndarray = np.expand_dims(
            np.sum(square_error, axis=0)/square_error.shape[0], axis=0)

        frame = pd.DataFrame(data=np.sqrt(mse),
                             columns=['l_tc_e_metrics', 'u_tc_e_metrics'], index=['r_mse'])

        return frame

    @staticmethod
    def __pe(data: pd.DataFrame) -> pd.DataFrame:
        """
        ref. lower estimate error percentage, upper estimate error percentage

        :param data:
        :return:
        """

        er: np.ndarray = data[['l_tc_ep', 'u_tc_ep']].to_numpy()
        tiles: np.ndarray = np.percentile(a=er, q=[10, 25, 50, 75, 90], axis=0)
        frame = pd.DataFrame(data=tiles, columns=['l_tc_e_metrics', 'u_tc_e_metrics'],
                             index=['l_whisker_ep', 'l_quarter_ep', 'median_ep', 'u_quarter_ep', 'u_whisker_ep'])

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

    def exc(self, parts: pr.Parts, specifications: se.Specifications) -> str:
        """

        :param parts:
        :param specifications:
        :return:
        """

        nodes = {
            'estimates': self.__get_metrics(data=parts.estimates),
            'health_board_code': specifications.health_board_code,
            'health_board_name': specifications.health_board_name,
            'hospital_code': specifications.hospital_code,
            'hospital_name': specifications.hospital_name}

        message = self.__objects.write(
            nodes=nodes, path=os.path.join(self.__path, f'{specifications.hospital_code}.json'))

        return message

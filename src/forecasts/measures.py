"""Module measures.py"""
import json
import logging
import os

import pandas as pd

import config
import src.elements.parts as pr
import src.elements.specifications as se
import src.functions.objects


class Measures:
    """
    Measures
    """

    def __init__(self):
        """

        """

        self.__configurations = config.Config()
        self.__path = os.path.join(self.__configurations.points_, 'forecasts')

        # Instance for writing/reading JSON (JavaScript Object Notation) items.
        self.__objects = src.functions.objects.Objects()

        # Graphing fields; minimal is for futures parts, which do not include error measures because
        # their true values are yet unknown.
        self.__reference = ['milliseconds', 'n_attendances', 'l_estimate', 'u_estimate', 'l_e_error', 'u_e_error',
                            'l_e_error_rate', 'u_e_error_rate', 'trend', 'l_tc_estimate', 'u_tc_estimate', 'l_tc_ep', 'u_tc_ep']
        self.__minimal = ['milliseconds', 'n_attendances', 'l_estimate', 'u_estimate']

    @staticmethod
    def __get_node(blob: pd.DataFrame) -> dict:
        """

        :param blob:
        :return:
        """

        string: str = blob.to_json(orient='split')

        return json.loads(string)

    def __persist(self, nodes: dict, code: str):
        """

        :param nodes: An institution's data dictionary consisting of forecasts w.r.t. training,
                      testing, and futures parts; <b>alongside error measures</b>.<br>
        :param code: An institution's identification code.<br>
        :return:
        """

        message = self.__objects.write(nodes=nodes, path=os.path.join(self.__path, f'{code}.json'))

        logging.info('Forecasts Values & Measures -> %s', message)

    def exc(self, parts: pr.Parts, specifications: se.Specifications) -> pr.Parts:
        """

        :param parts: An institution's data object consisting of forecasts w.r.t. training,
                      testing, and futures parts.<br>
        :param specifications: An institution's identifiers.<br>
        :return:
        """

        nodes = {
            'estimates': self.__get_node(parts.estimates[self.__reference]),
            'tests': self.__get_node(parts.tests[self.__reference]),
            'futures': self.__get_node(parts.futures[self.__minimal]),
            'health_board_code': specifications.health_board_code,
            'health_board_name': specifications.health_board_name,
            'hospital_code': specifications.hospital_code,
            'hospital_name': specifications.hospital_name}
        self.__persist(nodes=nodes, code=specifications.hospital_code)

        return parts

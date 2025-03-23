"""Module menu.py"""
import logging
import os

import pandas as pd

import config
import src.functions.objects


class Menu:
    """
    Menu
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

    def exc(self, reference: pd.DataFrame):
        """

        :param reference: The institutions/hospitals & health board reference.
        :return:
        """

        frame = pd.DataFrame(data={'desc': reference['hospital_code'].to_numpy(),
                                   'name': reference['hospital_name'].to_numpy()})

        nodes = frame.to_dict(orient='records')
        logging.info(nodes)

        message = src.functions.objects.Objects().write(
            nodes=nodes, path=os.path.join(self.__configurations.menu_, 'menu.json'))
        logging.info(message)

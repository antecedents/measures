"""Module menu.py"""
import glob
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

    def exc(self):
        """

        :return:
        """

        listings = glob.glob(os.path.join(self.__configurations.data_, 'data', '**'))
        codes = [os.path.basename(listing) for listing in listings]

        frame = pd.DataFrame(data={'desc': codes, 'name': codes})
        nodes = frame.to_dict(orient='records')

        src.functions.objects.Objects().write(
            nodes=nodes, path=os.path.join(self.__configurations.menu_, 'menu.json'))

"""Module setup.py"""
import sys

import config
import src.functions.cache
import src.functions.directories
import src.s3.bucket
import src.s3.keys
import src.s3.prefix


class Setup:
    """
    Description
    -----------

    Sets up local & cloud environments
    """

    def __init__(self):
        """
        Constructor
        """

        # Configurations, etc.
        self.__configurations = config.Config()

        # Instances
        self.__directories = src.functions.directories.Directories()

    def __data(self) -> bool:
        """

        :return:
        """

        self.__directories.cleanup(path=self.__configurations.data_)

        return self.__directories.create(path=self.__configurations.data_)

    def __local(self) -> bool:
        """

        :return:
        """

        self.__directories.cleanup(path=self.__configurations.warehouse)

        states = []
        for path in [self.__configurations.points_, self.__configurations.menu_]:
            states.append(self.__directories.create(path=path))

        return all(states)

    def exc(self) -> bool:
        """

        :return:
        """

        if self.__local() & self.__data():
            return True

        src.functions.cache.Cache().exc()
        sys.exit('Set up failure (setup.py)')

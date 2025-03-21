
import numpy as np
import pandas as pd
import scipy.linalg as li

class Hankel:

    def __init__(self, arguments: dict):
        """

        :param arguments: A set of model development, and supplementary, arguments.
        """

        self.__arguments = arguments

    def exc(self, data: pd.DataFrame) -> np.ndarray:
        """

        :param data: An institution's data
        :return:
        """

        frame = data.copy()

        points = frame['n_attendances'].to_numpy()
        reverse = points[::-1]

        matrix: np.ndarray = li.hankel(
            reverse[:self.__arguments.get('seasons')],
            reverse[(self.__arguments.get('seasons') - 1):]).T

        return matrix


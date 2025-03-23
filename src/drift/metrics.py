import typing

import numpy as np
import pandas as pd
import scipy.spatial as spa
import scipy.stats as sta


class Metrics:

    def __init__(self, arguments: dict):
        """

        :param arguments:
        """

        self.__arguments = arguments

    @staticmethod
    def __get_js(penultimate: np.ndarray, ultimate: np.ndarray) -> np.ndarray | float:
        """

        :param penultimate:
        :param ultimate:
        :return:
        """

        # noinspection PyArgumentList
        return spa.distance.jensenshannon(p=penultimate, q=ultimate, axis=1)

    @staticmethod
    def __get_wasserstein(penultimate: np.ndarray, ultimate: np.ndarray) -> float:
        """

        :param penultimate:
        :param ultimate:
        :return:
        """

        # noinspection PyTypeChecker
        return sta.wasserstein_distance(penultimate, ultimate).__float__()

    @staticmethod
    def __get_matrices(matrix: np.ndarray) -> typing.Tuple[np.ndarray, np.ndarray]:
        """

        :param matrix:
        :return:
        """

        penultimate = matrix[1:, :]
        ultimate = matrix[:-1, :]

        return np.fliplr(penultimate), np.fliplr(ultimate)

    @staticmethod
    def __milliseconds(blob: pd.DataFrame) -> pd.DataFrame:
        """

        :param blob:
        :return:
        """

        frame = blob.copy()
        frame['milliseconds']  = (frame['date'].to_numpy().astype(np.int64) / (10 ** 6)).astype(np.longlong)
        frame.sort_values(by='date', inplace=True)

        return frame

    def exc(self, matrix: np.ndarray, data: pd.DataFrame) -> pd.DataFrame:
        """

        :param matrix:
        :param data:
        :return:
        """

        # Matrices
        penultimate, ultimate = self.__get_matrices(matrix=matrix)

        # Scores
        js = self.__get_js(penultimate=penultimate, ultimate=ultimate)
        wasserstein = [self.__get_wasserstein(penultimate[i,:], ultimate[i,:]) for i in np.arange(ultimate.shape[0])]
        dates = pd.date_range(
            start=data['week_ending_date'].max(), periods=js.shape[0], freq='-1' + self.__arguments.get('frequency'))
        frame = pd.DataFrame(data={'js': js, 'wasserstein': wasserstein, 'date': dates})

        # Temporary
        code = data[['health_board_code', 'hospital_code']].drop_duplicates().squeeze()
        frame['health_board_code'] = code.health_board_code
        frame['hospital_code'] = code.hospital_code

        return self.__milliseconds(blob=frame)

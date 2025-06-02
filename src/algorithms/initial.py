"""Module initial.py"""
import dask
import numpy as np
import pandas as pd

import src.algorithms.persist
import src.elements.specifications as se
import src.functions.directories


class Initial:
    """
    Build's each institution's series
    """

    def __init__(self, data: pd.DataFrame, specifications_: list[se.Specifications]):
        """

        :param data: The weekly accidents & emergency data of institutions/hospitals
        :param specifications_: The unique set of health board & institution pairings.
        """

        self.__data = data
        self.__specifications_ = specifications_

    @dask.delayed
    def __get_data(self, specifications: se.Specifications) -> pd.DataFrame:
        """

        :param specifications: The board & institution codes, etc.
        :return:
        """

        frame = self.__data.copy().loc[self.__data['hospital_code'] == specifications.hospital_code, :]

        return frame

    @dask.delayed
    def __epoch(self, data: pd.DataFrame) -> pd.DataFrame:
        """

        :param data:
        :return:
        """

        instances = data.copy()
        instances['milliseconds']  = (
                instances['week_ending_date'].to_numpy().astype(np.int64) / (10 ** 6)
        ).astype(np.longlong)
        instances.sort_values(by='week_ending_date', inplace=True)

        return instances

    def exc(self) -> list[str]:
        """

        :return:
        """

        # Additional delayed tasks

        __persist = dask.delayed(src.algorithms.persist.Persist().exc)

        computations = []
        for specifications in self.__specifications_:
            data: pd.DataFrame = self.__get_data(specifications=specifications)
            data: pd.DataFrame = self.__epoch(data=data)
            message = __persist(data=data, specifications=specifications)
            computations.append(message)
        messages = dask.compute(computations, scheduler='threads')[0]

        return messages

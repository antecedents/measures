"""Module structuring.py"""

import numpy as np
import pandas as pd


class Structuring:
    """
    Structures the data in-line with graphing library expectations.
    """

    @staticmethod
    def __epoch(blob: pd.DataFrame) -> pd.DataFrame:
        """

        :param blob:
        :return:
        """

        decompositions = blob.copy()
        decompositions['milliseconds']  = (
                decompositions['week_ending_date'].to_numpy().astype(np.int64) / (10 ** 6)
        ).astype(np.longlong)
        decompositions.sort_values(by='week_ending_date', inplace=True)

        return decompositions

    def exc(self, blob: pd.DataFrame) -> pd.DataFrame:
        """

        :param blob: Decomposition components.
        :return:
        """

        data = blob.copy()

        return self.__epoch(blob=data)

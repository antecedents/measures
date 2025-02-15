
import pandas as pd
import numpy as np
import statsmodels.tsa.seasonal as stl

class Structuring:

    def __init__(self):
        pass

    @staticmethod
    def __epoch(blob: pd.DataFrame):
        """

        :param blob:
        :return:
        """

        decompositions = blob.copy()
        decompositions['milliseconds']  = (
                decompositions['week_ending_date'].to_numpy().astype(np.int64) / (10 ** 6)
        ).astype(np.longlong)

        return decompositions

    @staticmethod
    def __get_variables(parts: stl.DecomposeResult):

        decompositions = pd.DataFrame(
            data={'observation': parts.observed.values, 'trend': parts.trend.values, 'seasonal': parts.seasonal.values,
                  'residue': parts.resid.values, 'weight': parts.weights.values}, index=parts.observed.index)
        decompositions.reset_index(inplace=True)
        decompositions.sort_values(by='week_ending_date', inplace=True)

        return decompositions

    def exc(self, parts: stl.DecomposeResult):

        data = self.__get_variables(parts=parts)
        data = self.__epoch(blob=data)

        return data

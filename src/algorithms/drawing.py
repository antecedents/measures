import pandas as pd
import numpy as np
import statsmodels.tsa.seasonal as stl


class Drawing:

    def __init__(self):
        pass

    @staticmethod
    def __epoch(blob: pd.DataFrame):
        """
        
        :param blob:
        :return:
        """

        decompositions = blob.copy()

        decompositions['epoch']  = (
                decompositions['week_ending_date'].to_numpy().astype(np.int64) / (10 ** 6)
        ).astype(np.longlong)

    @staticmethod
    def __frame(struct: stl.DecomposeResult):

        decompositions = pd.DataFrame(
            data={'observation': struct.observed.values, 'trend': struct.trend.values, 'seasonal': struct.seasonal.values,
                  'residue': struct.resid.values, 'weight': struct.weights.values}, index=struct.observed.index)
        decompositions.reset_index(inplace=True)
        decompositions.sort_values(by='week_ending_date', inplace=True)

        return decompositions

    def exc(self, struct: stl.DecomposeResult):

        self.__frame(struct=struct)



import pandas as pd
import statsmodels.tsa.seasonal as stl


class Graphing:

    def __init__(self):
        pass

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



import logging
import numpy as np
import pandas as pd

import src.elements.parts as pr


class Measures:

    def __init__(self):
        pass

    @staticmethod
    def __errors(data: pd.DataFrame) -> pd.DataFrame:
        """

        :param data:
        :return:
        """

        ground = data['n_attendances'].to_numpy()[:,None]
        forecasts = data[['l_estimate', 'u_estimate']].to_numpy()
        errors: np.ndarray =  ground - forecasts
        errors.sort(axis=1)

        data.loc[:, ['l_error', 'u_error']] = errors
        data.loc[:, ['l_error_rate', 'u_error_rate']] = np.true_divide(errors, ground)

        return data

    def exc(self, parts: pr.Parts) -> pr.Parts:

        parts = parts._replace(estimates=self.__errors(data=parts.estimates.copy()),
                       tests=self.__errors(data=parts.tests.copy()))

        logging.info(parts)

        return parts

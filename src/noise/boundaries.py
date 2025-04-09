"""Module boundaries.py"""
import numpy as np
import pandas as pd
import scipy.stats as sta

import src.elements.parts as pr


class Boundaries:
    """
    <b>Notes</b><br>
    ------<br>
    This class determines estimations boundaries vis-à-vis estimations samples.<br>
    """

    def __init__(self):
        """
        Constructor
        """

        self.__span = 0.90

    @staticmethod
    def __get_metric(data: pd.DataFrame, percentile: float, disturbance: float) -> float:
        """
        period + average + (z-score * standard deviation)

        period:  An institution's seasonal component estimates.
        average: The averages of the samples of an institution's trend component estimates.
        deviation: The standard deviations of the trend component estimates samples.

        :param data: The data
        :param percentile: The percentile boundary of interest.
        :param disturbance:
        :return:
        """

        score = sta.norm.ppf(percentile)

        period = data['sc_estimate']
        average = data['tc_estimate']
        deviation = data['tc_estimate_deviation']

        return period + average + (score * deviation) + disturbance

    @staticmethod
    def __get_error_values(frame: pd.DataFrame) -> pd.DataFrame:
        """

        :param frame: The forecasts w.r.t. training or testing phases.
        :return:
        """

        # ground truth, forecasts
        forecasts = frame[['l_estimate', 'u_estimate']].to_numpy()
        ground = frame['n_attendances'].to_numpy()[:,None]

        # raw errors and error rates; negative/lower, positive/higher
        errors: np.ndarray =  forecasts - ground
        frame.loc[:, ['l_e_error', 'u_e_error']] = errors
        frame.loc[:, ['l_e_ep', 'u_e_ep']] = 100 * np.true_divide(errors, ground)

        return frame

    def __get_boundaries(self, data: pd.DataFrame, metrics: pd.Series) -> pd.DataFrame:
        """

        :param data:
        :return:
        """

        data['l_estimate'] = self.__get_metric(data=data, percentile=0.5 - 0.5*self.__span, disturbance=metrics['l_m_decile'])
        data['u_estimate'] = self.__get_metric(data=data, percentile=0.5 + 0.5*self.__span, disturbance=metrics['u_m_decile'])

        return data

    def exc(self, parts: pr.Parts, quantiles: pd.DataFrame) -> pr.Parts:
        """

        :param parts:
        :param quantiles:
        :return:
        """

        metrics = quantiles['residue']

        estimates = self.__get_boundaries(data=parts.estimates.copy(), metrics=metrics)
        tests = self.__get_boundaries(data=parts.tests.copy(), metrics=metrics)
        futures = self.__get_boundaries(data=parts.futures.copy(), metrics=metrics)

        estimates = self.__get_error_values(frame=estimates.copy())
        tests = self.__get_error_values(frame=tests.copy())

        parts = parts._replace(estimates=estimates, tests=tests, futures=futures)

        return parts

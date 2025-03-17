"""Module seasonal.py"""
import typing

import pandas as pd


class Trend(typing.NamedTuple):
    """
    The data type class ⇾ Trend

    Attributes
    ----------
    estimates :
        The data frame of estimates vis-à-vis training data
    tests:
        The frame of estimates vis-à-vis testing data
    futures:
        The frame of estimates vis-à-vis the future
    """

    estimates: pd.DataFrame
    tests: pd.DataFrame
    futures: pd.DataFrame

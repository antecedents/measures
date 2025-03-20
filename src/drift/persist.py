"""Module persist.py"""
import numpy as np
import pandas as pd


class Persist:

    def __init__(self):
        pass

    @staticmethod
    def __milliseconds(blob: pd.DataFrame) -> pd.DataFrame:

        frame = blob.copy()
        frame['milliseconds']  = (
                frame['week_ending_date'].to_numpy().astype(np.int64) / (10 ** 6)
        ).astype(np.longlong)
        frame.sort_values(by='week_ending_date', inplace=True)

        return frame

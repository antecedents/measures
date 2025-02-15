import pandas as pd
import numpy as np


class Drawing:

    def __init__(self):

        self.__fields = ['milliseconds', 'observation', 'trend', 'seasonal', 'residue', 'weight']

    def __get_instances(self, blob: pd.DataFrame) -> dict:

        instances = blob[self.__fields].to_dict(orient='split')

        return instances

    def exc(self, data: pd.DataFrame, health_board_code: str, hospital_code):

        instances: dict = self.__get_instances(blob=data)
        instances['health_board_code'] = health_board_code
        instances['hospital_code'] = hospital_code

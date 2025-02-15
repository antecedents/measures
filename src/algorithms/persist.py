import pandas as pd

import src.functions.objects


class Persist:

    def __init__(self):
        """
        Constructor
        """

        self.__fields = ['milliseconds', 'observation', 'trend', 'seasonal', 'residue', 'weight']

    def __get_instances(self, blob: pd.DataFrame) -> dict:
        """

        :param blob:
        :return:
        """

        nodes = blob[self.__fields].to_dict(orient='split')

        return nodes

    def exc(self, data: pd.DataFrame, health_board_code: str, hospital_code):
        """

        :param data:
        :param health_board_code:
        :param hospital_code:
        :return:
        """

        nodes: dict = self.__get_instances(blob=data)
        nodes['health_board_code'] = health_board_code
        nodes['hospital_code'] = hospital_code

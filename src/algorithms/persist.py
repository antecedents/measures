import logging
import os
import pandas as pd

import config
import src.functions.objects


class Persist:
    """
    Notes<br>
    ------<br>
    
    Saves an institution's attendance series decompositions in a stocks graphs format.
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()
        self.__objects = src.functions.objects.Objects()

        # Fields in focus
        self.__fields = ['milliseconds', 'observation', 'trend', 'seasonal', 'residue', 'weight']

        # Logging: If necessary, set force = True
        logging.basicConfig(level=logging.INFO, format='%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __get_nodes(self, blob: pd.DataFrame) -> dict:
        """

        :param blob:
        :return:
        """

        nodes = blob[self.__fields].to_dict(orient='split')

        return nodes

    def exc(self, data: pd.DataFrame, health_board_code: str, hospital_code: str):
        """

        :param data: The decomposition data.
        :param health_board_code: A board's unique identification code.
        :param hospital_code: An institution's unique identification code.
        :return:
        """

        nodes: dict = self.__get_nodes(blob=data)
        nodes['health_board_code'] = health_board_code
        nodes['hospital_code'] = hospital_code

        message = self.__objects.write(
            nodes=nodes, path=os.path.join(self.__configurations.decompositions_, f'{hospital_code}.json'))
        self.__logger.info(message)

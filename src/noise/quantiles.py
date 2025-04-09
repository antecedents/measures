"""Module quantiles.py"""
import json
import logging
import os

import numpy as np
import pandas as pd

import config
import src.elements.parts as pr
import src.elements.specifications as se
import src.functions.objects


class Quantiles:

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()
        self.__path = os.path.join(self.__configurations.points_, 'quantiles')

        # Instances
        self.__objects = src.functions.objects.Objects()

        self.__terms = {0.1: 'l_whisker', 0.25: 'l_quartile', 0.4: 'l_m_decile', 0.5: 'median',
                        0.6: 'u_m_decile', 0.75: 'u_quartile', 0.9: 'u_whisker'}

    def __get_quantiles(self, blob: pd.DataFrame) -> pd.DataFrame:
        """

        :param blob: A dataframe that includes the residues after series decomposition
        :return:
        """

        values: pd.Series = blob['residue'].quantile(q=np.array([0.1, 0.25, 0.4, 0.5, 0.6, 0.75, 0.9]))
        board = values.to_frame()
        board['term'] = board.index.map(self.__terms)

        # Implicitly drop the index of quantile points
        board.set_index(keys='term', inplace=True)

        return board

    def __persist(self, quantiles: pd.DataFrame, specifications: se.Specifications):
        """

        :param quantiles: The residues quantiles.
        :param specifications: A set of institution/hospital attributes.
        :return:
        """

        nodes = json.loads(quantiles['residue'].to_json(orient='split'))
        nodes['categories'] = 'residue'
        nodes.update(specifications._asdict())

        message = self.__objects.write(
            nodes=nodes, path=os.path.join(self.__path, f'{specifications.hospital_code}.json'))

        logging.info('Quantiles -> %s', message)

    def exc(self, parts: pr.Parts, specifications: se.Specifications) -> pd.DataFrame:
        """

        :param parts: An object of dataframes, refer to src.elements.parts
        :param specifications: A set of institution/hospital attributes.
        :return:
        """

        data = parts.estimates

        # The index values are the self.__terms values, and the frame has a single field -> residue
        quantiles = self.__get_quantiles(blob=data)
        logging.info(quantiles)

        # Persist
        self.__persist(quantiles=quantiles, specifications=specifications)

        return quantiles

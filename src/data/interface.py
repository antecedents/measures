"""Module interface.py"""
import logging

import pandas as pd

import config
import src.elements.s3_parameters as s3p
import src.elements.text_attributes as txa
import src.functions.streams


class Interface:
    """
    Notes<br>
    ------<br>

    Reads-in the data in focus.
    """

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        """

        self.__s3_parameters = s3_parameters

        # Instances
        self.__streams = src.functions.streams.Streams()
        self.__configurations = config.Config()

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n\n',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __get_data(self, uri: str) -> pd.DataFrame:
        """

        :param uri: A data sets' uniform resource identifier.
        :return:
        """

        text = txa.TextAttributes(uri=uri, header=0)

        frame = self.__streams.read(text=text)
        frame['week_ending_date'] = pd.to_datetime(
            frame['week_ending_date'].astype(dtype=str), errors='coerce', format='%Y-%m-%d')

        return frame[self.__configurations.fields]

    def __viable(self, blob: pd.DataFrame) -> pd.DataFrame:
        """

        :param blob:
        :return:
        """

        # Counts per institution
        counts: pd.DataFrame = blob.copy()[['health_board_code', 'hospital_code']].groupby(
            by='health_board_code').value_counts().to_frame()
        counts.reset_index(inplace=True)

        # Institutions that have a viable number of observations.
        viable: pd.DataFrame = counts.loc[counts['count'] >= (
                self.__configurations.seasons * self.__configurations.cycles), :]

        return viable

    def exc(self, stamp: str) -> pd.DataFrame:
        """

        :param stamp: A date stamp.
        :return:
            training: The training data set.<br>
            testing: The testing data set.
        """

        # The data sets' uniform resource identifier
        uri = ('s3://' + self.__s3_parameters.internal + '/' +
                self.__s3_parameters.path_internal_data + f'raw/{stamp}.csv')

        # Reading
        data = self.__get_data(uri=uri)
        data.info()

        # Institutions that have a viable number of observations.
        viable = self.__viable(blob=data)
        data = data.copy().loc[data['hospital_code'].isin(viable['hospital_code'].unique()), :]
        data.info()

        # Index
        data.set_index(keys='week_ending_date', drop=True, inplace=True)
        self.__logger.info(data.head())

        return data

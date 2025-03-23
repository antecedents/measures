
import logging

import config
import src.elements.s3_parameters as s3p
import src.s3.directives
import src.s3.unload


class Assets:
    """
    Notes<br>
    ------<br>

    An interface to the data/artefacts retrieval class.  <b>Beware, sometimes dask
    will be unnecessary, edit accordingly.</b>
    """

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters: The overarching S3 (Simple Storage Service) parameters
                              settings of this project, e.g., region code name, buckets, etc.
        """

        self.__s3_parameters: s3p.S3Parameters = s3_parameters

        # Setting up
        self.__configurations = config.Config()
        self.__source_bucket = self.__s3_parameters.internal
        self.__prefix = self.__s3_parameters.path_internal_artefacts + self.__configurations.stamp

        # Directives
        self.__directives = src.s3.directives.Directives()

    def __get_assets(self) -> int:
        """

        :return:
        """

        try:
            return self.__directives.synchronise(
                source_bucket=self.__source_bucket, origin=self.__prefix, target=self.__configurations.data_)
        except RuntimeError as err:
            raise err from err

    def exc(self):

        state = self.__get_assets()
        logging.info('Assets State: %s', state)

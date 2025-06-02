"""Module interface.py"""
import logging
import os

import boto3
import pandas as pd

import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.s3.ingress
import src.transfer.dictionary
import src.transfer.metadata


class Interface:
    """
    Notes<br>
    ------<br>

    This class executes the data transfer step; transfer to Amazon S3 (Simple Storage Service).
    """

    def __init__(self, connector: boto3.session.Session, service: sr.Service,  s3_parameters: s3p):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 parameters settings of this
                              project, e.g., region code name, buckets, etc.
        """

        self.__service: sr.Service = service
        self.__s3_parameters: s3p.S3Parameters = s3_parameters

        # Metadata
        metadata = src.transfer.metadata.Metadata(connector=connector)
        self.__metadata_p = metadata.exc(name='points.json')
        self.__metadata_m = metadata.exc(name='menu.json')

        # Instances
        self.__dictionary = src.transfer.dictionary.Dictionary()

    def __get_metadata(self, frame: pd.DataFrame) -> pd.DataFrame:
        """

        :param frame:
        :return:
        """

        sections = ['decompositions', 'drift', 'errors', 'forecasts', 'adjusting', 'quantiles']

        frame = frame.assign(
            metadata = frame['section'].apply(
                lambda x: self.__metadata_p if x in sections else self.__metadata_m))

        return frame

    def exc(self):
        """

        :return:
        """

        # The strings for transferring data to Amazon S3 (Simple Storage Service)
        strings = self.__dictionary.exc(
            path=os.path.join(os.getcwd(), 'warehouse'), extension='json', prefix='warehouse/')

        # Adding metadata details per instance
        strings = self.__get_metadata(frame=strings.copy())
        logging.info(strings)



        # Transfer
        messages = src.s3.ingress.Ingress(
            service=self.__service, bucket_name=self.__s3_parameters.external).exc(
            strings=strings, tagging='project=emergency')
        logging.info(messages)

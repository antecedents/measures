"""Module interface.py"""
import logging
import sys
import typing

import boto3

import config
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.functions.cache
import src.functions.service
import src.preface.setup
import src.s3.configurations
import src.s3.keys
import src.s3.s3_parameters


class Interface:
    """
    Interface
    """

    def __init__(self):
        pass

    @staticmethod
    def __get_arguments(connector: boto3.session.Session) -> dict:
        """

        :return:
        """

        key_name = 'artefacts' + '/' + 'architecture' + '/' + 'arguments.json'

        return src.s3.configurations.Configurations(connector=connector).objects(key_name=key_name)

    @staticmethod
    def __proceed(service: sr.Service, bucket_name: str):
        """

        :param service:
        :param bucket_name:
        :return:
        """

        prefix = f'artefacts{config.Config().stamp}'

        value = src.s3.keys.Keys(service=service, bucket_name=bucket_name).excerpt(prefix=prefix)
        logging.info('KEYS: %s', value)

        return value

    def exc(self) -> typing.Tuple[boto3.session.Session, s3p.S3Parameters, sr.Service, dict]:
        """

        :return:
        """

        connector = boto3.session.Session()
        s3_parameters: s3p.S3Parameters = src.s3.s3_parameters.S3Parameters(connector=connector).exc()
        service: sr.Service = src.functions.service.Service(
            connector=connector, region_name=s3_parameters.region_name).exc()

        if not self.__proceed(service=service, bucket_name=s3_parameters.internal):
            src.functions.cache.Cache().exc()
            sys.exit('EMPTY')

        arguments: dict = self.__get_arguments(connector=connector)
        src.preface.setup.Setup().exc()

        return connector, s3_parameters, service, arguments

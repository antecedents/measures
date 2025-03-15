"""Module interface.py"""
import logging
import typing

import boto3

import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.functions.service
import src.preface.setup
import src.s3.s3_parameters


class Interface:
    """
    Interface
    """

    def __init__(self):
        pass


    @staticmethod
    def __setting_up(service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param service:
        :param s3_parameters:
        :return:
        """

        src.preface.setup.Setup(service=service, s3_parameters=s3_parameters).exc()

    def exc(self) -> typing.Tuple[boto3.session.Session, s3p.S3Parameters, sr.Service]:
        """

        :return:
        """

        connector = boto3.session.Session()
        s3_parameters: s3p.S3Parameters = src.s3.s3_parameters.S3Parameters(connector=connector).exc()
        service: sr.Service = src.functions.service.Service(
            connector=connector, region_name=s3_parameters.region_name).exc()


        self.__setting_up(service=service, s3_parameters=s3_parameters)

        return connector, s3_parameters, service

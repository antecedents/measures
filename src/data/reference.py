import logging
import src.elements.s3_parameters as s3p
import src.functions.streams
import src.elements.text_attributes as txa


class References:

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters: The overarching S3 (Simple Storage Service) parameters
                              settings of this project, e.g., region code name, buckets, etc.
        """

        self.__s3_parameters: s3p.S3Parameters = s3_parameters

        self.__stream = src.functions.streams.Streams()

    def __boards(self):

        uri = 's3://' + self.__s3_parameters.internal + '/' + 'references' + '/' + 'boards.csv'
        text = txa.TextAttributes(uri=uri, header=0, usecols=['health_board_code', 'health_board_name'])

        return self.__stream.read(text=text)

    def __institutions(self):

        uri = 's3://' + self.__s3_parameters.internal + '/' + 'references' + '/' + 'institutions.csv'
        text = txa.TextAttributes(uri=uri, header=0, usecols=['health_board_code', 'hospital_code', 'hospital_name'])

        return self.__stream.read(text=text)

    def exc(self):

        logging.info(self.__boards())
        logging.info(self.__institutions())

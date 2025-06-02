"""
Module config.py
"""
import logging
import datetime
import os


class Config:
    """
    Description
    -----------

    A class for configurations
    """

    def __init__(self) -> None:
        """
        <b>Notes</b><br>
        ------<br>

        Variables denoting a path - including or excluding a filename - have an underscore suffix; this suffix is
        excluded for names such as warehouse, storage, depository, *key, etc.<br><br>

        """

        '''
        Date Stamp: The most recent Tuesday.  The code of Tuesday is 1, hence 
        now.weekday() - 1
        '''
        now = datetime.datetime.now()
        offset = (now.weekday() - 1) % 7
        tuesday = now - datetime.timedelta(days=offset)
        self.stamp: str = tuesday.strftime('%Y-%m-%d')
        logging.info(self.stamp)


        '''
        The prefix.ending.string & key.name of the modelling data; ref.
            s3:// {bucket} / {prefix.starting.string} / {prefix.ending.string} / {key.name}
        '''
        self.source = f'modelling/{self.stamp}.csv'


        '''
        Keys
        '''
        self.s3_parameters_key = 's3_parameters.yaml'
        self.arguments_key = 'measures/arguments.json'
        self.metadata_ = 'measures/external'


        '''
        The prefix of the Amazon repository where the measures will be stored
        '''
        self.prefix = 'warehouse/measures'


        '''
        Local Paths
        '''
        self.warehouse: str = os.path.join(os.getcwd(), 'warehouse')
        self.measures_ = os.path.join(self.warehouse, 'measures')
        self.points_ = os.path.join(self.measures_, 'points')
        self.menu_ = os.path.join(self.measures_, 'menu')


        '''
        Extra
        '''
        self.fields = ['week_ending_date', 'health_board_code', 'hospital_code', 'n_attendances']

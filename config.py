"""
Module config.py
"""
import logging
import os
import datetime


class Config:
    """
    Description
    -----------

    A class for configurations
    """

    def __init__(self) -> None:
        """
        Notes<br>
        -------<br>


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


        # ...
        self.data_ = os.path.join(os.getcwd(), 'data')
        self.warehouse = os.path.join(os.getcwd(), 'warehouse')
        self.decomposition_ = os.path.join(self.warehouse, 'series', 'decomposition')

        # Seed
        self.seed = 5

        # Configuration files
        self.s3_parameters_key = 's3_parameters.yaml'
        self.metadata_ = 'metadata'

        '''
        For architecture JSON
        '''

        # Fields
        self.fields = ['week_ending_date', 'health_board_code', 'hospital_code',  'n_attendances']

        # Seasons, trends, etc.
        self.seasons = 52
        self.trends = 1
        self.cycles = 3

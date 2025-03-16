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

        # Directories
        self.data_ = os.path.join(os.getcwd(), 'data')
        self.warehouse = os.path.join(os.getcwd(), 'warehouse')

        # Configuration files
        self.s3_parameters_key = 's3_parameters.yaml'
        self.metadata_ = 'metadata'

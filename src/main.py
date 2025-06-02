"""Module main.py"""
import datetime
import logging
import os
import sys


def main():
    """
    https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior

    :return:
    """

    logger = logging.getLogger(__name__)
    logger.info(datetime.datetime.now().strftime('%A %d %b %Y, %H:%M:%S.%f'))

    # Data
    data, specifications_ = src.data.interface.Interface(s3_parameters=s3_parameters).exc()

    # Each institution's series
    messages = src.algorithms.interface.Interface(data=data).exc(specifications_=specifications_)
    logger.info(messages)

    # Transfer
    src.transfer.interface.Interface(
        connector=connector, service=service, s3_parameters=s3_parameters).exc()

    # Delete cache
    src.functions.cache.Cache().exc()


if __name__ == '__main__':

    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n\n',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Classes
    import src.algorithms.interface
    import src.data.interface
    import src.functions.cache
    import src.preface.interface
    import src.transfer.interface

    connector, s3_parameters, service = src.preface.interface.Interface().exc()

    main()

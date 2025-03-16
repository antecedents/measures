"""Module main.py"""
import logging
import os
import sys


def main():
    """

    :return:
    """

    logger: logging.Logger = logging.getLogger(__name__)

    # Steps
    # src.data.interface.Interface(s3_parameters=s3_parameters).exc()
    src.decompositions.interface.Interface().exc()

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
    import src.data.interface
    import src.functions.cache
    import src.preface.interface
    import src.transfer.interface
    import src.decompositions.interface

    # connector, s3_parameters, service = src.preface.interface.Interface().exc()

    main()

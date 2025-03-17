"""Module main.py"""
import os
import sys


def main():
    """

    :return:
    """

    # Steps
    # src.data.interface.Interface(s3_parameters=s3_parameters).exc()
    # src.decompositions.interface.Interface().exc()
    src.metrics.interface.Interface().exc()

    # Delete cache
    src.functions.cache.Cache().exc()


if __name__ == '__main__':

    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Classes
    import src.data.interface
    import src.decompositions.interface
    import src.functions.cache
    import src.metrics.interface
    import src.preface.interface
    import src.transfer.interface

    # connector, s3_parameters, service = src.preface.interface.Interface().exc()

    main()

"""Module specifications.py"""
import typing

class Specifications(typing.NamedTuple):
    """
    The data type class ⇾ Seasonal

    Attributes
    ----------
    health_board_code :
        A health board code
    health_board_name:
        The health board name
    hospital_code:
        A hospital code
    hospital_name:
        The hospital's name
    """

    health_board_code: str
    health_board_name: str
    hospital_code: str
    hospital_name: str

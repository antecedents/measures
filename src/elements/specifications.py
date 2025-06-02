"""Module specifications.py"""
import typing

class Specifications(typing.NamedTuple):
    """
    The data type class ⇾ Specifications

    Attributes
    ----------

    hospital_code:
        A hospital code
    hospital_name:
        The hospital's name
    health_board_code :
        A health board code
    health_board_name:
        The health board name
    post_code:
        Post Code
    hscp_code:
        HSCP
    council_area:
        Council Area
    intermediate_zone:
        Intermediate Zone
    data_zone:
        Data Zone
    """

    hospital_code: str
    hospital_name: str
    health_board_code: str
    health_board_name: str
    post_code: str
    hscp_code: str
    council_area: str
    intermediate_zone: str
    data_zone: str

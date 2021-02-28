
import os
from .kraken_exceptions import (
    ResponseException,
    NoResults
)


def get_root_directory():
    """
    Return the absolute form of the root directory
    """
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def check_file_existence(path: str) -> bool:
    """
    Returns True if files exists, False if not.
    """
    return os.path.exists(path)


def request_checker(response: dict):
    """
    Function that looks for errors or empty results and raise Errors accordingly
    """
    if response["error"]:
        raise ResponseException(response["error"][0])
    if "result" not in response:
        raise NoResults("No results were found")

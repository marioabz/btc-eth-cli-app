
import os
from .kraken.exceptions import (
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

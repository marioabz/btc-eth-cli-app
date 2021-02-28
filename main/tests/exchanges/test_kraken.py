
import os
import pytest
from main import get_root_directory
from main import (
    KrakenAPI,
    ResponseException,
)


EXISTING_FILE = "api.key"
NON_EXISTING_FILE = "abc.def"
WRONG_API_KEY_FILE = "api2.key"
ROOT_DIRECTORY = get_root_directory()


@pytest.fixture
def balances_response():
    return ("A", "B"), {
        "XETH": "0.0058492",
        "XBT": "0.0058697"
    }


@pytest.fixture
def orders_response():
    return ("A", "B", "C", "D", "E"), \
           {
            "ABCDE": {"opentm": "1614488110",
                      "descr": {"pair": "AB", "order": "a 0.0 @ l 0.0"}, "vol": "0.01"},
           }


def test_set_api():
    """
    Raises if the api file does not exist
    """
    with pytest.raises(FileNotFoundError):
        _ = KrakenAPI(NON_EXISTING_FILE)


def test_balances_response(balances_response):
    """
    Test balance's response format
    """
    columns, balances = balances_response
    for asset, value in balances.items():
        assert isinstance(asset, str)
        assert isinstance(value, str)


def test_orders_response(orders_response):
    """
    Test order's response format
    """
    _, balances = orders_response
    for order_id, item in balances.items():
        assert isinstance(order_id, str)
        assert isinstance(item, dict)
        assert isinstance(item["opentm"], str)
        assert isinstance(item["descr"]["pair"], str)
        assert isinstance(item["descr"]["order"], str)
        assert isinstance(item["vol"], str)


def test_balances_file_saving(balances_response):
    columns, balances = balances_response
    KrakenAPI.save(KrakenAPI.balances_file_name, "A", *columns, **balances)
    balances_file = f"{get_root_directory()}/{KrakenAPI.balances_file_name}"
    assert os.path.exists(balances_file)
    os.remove(balances_file)


def test_orders_file_saving(orders_response):
    columns, orders = orders_response
    KrakenAPI.save(KrakenAPI.open_orders_file_name, "B", *columns, **orders)
    orders_file = f"{get_root_directory()}/{KrakenAPI.open_orders_file_name}"
    assert os.path.exists(orders_file)
    os.remove(orders_file)

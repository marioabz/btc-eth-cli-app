
import pytest

from unittest.mock import patch

from mocks import (
    FakeAPI,
    FailingAPI,
    FakeKrakenAPI,
)

from main.interfaces import (
    load_kraken_trades,
    load_kraken_balances,
    load_bitcoin_balances,
    load_kraken_open_orders,
    load_ethereum_adresseses_info,
    BitcoinException,
    EthereumException,
    KrakenException
)


@pytest.fixture
def bitcoin_addresses():
    return (
        "1KFHE7w8BhaENAswwryaoccDb6qcT6DbYY",
        "33T3ELDqkeE7K7UgFRm2ZASftHJ7mT4qbA",
        "bc1q9kja7t2zxz0ze4lcgxf0l07pygpc69ws528lj9",
    )


@pytest.fixture
def ethereum_addresses():
    return (
        "0xF8df999f88Fd5691c961FeEB5b359B06e6A21b74",
        "0x1CbF40Fb9454e920eE53389b2e86D570bcF59415",
    )


@patch("main.interfaces.BitcoinAPI.get_balance", new=FakeAPI.get_balance)
def test_interface_handling_bitcoin_balances(bitcoin_addresses):
    balance = "0.0001"
    mock_response = {address: balance for address in bitcoin_addresses}
    balance_sheet = load_bitcoin_balances(bitcoin_addresses, 0)
    assert balance_sheet == mock_response


@patch("main.interfaces.EthereumAPI.get_address_information", new=FakeAPI.get_address_information)
def test_interface_handling_ethereum_balances(ethereum_addresses):
    mocked_results = FakeAPI().get_address_information("")
    mocked_ethereum_info = dict()
    for address in ethereum_addresses:
        mocked_ethereum_info[address] = dict()
        for token in mocked_results:
            mocked_ethereum_info[address][token] = dict()
            mocked_ethereum_info[address][token] = mocked_results[token]["info"]
    result = load_ethereum_adresseses_info(ethereum_addresses, 0)
    assert result == mocked_ethereum_info


@patch("main.interfaces.BitcoinAPI.get_balance", new=FailingAPI.raise_rate_limit_exception)
def test_catching_bitcoin_rate_limit_exception(bitcoin_addresses):
    with pytest.raises(BitcoinException):
        _ = load_bitcoin_balances(bitcoin_addresses, 0)


@patch("main.interfaces.BitcoinAPI.get_balance", new=FailingAPI.raise_bad_request_exception)
def test_catching_bitcoin_bad_request_exception(bitcoin_addresses):
    with pytest.raises(BitcoinException):
        _ = load_bitcoin_balances(bitcoin_addresses, 0)


@patch("main.interfaces.EthereumAPI.get_address_information", new=FailingAPI.raise_error_in_ethereum_api)
def test_catching_ethereum_api_exception(ethereum_addresses):
    with pytest.raises(EthereumException):
        _ = load_ethereum_adresseses_info(ethereum_addresses, 0)


@patch("main.interfaces.KrakenAPI.get_balances", new=FakeKrakenAPI.get_balances)
def test_kraken_balances_response():
    balances = load_kraken_balances("api.key")
    _, fake_balances = FakeKrakenAPI("").get_balances()
    assert balances == fake_balances


@patch("krakenex.API.query_private", new=FakeKrakenAPI.get_empty_results)
def test_catching_kraken_no_results_exception():
    with pytest.raises(KrakenException):
        _ = load_kraken_balances("api.key")


@patch("krakenex.API.query_private", new=FakeKrakenAPI.get_empty_results)
def test_catching_kraken_response_exception():
    with pytest.raises(KrakenException):
        _ = load_kraken_balances("api.key")


@patch("main.interfaces.KrakenAPI.get_open_orders", new=FakeKrakenAPI.get_open_orders)
def test_kraken_open_orders():
    orders = load_kraken_open_orders("api.key")
    _, fake_orders = FakeKrakenAPI("").get_open_orders()
    assert orders == fake_orders


@patch("main.interfaces.KrakenAPI.get_trades", new=FakeKrakenAPI.get_open_orders)
def test_kraken_trades():
    trades = load_kraken_trades("api.key")
    _, fake_trades = FakeKrakenAPI("").get_open_orders()
    assert trades == fake_trades

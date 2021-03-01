
import pytest


@pytest.fixture
def bitcoin_addresses():
    return (
        "1"
        "1KFHE7w8BhaENAswwryaoccDb6qcT6DbYY",
        "33T3ELDqkeE7K7UgFRm2ZASftHJ7mT4qbA",
        "bc1q9kja7t2zxz0ze4lcgxf0l07pygpc69ws528lj9",
    )


@pytest.fixture
def ethereum_addresses():
    return (
        "2"
        "0xF8df999f88Fd5691c961FeEB5b359B06e6A21b74",
        "0x1CbF40Fb9454e920eE53389b2e86D570bcF59415",
    )


def test_invalid_bitcoin_address_raises_exception():
    assert False


def test_invalid_ethereum_address_raises_exception():
    assert False


def test_addresses_input_and_grouping():
    assert False


def test_bitcoin_balances():
    assert False


def test_ethereum_balances():
    assert False


from main import get_address_type


BITCOIN = "btc"
ETHEREUM = "eth"
ethereum_address = "0x0a589899a744c89a70e27db251f09c82ee1bd347"
bitcoin_addresses = {
    "p2sh": "3F5B6rct1TPW3JGuczdVLQ9wiTchqPT4od",
    "p2pkh": "1FuxNbFZKoVVDKTbL5pQMMXqpCbozg8mWL",
    "segwit": "bc1qyy30guv6m5ez7ntj0ayr08u23w3k5s8vg3elmxdzlh8a3xskupyqn2lp5w",
}


def test_ethereum_address_validation():
    """
    Test whether function recognizes an ethereum address
    """
    assert get_address_type(ethereum_address) == ETHEREUM


def test_bitcoin_p2sh_address_validation():
    """
        Test whether function recognizes an P2SH bitcoin address
    """
    assert get_address_type(bitcoin_addresses["p2sh"]) == BITCOIN


def test_bitcoin_p2pkh_address_validation():
    """
        Test whether function recognizes an P2PKH bitcoin address
    """
    assert get_address_type(bitcoin_addresses["p2pkh"]) == BITCOIN


def test_bitcoin_segwit_address_validation():
    """
        Test whether function recognizes an Segwit bitcoin address
    """
    assert get_address_type(bitcoin_addresses["segwit"]) == BITCOIN


def test_incomplete_ethereum_address():
    """
        Test function address is invalid and function returns empty string
    """
    assert get_address_type(ethereum_address[:-2]) == ""


def test_incomplete_bitcoin_address():
    """
        Test function address is invalid and function returns empty string
    """
    assert get_address_type(bitcoin_addresses["p2pkh"][:-1]) == ""


def test_ignores_unvalid_data():
    """
        Test function returns an empty string for nonsense data inputs
    """
    assert get_address_type("a") == ""
    assert get_address_type("1") == ""
    assert get_address_type("0x123") == ""
    assert get_address_type("bc1" + "0x0a589899a744c89a70e27db251f09c82ee1bd347") == ""

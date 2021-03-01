import requests

from decimal import Decimal

from typing import (
    Dict,
)

from .exceptions import APIException

# Keywords of a dictionary
tokens, error, decimals = "tokens", "error", "decimals"
token_info, name, balance = "tokenInfo", "name", "balance"
price, rate = "price", "rate"


class EthereumAPI(object):
    """
    EthereumAPI is an interface to handle Bitcoin requests.
    This API does not start a session since the application makes just one
    request once the application is started.
    """

    def __init__(self):
        self.api = "https://api.ethplorer.io"

    def get_address_information(self, address: str) -> Dict:
        """
        Fetch address information.

        Information:
            Address balance [ether, price rate, etc.]
            Address tokens balance (if any) [amout, decimals, price rate]

        Returns:
            A dictionary with tokens and ether as keys and an object
            with balance and price rate (if any) per currency as value.

        """
        path = f"getAddressInfo/{address}?apiKey=freekey"
        url = f"{self.api}/{path}"
        result = dict()
        response = requests.get(url)
        data = response.json()
        if error in data:
            msg = f"Error: {data[error]['message']}. Code: {data[error]['code']}"
            raise APIException(msg)
        result["ETH"] = {
            "info": EthereumAPI.get_currency_object(
                data["ETH"][balance],
                data["ETH"][price][rate]
            )
        }
        if tokens not in data:
            return result
        return EthereumAPI.process_tokens(data, result)

    @staticmethod
    def process_tokens(data: Dict[str, Dict], result: Dict[str, Dict]) -> Dict[str, Dict]:
        """
        Processes tokens and returns modified given object with found tokens.
        """
        for token in data[tokens]:
            if token_info not in token:
                continue
            token_name = token[token_info][name]

            if EthereumAPI.is_token_spam(token_name):
                continue

            value = Decimal(token[balance])
            if decimals in token[token_info]:
                value = value/10**int(token[token_info][decimals])
            if token[token_info][price]:
                _rate = token[token_info][price][rate]
            else:
                _rate = "N/A"
            result[token_name] = {
                "info": EthereumAPI.get_currency_object(str(value), _rate)
            }
        return result

    @staticmethod
    def get_currency_object(value: str, _rate: str) -> Dict[str, str]:
        """
        Returns a currency object
        """
        result = dict()
        result["balance"] = value
        result["rate"] = _rate
        return result

    @staticmethod
    def is_token_spam(_name: str) -> bool:
        """
        Returns True is token is spam, False if not
        """
        for pattern in ("www", "WWW", "!"):
            if pattern in _name:
                return True
        return False

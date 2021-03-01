
from main.interfaces.bitcoin.exceptions import (
    BadRequestException,
    RateLimitExceededException,
)

from main.interfaces.ethereum.exceptions import APIException


class FakeAPI(object):

    """
    Allows to return mock data to interface functions to allow interface testing
    """

    def get_balance(self, address):
        return "0.0001"

    def get_address_information(self, address):
        fake_ether_balance, fake_tokens_balance = dict(), dict()
        fake_ether_balance["ETH"] = {"info": {
            "balance": "1",
            "rate": "1500"
        }}
        fake_tokens_balance["Compound"] = {"info": {
            "balance": "100",
            "rate": "50"
        }}
        fake_tokens_balance["Aave"] = {"info": {
            "balance": "25",
            "rate": "12"
        }}
        return {**fake_ether_balance, **fake_tokens_balance}


class FailingAPI(object):

    def raise_rate_limit_exception(self, address):
        raise RateLimitExceededException

    def raise_bad_request_exception(self, address):
        raise BadRequestException

    def raise_error_in_ethereum_api(self, address):
        raise APIException


class FakeKrakenAPI(object):

    def __init__(self, file):
        pass

    def get_balances(self):
        return ("Currency", "Balance"), {"XBT": "0.0001", "XETH": "0.02"}

    def get_empty_results(self, method):
        return {"error": []}

    def get_balances_with_error_code(self, method):
        return {"error": ['ABC:DEF']}

    def get_open_orders(self):
        """
        Method can supply fake data to KrakenAPI.get_open_orders and
        KrakenAPI.get_trades since they have the same format
        """
        return (), \
               {"AB-CD": {
                   "pair": "XETHZUSD",
                   "vol": "0.005896",
                   "price": "1600"
               }}

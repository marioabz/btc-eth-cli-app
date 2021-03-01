
import requests

from decimal import Decimal
from .exceptions import (
    BadRequestException,
    RateLimitExceededException,
)


class BitcoinAPI(object):

    """
    BitcoinAPI is an interface to handle Bitcoin requests.
    This API does not start a session since the application makes just one
    request once the application is started.
    """

    def __init__(self):
        self.uri = "https://api.blockcypher.com/"
        self.version = "v1"
        self.currency = "btc"

    def get_balance(self, address) -> Decimal:
        """
        Fetch balance sum from all unspent transactions with confirmations > 0
        """
        path = f"main/addrs/{address}/balance"
        url = f"{self.uri}/{self.version}/{self.currency}/{path}"
        response = requests.get(url)
        data = response.json()
        status_code = response.status_code
        if status_code == 429:
            msg = "Rate limit exceeded: Rate limit is 200 requests per second."
            raise RateLimitExceededException(msg)
        if status_code != 200:
            msg = f"HTTP Code: {status_code}, Error: {data['error']}"
            raise BadRequestException(msg)
        return Decimal(data["final_balance"])

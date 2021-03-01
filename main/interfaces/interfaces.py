
import time

from typing import (
    List,
    Dict,
    Tuple
)

from .bitcoin import (
    BitcoinAPI,
    RateLimitExceededException,
    BadRequestException,
)

from .ethereum import (
    EthereumAPI,
    APIException
)

from .kraken import (
    KrakenAPI,
    NoResults,
    ResponseException,
)

from .exceptions import (
    BitcoinException,
    EthereumException,
    KrakenException,
)


def load_bitcoin_balances(addresses: List[str], sleep: float = 1):
    """
    Loads addresses, request balances to API and prepares dictionary
    to be saved.
    """
    api = BitcoinAPI()
    try:
        result = dict()
        if not addresses:
            return result
        for address in addresses:
            balance = api.get_balance(address)
            result[address] = balance
            # BitcoinAPI has as rate limit 3 requests per second, 200 per hour.
            # Sleep half a second.
            time.sleep(sleep)
    except (RateLimitExceededException, BadRequestException) as e:
        msg = f"Error: {e}"
        raise BitcoinException(msg)
    return result


def load_ethereum_adresseses_info(addresses: List[str], sleep: float = 1) -> Dict:
    """
    Loads addresses, request address info to API and saves dictionary
    """
    try:
        balances = dict()
        if not addresses:
            return balances
        api = EthereumAPI()
        for address in addresses:
            info = api.get_address_information(address)
            balances[address] = dict()
            for key in info:
                balances[address][key] = info[key]["info"]
            # Sleep half a second.
            time.sleep(sleep)
    except APIException as e:
        msg = f"Error: {e}"
        raise EthereumException(msg)
    return balances


def load_kraken_balances(api_key_file: str) -> Dict[str, str]:
    """
    Loads API keys, requests balances to Kraken REST API

    Returns:
        dict[]: sheet of balances (if any)
    """
    api = KrakenAPI(api_key_file)
    try:
        _, balances = api.get_balances()
        return balances
    except NoResults as e:
        msg = f"{e} regarding Balances"
        raise KrakenException(msg)
    except ResponseException as e:
        msg = f"Error: {e}"
        raise KrakenException(msg)


def load_kraken_open_orders(api_key_file: str) -> Dict:
    """
    Check for empty results
    """
    try:
        api = KrakenAPI(api_key_file)
        columns, orders = api.get_open_orders()
        KrakenAPI.save(
            KrakenAPI.trades_file_name,
            "Trades on Kraken",
            *columns,
            **orders
        )
        return orders
    except NoResults as e:
        msg = f"{e} regarding Open Orders"
        raise KrakenException(msg)
    except ResponseException as e:
        msg = f"Error: {e}"
        raise KrakenException(msg)


def load_kraken_trades(api_key_file: str):
    """
    Loads API keys, fetch trades history, saves them on a file (if any)
    """
    try:

        api = KrakenAPI(api_key_file)
        columns, trades = api.get_trades()
        KrakenAPI.save(
            KrakenAPI.trades_file_name,
            "Trades on Kraken",
            *columns,
            **trades
        )
        return trades
    except NoResults as e:
        msg = f"{e} regarding Trades"
        raise KrakenException(msg)
    except ResponseException as e:
        msg = f"Error: {e}"
        raise KrakenException(msg)

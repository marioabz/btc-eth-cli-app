
import krakenex
import datetime

from typing import (
    Dict,
    Iterable,
    Tuple
)

from .exceptions import (
    NoResults,
    ResponseException
)

from ..helpers import (
    get_root_directory,
    check_file_existence,
)

columns_orders = {
    "Id": "Id",
    "pair": "Pair",
    "vol": "Volume",
    "opentm": "Opened at",
    "order": "Description",
}

columns_trades = {
    "Id": "Id",
    "pair": "Pair",
    "vol": "Volume",
    "price": "Price",
    "time": "Executed at",
    "ordertxid": "From Order",
    "fee": "Fee"
}

# Variables with needed keywords to access request's response dictionary.
result, _open, pair = "result", "open", "pair"
descr, vol, opened_at = "descr", "vol", "opentm"
trades, price, time = "trades", "price", "time"
order_id, fee, order = "ordertxid", "fee", "order"


class KrakenAPI(object):
    """
    KrakenAPI is a class that allows to fetch private data through an API via REST.

    Class has 2 properties:
        balances_file_name (str): File where balances are stored
        open_orders_file_name (str): File where open orders are stored
    """

    trades_file_name = "kraken_trades.txt"
    balances_file_name = "kraken_balances.txt"
    open_orders_file_name = "kraken_open_orders.txt"

    def __init__(self, key_file: str):
        self.key_file = key_file
        self.api = krakenex.API()
        self.initialize_api()

    @staticmethod
    def request_checker(response: dict):
        """
        Function that looks for errors or empty results and raise Errors accordingly
        """
        if response["error"]:
            raise ResponseException(response["error"][0])
        if "result" not in response:
            raise NoResults("No results were found")

    def initialize_api(self):
        """
        Check for file existance, prepares API for calls if nothing went wrong.
        """
        abs_api_key_path = f"{get_root_directory()}/{self.key_file}"
        file_exists = check_file_existence(abs_api_key_path)
        if not file_exists:
            raise FileNotFoundError(abs_api_key_path)
        self.api.load_key(abs_api_key_path)

    def get_balances(self) -> Tuple[Tuple[str, str], Dict[str, str]]:
        """
        Fetch assets balances. Returns assets whose balances surpasses a predetermined threshold.
        """
        response = self.api.query_private('Balance')
        KrakenAPI.request_checker(response)
        return ("Currency", "Balance"), response["result"]

    def get_open_orders(self) -> Tuple[Iterable, Dict[str, Dict[str, dict]]]:
        """
        Fetch open orders
        """
        response = self.api.query_private("OpenOrders")
        KrakenAPI.request_checker(response)
        formatted_response = dict()
        for _id, item in response[result][_open].items():
            if _id not in formatted_response:
                formatted_response[_id] = dict()
            formatted_response[_id][pair] = item[descr][pair]
            formatted_response[_id][vol] = item[vol]
            formatted_response[_id]["opened_at"] = item[opened_at]
            formatted_response[_id][descr] = item[descr][order]
        return tuple(columns_orders.values()), formatted_response

    def get_trades(self) -> Tuple[Iterable, Dict[str, Dict[str, dict]]]:
        """
        Fetch trades without any type of limit or parameters.
        """
        response = self.api.query_private("TradesHistory")
        KrakenAPI.request_checker(response)
        formatted_response = dict()
        for _id, item in response[result][trades].items():
            if _id not in formatted_response:
                formatted_response[_id] = dict()
            formatted_response[_id][pair] = item[pair]
            formatted_response[_id][vol] = item[vol]
            formatted_response[_id][price] = item[price]
            formatted_response[_id][time] = item[time]
            formatted_response[_id][fee] = item[fee]
        return tuple(columns_trades.values()), formatted_response

    @staticmethod
    def save(file_name, header, *columns, **response):
        """
        Creates or truncates file and writes new data.
        """
        balances_file = f"{get_root_directory()}/{file_name}"
        file = open(balances_file, "w+")
        file.write(f"{header}\tLast update: {datetime.datetime.now()}\n\n\n")
        for column in columns:
            file.write(f"{column}\t")
        file.write("\n")
        for first_column, item in response.items():
            if isinstance(item, str):
                file.write(f"{first_column}\t{item}\n")
                continue
            file.write(f"{first_column}\t")
            for _, column in item.items():
                file.write(f"{column}\t")
            file.write("\n")


if __name__ == "__main__":
    api = KrakenAPI("api.key")
    balance_cols, balances = api.get_balances()
    api.save(KrakenAPI.balances_file_name, "Balances on Kraken", *balance_cols, **balances)
    orders_cols, orders = api.get_open_orders()
    api.save(KrakenAPI.open_orders_file_name, "Open orders on Kraken", *orders_cols, **orders)

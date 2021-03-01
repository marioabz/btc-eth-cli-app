
import click

from typing import (
    Dict,
    Iterable,
    Callable
)

from interfaces import (
    KrakenException,
    BitcoinException,
    EthereumException,
)

from interfaces import (
    load_kraken_trades,
    load_kraken_balances,
    load_bitcoin_balances,
    load_kraken_open_orders,
    load_ethereum_adresseses_info,
)


def print_bitcoin_balances(addresses: set, printer: Callable):

    try:
        balances = load_bitcoin_balances(addresses)
        for address, value in balances.items():
            msg = f"Bitcoin wallet [ {address} ] has balance of: {value} satoshis"
            printer(msg)
        printer("\n")
    except BitcoinException as e:
        printer(e, color="red")


def print_ethereum_balances(addresses: set, printer: Callable):
    try:
        ethereum_info = load_ethereum_adresseses_info(list(addresses))
        for address in ethereum_info:
            msg = f"Balances of {address}:"
            printer(msg)
            for currency in ethereum_info[address]:
                msg = f"\tCurrency: {currency}, Balance: {ethereum_info[address][currency]['balance']}"
                printer(msg)
            printer("\n")

    except EthereumException as e:
        printer(e, color="red")


def kraken_wrapper(func: Callable):
    def wrapper(file_name, printer):
        try:
            func(file_name, printer)
        except KrakenException as e:
            printer(" ".join(e.args), color="red")
    return wrapper


@kraken_wrapper
def print_kraken_balances(file_name: str, printer: Callable):
    balances = load_kraken_balances(file_name)
    printer("Balances on Kraken")
    for currency in balances:
        msg = f"Currency: {currency}, Balance: {balances[currency]}"
        printer(msg)


@kraken_wrapper
def print_kraken_trades(file_name: str, printer: Callable):

    trades = load_kraken_trades(file_name)
    if not trades:
        printer("No trades were found")
        return
    printer("Trades on Kraken")
    for trade, item in trades.items():
        msg = f"Trade:[{trade}],  Pair:[{item['pair']}], Volume:[{item['vol']}], " \
            f"Opened at:[{item['time']}], Fee: [{item['fee']}] "
        printer(msg)
    printer("\n")


@kraken_wrapper
def print_kraken_orders(file_name: str, printer: Callable):
    orders = load_kraken_open_orders(file_name)
    if not orders:
        printer("No orders were found")
        return
    printer("Orders on Kraken")
    for order, item in orders.items():
        msg = f"Order:[{order}],  Pair:[{item['pair']}], Volume:[{item['vol']}], " \
            f"Opened at:[{item['opened_at']}], Short Version: [{item['descr']}] "
        printer(msg)
    printer("\n")


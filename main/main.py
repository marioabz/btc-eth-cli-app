
import click


from typing import (
    Dict,
    Tuple,
)

from cli_handler import (
    print_kraken_trades,
    print_kraken_orders,
    print_kraken_balances,
    print_bitcoin_balances,
    print_ethereum_balances,
)

from helpers import (
    get_address_type,
    echo_with_spaces
)


def print_with_color(msg, color="green"):
    click.echo(click.style(msg, color))


@click.group()
def cli():
    pass


@echo_with_spaces
def echo_addresses(addresses: Dict[str, Dict[str, int]]):
    """
    Echo Bitcoin and/or Ethereum addresses
    """
    for currency in addresses:
        click.echo(f"Your {currency} addresses are:")
        for address in addresses[currency]:
            click.echo(f"{address}")
        click.echo("-"*45)


@cli.command()
def start(**kwargs):
    addresses = list()
    addresses_per_type = dict()
    api_key_file = ""
    try:
        while True:
            address = input("Enter address to be scanned: [Press Ctrl+C to continue]\n")
            _type = get_address_type(address)
            if not _type:
                print_with_color(f"'{address}' is not a valid Ethereum "
                                 f"or Bitcoin address!", color="red")
                continue
            if _type not in addresses_per_type:
                addresses_per_type[_type] = set()
            addresses_per_type[_type].add(address)
            addresses.append(address)
    except KeyboardInterrupt:
        print_with_color("\n")
        pass
    try:
        api_key_file = input("Enter your api key file name: ")
    except KeyboardInterrupt:
        print_with_color("\n")
        pass
    return addresses_per_type, api_key_file


@cli.command()
@click.argument("args", nargs=-1)
def bitcoin_balances(args, **kwargs):
    click.clear()
    print_bitcoin_balances(args, print_with_color)


@cli.command()
@click.argument("args", nargs=-1)
def ethereum_balances(args, **kwargs):
    click.clear()
    print_ethereum_balances(args, print_with_color)


@cli.command()
@click.argument("file", nargs=-1)
def kraken_balances(file, **kwargs):
    click.clear()
    file = "".join(file)
    print_kraken_balances(file, print_with_color)


@cli.command()
@click.argument("file", nargs=-1)
def kraken_trades(file, **kwargs):
    click.clear()
    file = "".join(file)
    print_kraken_trades(file, print_with_color)


@cli.command()
@click.argument("file", nargs=-1)
def kraken_open_orders(file, **kwargs):
    click.clear()
    file = "".join(file)
    print_kraken_orders(file, print_with_color)


def main():
    """
    Main application
    """
    try:
        click.clear()
        addresses, api_key_file = start(standalone_mode=False)
        if not addresses and not api_key_file:
            print_with_color("\nNo addresses or api key file name were provided!", color="yellow")
            return
        while True:
            arg = api_key_file
            value = click.prompt(
                'Select a command to run',
                type=click.Choice(list(cli.commands.keys()) + ['exit'])
            )
            if value == "exit":
                break

            if "bitcoin" in value:
                if "btc" not in addresses:
                    msg = "You did not provided addresses for this currency"
                    print_with_color(msg, color="red")
                    continue
                arg = addresses["btc"]

            if "ethereum" in value:
                if "eth" not in addresses:
                    msg = "You did not provided addresses for this currency"
                    print_with_color(msg, color="red")
                    continue
                arg = addresses["eth"]

            if "kraken" in value and not api_key_file:
                print_with_color("No API Key file were provided", color="red")
                continue

            if value == "start":
                click.echo("Application is already started!")
                continue
            cli.commands[value](arg, standalone_mode=False)
    except (KeyboardInterrupt, click.exceptions.Abort):
        print_with_color("\nBye!", color="yellow")


if __name__ == "__main__":
    main()

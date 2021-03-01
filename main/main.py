
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
        api_key_file = input("Enter your api key file: ")
    except KeyboardInterrupt:
        print_with_color("\n")
        pass
    return addresses_per_type, api_key_file


def main():
    """
    Main application
    """
    click.clear()
    addresses, api_key_file = start(standalone_mode=False)
    try:
        while True:
            arg = api_key_file
            value = click.prompt(
                'Select a command to run',
                type=click.Choice(list(cli.commands.keys()) + ['exit'])
            )
            if value == "exit":
                break

            if value == "start":
                click.echo("Application is already started!")
                continue
            cli.commands[value](arg, standalone_mode=False)
    except (KeyboardInterrupt, click.exceptions.Abort):
        print_with_color("\nBye!", color="yellow")


if __name__ == "__main__":
    main()

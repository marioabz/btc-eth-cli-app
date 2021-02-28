
import click
from typing import (
    Dict,
    Tuple,
    List
)

from helpers import (
    get_address_type,
    echo_with_spaces
)


@click.group()
def cli():
    pass


@cli.command()
@click.option("--addresses")
@click.option("--api-key-file")
@click.argument('addresses', nargs=-1)
def init(addresses: Tuple[str], api_key_file: str, **kwargs) -> (Dict[Dict[str:int]], str):
    """
    Allows application to initialize with an unlimited amount of addresses
    """
    if not addresses:
        click.echo("No addresses were provided :(")
        return addresses
    addresses_per_type = dict()
    for address in addresses:
        currency = get_address_type(address)
        if not currency:
            click.echo(f"'{address}' is not a valid "
                       f"Ethereum or Bitcoin address!")
            continue
        if currency not in addresses_per_type:
            addresses_per_type[currency] = dict()
        addresses_per_type[currency][address] = 1
    return addresses_per_type, api_key_file


@echo_with_spaces
def echo_addresses(addresses):
    """
    Echo Bitcoin and/or Ethereum addresses
    """
    for currency in addresses:
        click.echo(f"Your {currency} addresses are:")
        for address in addresses[currency]:
            click.echo(f"{address}")
        click.echo("-"*45)


def main():
    addresses, key_file = init(standalone_mode=False)
    if not addresses:
        return
    echo_addresses(addresses)
    while True:
        value = click.prompt(
            'Select a command to run',
            type=click.Choice(list(cli.commands.keys()) + ['exit'])
        )
        if value == "exit":
            break
        if value == "init":
            click.echo("Application is already initialized!")
            continue
        cli.commands[value](standalone_mode=False)


if __name__ == "__main__":
    main()


import eth_utils
import cryptoaddress
import bech32


def get_address_type(address: str) -> str:
    """
    Function checks whether the input address is a Bitcoin (in mainnet) or an
    Ethereum address.
    :param address:
    :return: btc, eth or ""
    """
    try:
        if eth_utils.is_address(address):
            return "eth"
        if is_valid_bech32_address(address) or cryptoaddress.BitcoinAddress(address):
            return "btc"
    except ValueError:
        return ""


def is_valid_bech32_address(value: str) -> bool:
    """Validates a bitcoin SegWit address for the mainnet
    """
    decoded = bech32.decode('bc', value)
    return decoded != (None, None)

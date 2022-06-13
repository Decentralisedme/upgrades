from brownie import accounts, network, config
import eth_utils


LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "development",
    "ganache",
    "ganache-local",
    "hardhat",
    "mainnet-fork",
    "mainnet-fork-dev",
]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    # if network.show_active() in config["networks"]:
    #     return accounts.add(config["wallets"]["from_key"])
    return accounts.add(config["wallets"]["from_key"])


# ENCODE funciton
# initializer=box.store, 1, 2... (we only have 1 variable here)
"""Encodes the function call so we can work with an initializer.
    Args:
        initializer ([brownie.network.contract.ContractTx], optional):
        The initializer function we want to call. Example: `box.store`.
        Defaults to None.
        args (Any, optional):
        The arguments to pass to the initializer function
    Returns:
        [bytes]: Return the encoded bytes.
"""


def encode_function_data(initializer=None, *args):
    #  Brownie has funct already (encode_input()),
    # but it has a problem when len of arg =0
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)


def upgrade(
    account,
    proxy,
    new_implementation_address,
    proxy_admin_contract=None,
    initializer=None,
    *args
):
    transaction = None
    # A. if we have proxyadmin contract
    if proxy_admin_contract:
        # If we have initializer
        if initializer:
            encoded_function_call = encoded_function_call(initializer, *args)
            # From ProxyAdmin we take upgradeAndCall
            transaction = proxy_admin_contract.upgradeAndCall(
                proxy.address,
                new_implementation_address,
                encode_function_data,
                {"from": account},
            )
        # If we do NOT have initializer
        else:
            transaction = proxy_admin_contract.upgrade(
                proxy.address, new_implementation_address, {"from": account}
            )
    # B. if we do NOT have Proxy admin contract, we call directly then
    else:
        if initializer:
            encoded_function_call = encoded_function_call(initializer, *args)
            transaction = proxy.upgradeAndCall(
                new_implementation_address, encode_function_data, {"from": account}
            )
        else:
            transaction = proxy.upgradeAndCall(
                new_implementation_address, {"from": account}
            )
    return transaction


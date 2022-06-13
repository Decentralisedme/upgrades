from brownie import (
    network,
    Box,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    BoxV2,
)
from scripts.helpful_scripts import get_account, encode_function_data, upgrade


def main():
    account = get_account()
    print(f"Deploying the to {network.show_active()}")
    box = Box.deploy({"from": account}, publish_source=True)

    proxy_admin = ProxyAdmin.deploy({"from": account}, publish_source=True)

    ### With Initializer
    # initializer = box.store, 1
    # box_encoded_initializer_function = encode_function_data(initializer)

    ### With No Initializer: funct says or not initializer >> then 0x
    box_encoded_initializer_function = encode_function_data()

    # Now add the Proxy Admin Constructur var
    # 1. our implementation address -box above
    # 2. Admin address >> the proxy admin (it could be us)
    # 3. _data = the implementaion encoded: box_encoded_...

    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
        publish_source=True,
    )
    print(f"Proxy deployed to {proxy}, you can now upgrade to V2!!!")
    #  we can now, on the proxy address, call functions
    #  usually would be directly: box.store(1)
    #  But we want to do it on a proxy >> We need to assign implementation ABI to the proxy
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    #  we delegate the call from Proxy (we have proxy address) to Box, as example:
    #  we also store a new vauek
    proxy_box.store(1, {"from": account})
    print(f"Printing retrieve {proxy_box.retrieve()} box function!!")
    """ 
    TO NOTICED: 
    if you store in box:
        box.store(1, {"from": account})
    then to retrive it you need to 
        box.retrieve()
    If you call:
        proxy_box.retrieve()
    The box vaue will not bee seen
    """
    # UPGRADE TO BOX-V2
    box_v2 = BoxV2.deploy({"from": account}, publish_source=True)
    # we need to call the upgradeTo function from Transparent Proxy
    #  we need to wrap things around in a function in helpfulscrip
    upgrade_transaction = upgrade(
        account, proxy, box_v2.address, proxy_admin_contract=proxy_admin
    )
    upgrade_transaction.wait(1)
    print("Proxy has been upgreated")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    proxy_box.increment({"from": account})
    print(proxy_box.retrieve())
    # BoxV2 only has increment function
    #  the functin add 1 to previous storaged data > now should be 2 (=1 from above, 1 frm increment)


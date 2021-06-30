from thor_requests import utils
from thor_requests.connect import Connect
from thor_requests.contract import Contract
from thor_requests.wallet import Wallet

def helper_deploy(connector, wallet, contract) -> str:
    ''' Deploy a smart contract and return the created contract address'''
    res = connector.deploy(wallet, contract, None, None, 0)
    assert "id" in res
    receipt = connector.wait_for_tx_receipt(res["id"])
    created_contracts = utils.read_created_contracts(receipt)
    assert len(created_contracts) == 1
    return created_contracts[0]

def helper_call(connector:Connect, caller:str, contract_addr:str, contract:Contract, func_name:str, func_params:list, value:int=0):
    '''Call on-chain, return reverted(bool), response'''
    # Call to get the balance of user's vtho
    res = connector.call(
        caller,
        contract,
        func_name,
        func_params,
        contract_addr,
        value=value
    )
    return res["reverted"], res

def helper_transact(connector:Connect, wallet:Wallet, contract_addr:str, contract:Contract, func_name:str, func_params:list, value:int=0):
    '''Transact on-chain, and return reverted(bool), receipt'''
    res = connector.transact(
        wallet,
        contract,
        func_name,
        func_params,
        contract_addr,
        value=value,
        force=True
    )
    assert res["id"]
    receipt = connector.wait_for_tx_receipt(res["id"])
    return receipt["reverted"], receipt

def helper_wait_for_block(connector:Connect, number:int=1):
    counter = 0
    for block in connector.ticker():
        counter += 1
        if counter >= number:
            break

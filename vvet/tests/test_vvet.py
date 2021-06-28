import time
import pytest
from thor_requests import utils
from .fixtures import (
    testnet_connector,
    testnet_wallet,
    vvet_contract
)

@pytest.fixture(autouse=True)
def deployed_contract(testnet_connector, testnet_wallet, vvet_contract):
    ''' Deploy smart contract before each execution, return contract address '''
    res = testnet_connector.deploy(testnet_wallet, vvet_contract, None, None, 0)
    assert "id" in res

    receipt = testnet_connector.wait_for_tx_receipt(res["id"])
    created_contracts = utils.read_created_contracts(receipt)
    assert len(created_contracts) == 1
    return created_contracts[0]

@pytest.fixture
def deposit_vet(deployed_contract, testnet_connector, testnet_wallet, vvet_contract, wei):
    ''' Add some VET to the vvet.sol '''
    res = testnet_connector.transact(
        testnet_wallet,
        vvet_contract,
        "addVET",
        [testnet_wallet.getAddress(), wei],
        deployed_contract
    )
    assert res["id"]
    receipt = testnet_connector.wait_for_tx_receipt(res["id"])
    assert utils.is_reverted(receipt) == False

def test_deposit_vet():
    ''' User deposit vet '''
    pass

def test_redeem_vet():
    ''' User redeem vet with vvet '''
    pass

def test_over_redeem_vet():
    ''' User over redeem vvet '''
    pass

def test_transfer_vvet():
    ''' User transfer his vvet '''
    pass

def test_over_transfer_vvet():
    ''' User over transfer his vvet '''
    pass

def test_approve():
    ''' Test approve of one's funds to be spend by other person '''
    pass

def test_over_approve():
    ''' Test over approve of one's funds '''
    pass

def test_claim():
    ''' Normal claim of generated vtho '''
    pass

def test_over_claim():
    ''' Over claim of generated vtho '''
    pass

def test_claim_to_other_wallet():
    ''' Claim vtho to another wallet than the caller itself '''
    pass

# def test_store(deployed_contract, testnet_connector, testnet_wallet, vvet_contract):
#     ''' Transaction of add some VET '''
#     print("wallet:addr:", testnet_wallet.getAddress())
#     contract_addr = deployed_contract
#     print("contract:addr:", contract_addr)

#     # Call to get the balance of user's vet
#     res = testnet_connector.call(
#         testnet_wallet.getAddress(),
#         vvet_contract,
#         "vetBalance",
#         [testnet_wallet.getAddress()],
#         contract_addr
#     )
#     assert res["reverted"] == False
#     assert res["decoded"]["0"] == 0  # nothing added, so no vet is there
#     print('call:vetBalance:gas:', res["gasUsed"])

#     # Call to get the balance of user's vtho
#     res = testnet_connector.call(
#         testnet_wallet.getAddress(),
#         vvet_contract,
#         "vthoBalance",
#         [testnet_wallet.getAddress()],
#         contract_addr
#     )
#     assert res["reverted"] == False
#     assert res["decoded"]["0"] == 0  # nothing added, so no vtho is there
#     print('call:vthoBalance:gas:', res["gasUsed"])

#     # Add 3 vet for the first time
#     res = testnet_connector.transact(
#         testnet_wallet,
#         vvet_contract,
#         "addVET",
#         [testnet_wallet.getAddress(), 3 * (10 ** 18)],
#         contract_addr
#     )
#     assert res["id"]

#     tx_id = res["id"]
#     receipt = testnet_connector.wait_for_tx_receipt(tx_id)
#     print('transact:addVET:gas:', receipt["gasUsed"])

#     time.sleep(12)

#     # Call to get the balance of user's vet
#     res = testnet_connector.call(
#         testnet_wallet.getAddress(),
#         vvet_contract,
#         "vetBalance",
#         [testnet_wallet.getAddress()],
#         contract_addr
#     )
#     assert res["reverted"] == False
#     assert res["decoded"]["0"] == 3 * (10 ** 18)  # 3 vet should be there
#     print('call:vetBalance:gas:', res["gasUsed"])

#     # Call to get the balance of user's vtho
#     res = testnet_connector.call(
#         testnet_wallet.getAddress(),
#         vvet_contract,
#         "vthoBalance",
#         [testnet_wallet.getAddress()],
#         contract_addr
#     )
#     assert res["reverted"] == False
#     assert res["decoded"]["0"] > 0 # Some vtho should be there
#     print('call:vthoBalance:gas:', res["gasUsed"])

#     # Add more VET (3) to the user
#     res = testnet_connector.transact(
#         testnet_wallet,
#         vvet_contract,
#         "addVET",
#         [testnet_wallet.getAddress(), 3 * (10 ** 18)],
#         contract_addr
#     )
#     assert res["id"]

#     tx_id = res["id"]
#     receipt = testnet_connector.wait_for_tx_receipt(tx_id)
#     print('transact:addVET:gas:', receipt["gasUsed"])

#     time.sleep(12)

#     # Call to get the balance of user's vet
#     res = testnet_connector.call(
#         testnet_wallet.getAddress(),
#         vvet_contract,
#         "vetBalance",
#         [testnet_wallet.getAddress()],
#         contract_addr
#     )
#     assert res["reverted"] == False
#     assert res["decoded"]["0"] == 6 * (10 ** 18)  # 6 vet should be there
#     print('call:vetBalance:gas:', res["gasUsed"])

#     # Call to get the balance of user's vtho
#     res = testnet_connector.call(
#         testnet_wallet.getAddress(),
#         vvet_contract,
#         "vthoBalance",
#         [testnet_wallet.getAddress()],
#         contract_addr
#     )
#     assert res["reverted"] == False
#     assert res["decoded"]["0"] > 0 # Some vtho should be there
#     print('call:vthoBalance:gas:', res["gasUsed"])
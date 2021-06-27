import time
import pytest
from thor_requests import utils
from .fixtures import (
    testnet_connector,
    testnet_wallet,
    vthobox_contract
)

@pytest.fixture(autouse=True)
def deploy_contract(testnet_connector, testnet_wallet, vthobox_contract):
    ''' test the storage gas '''
    res = testnet_connector.deploy(testnet_wallet, vthobox_contract, None, None, 0)
    assert "id" in res  # Should contain a {'id': '0x...' }
    # print(f"deploy_vvet_tx_id: {res['id']}")
    tx_id = res["id"]
    # Should have the deployed contract address now
    receipt = testnet_connector.wait_for_tx_receipt(tx_id)
    created_contracts = utils.read_created_contracts(receipt)
    assert len(created_contracts) == 1
    # print(f"created_vvet_address: {created_contracts[0]}")
    return created_contracts[0]

def test_store(deploy_contract, testnet_connector, testnet_wallet, vthobox_contract):
    ''' Transaction of add some VET '''
    print("wallet:addr:", testnet_wallet.getAddress())
    contract_addr = deploy_contract
    print("contract:addr:", contract_addr)

    # Call to get the balance of user's vet
    res = testnet_connector.call(
        testnet_wallet.getAddress(),
        vthobox_contract,
        "vetBalance",
        [testnet_wallet.getAddress()],
        contract_addr
    )
    assert res["reverted"] == False
    assert res["decoded"]["0"] == 0  # nothing added, so no vet is there
    print('call:vetBalance:gas:', res["gasUsed"])

    # Call to get the balance of user's vtho
    res = testnet_connector.call(
        testnet_wallet.getAddress(),
        vthobox_contract,
        "vthoBalance",
        [testnet_wallet.getAddress()],
        contract_addr
    )
    assert res["reverted"] == False
    assert res["decoded"]["0"] == 0  # nothing added, so no vtho is there
    print('call:vthoBalance:gas:', res["gasUsed"])

    # Add 3 vet for the first time
    res = testnet_connector.transact(
        testnet_wallet,
        vthobox_contract,
        "addVET",
        [testnet_wallet.getAddress(), 3 * (10 ** 18)],
        contract_addr
    )
    assert res["id"]

    tx_id = res["id"]
    receipt = testnet_connector.wait_for_tx_receipt(tx_id)
    print('transact:addVET:gas:', receipt["gasUsed"])

    time.sleep(12)

    # Call to get the balance of user's vet
    res = testnet_connector.call(
        testnet_wallet.getAddress(),
        vthobox_contract,
        "vetBalance",
        [testnet_wallet.getAddress()],
        contract_addr
    )
    assert res["reverted"] == False
    assert res["decoded"]["0"] == 3 * (10 ** 18)  # 3 vet should be there
    print('call:vetBalance:gas:', res["gasUsed"])

    # Call to get the balance of user's vtho
    res = testnet_connector.call(
        testnet_wallet.getAddress(),
        vthobox_contract,
        "vthoBalance",
        [testnet_wallet.getAddress()],
        contract_addr
    )
    assert res["reverted"] == False
    assert res["decoded"]["0"] > 0 # Some vtho should be there
    print('call:vthoBalance:gas:', res["gasUsed"])

    # Add more VET (3) to the user
    res = testnet_connector.transact(
        testnet_wallet,
        vthobox_contract,
        "addVET",
        [testnet_wallet.getAddress(), 3 * (10 ** 18)],
        contract_addr
    )
    assert res["id"]

    tx_id = res["id"]
    receipt = testnet_connector.wait_for_tx_receipt(tx_id)
    print('transact:addVET:gas:', receipt["gasUsed"])

    time.sleep(12)

    # Call to get the balance of user's vet
    res = testnet_connector.call(
        testnet_wallet.getAddress(),
        vthobox_contract,
        "vetBalance",
        [testnet_wallet.getAddress()],
        contract_addr
    )
    assert res["reverted"] == False
    assert res["decoded"]["0"] == 6 * (10 ** 18)  # 6 vet should be there
    print('call:vetBalance:gas:', res["gasUsed"])

    # Call to get the balance of user's vtho
    res = testnet_connector.call(
        testnet_wallet.getAddress(),
        vthobox_contract,
        "vthoBalance",
        [testnet_wallet.getAddress()],
        contract_addr
    )
    assert res["reverted"] == False
    assert res["decoded"]["0"] > 0 # Some vtho should be there
    print('call:vthoBalance:gas:', res["gasUsed"])
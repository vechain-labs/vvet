import pytest
from thor_requests import connect
from .helpers import (
    helper_deploy,
    helper_call,
    helper_transact,
    helper_wait_for_block
)
from .fixtures import (
    solo_connector as connector,
    solo_wallet as wallet,
    clean_wallet,
    vvet_contract as contract
)


@pytest.fixture
def deployed(connector, wallet, contract):
    ''' Deploy a new smart contract, return the deployed contract address '''
    return helper_deploy(connector, wallet, contract)


# @pytest.mark.parametrize(
#     'amount, should_revert',
#     [
#         (3*10**18, False), # normal deposit: 3 vet
#         (15*10**18, False), # normal deposit: 15 vet
#         (2**105, True), # too big deposit: overflow amount
#     ]
# )
# def test_deposit_vet(deployed, connector, wallet, contract, amount, should_revert):
#     '''
#         User "deposit" vet to exchange for vvet,
#         then check "balanceOf" user's vvet.

#         Include reverted and non-reverted cases.
#     '''
#     # First, deposit
#     r, receipt = helper_transact(connector, wallet, deployed, contract, 'deposit', [], amount)
#     assert r == should_revert
#     # Next, check the balance
#     if not should_revert:
#         r, res = helper_call(connector, wallet.getAddress(), deployed, contract, 'balanceOf', [wallet.getAddress()])
#         assert r == False
#         assert int(res['decoded']['0']) == amount


# @pytest.mark.parametrize(
#     'inAmount, outAmount, should_revert',
#     [
#         (2*10**18, 1*10**18, False), # normal withdraw
#         (1*10**18, 2*10**18, True), # over withdraw
#         (1*10**18, 2**105, True), # over withdraw with overflow amount
#     ]
# )
# def test_withdraw_vet(deployed, connector, wallet, contract, inAmount, outAmount, should_revert):
#     ''' User withdraw vet with vvet '''
#     # First, deposit
#     r, receipt = helper_transact(connector, wallet, deployed, contract, 'deposit', [], inAmount)
#     assert r == False

#     # Wait for pack
#     helper_wait_for_block(connector)

#     # Next, withdraw
#     r, receipt = helper_transact(connector, wallet, deployed, contract, 'withdraw', [outAmount])
#     assert r == should_revert


# @pytest.mark.parametrize(
#     'inAmount, outAmount, should_revert',
#     [
#         (2*10**18, 1*10**18, False), # normal transfer (success)
#         (2*10**18, 2*10**18, False), # all transfer (success)
#         (1*10**18, 2*10**18, True), # over transfer (fail)
#         (1*10**18, 2**105, True), # over transfer with overflow amount (fail)
#     ]
# )
# def test_transfer_vvet(deployed, connector, wallet, clean_wallet ,contract, inAmount, outAmount, should_revert):
#     ''' User transfer his vvet to other person '''
#     # First, deposit
#     r, receipt = helper_transact(connector, wallet, deployed, contract, 'deposit', [], inAmount)
#     assert r == False

#     # Wait for pack
#     helper_wait_for_block(connector)

#     # Next, transfer to other person
#     r, receipt = helper_transact(connector, wallet, deployed, contract, 'transfer', [clean_wallet.getAddress(), outAmount])
#     assert r == should_revert

#     # Wait for pack
#     helper_wait_for_block(connector)

#     # Finally, check "balanceOf" of two people
#     if r == False:
#         _, res = helper_call(connector, wallet.getAddress(), deployed, contract, 'balanceOf', [wallet.getAddress()])
#         assert int(res['decoded']['0']) == inAmount - outAmount
#         _, res = helper_call(connector, wallet.getAddress(), deployed, contract, 'balanceOf', [clean_wallet.getAddress()])
#         assert int(res['decoded']['0']) == outAmount
#     else:
#         _, res = helper_call(connector, wallet.getAddress(), deployed, contract, 'balanceOf', [wallet.getAddress()])
#         assert int(res['decoded']['0']) == inAmount
#         _, res = helper_call(connector, wallet.getAddress(), deployed, contract, 'balanceOf', [clean_wallet.getAddress()])
#         assert int(res['decoded']['0']) == 0


# @pytest.mark.parametrize(
#     'inAmount, approveAmount, outAmount, a_should_revert, t_should_revert',
#     [
#         (2*10**18, 1*10**18, 1*10**18, False, False), # owner approve some
#         (2*10**18, 2*10**18, 2*10**18, False, False), # owner approve whole
#         (1*10**18, 2*10**18, 2*10**18, False, True), # owner over approve, but transfer shall fail
#         (1*10**18, 2**105, 2**105, False, True), # owner over approve with overflow, but transfer shall fail
#         (1*10**18, 2**105, 1*10**18, False, False), # owner over approve with overflow, and transfer shall success
#         (2*10**18, 2*10**18, 3*10**18, False, True), # user over transfer
#         (2*10**18, 2*10**18, 2**105, False, True), # user over transfer with overflow
#     ]
# )
# def test_approve(deployed, connector, wallet, clean_wallet, contract, inAmount, approveAmount, outAmount, a_should_revert, t_should_revert):
#     ''' Test approve of one's funds to be spent by other person '''
#     # Deposit
#     r, receipt = helper_transact(connector, wallet, deployed, contract, 'deposit', [], inAmount)
#     assert r == False
#     helper_wait_for_block(connector)

#     # "approve"
#     r, receipt = helper_transact(connector, wallet, deployed, contract, 'approve', [clean_wallet.getAddress(), approveAmount])
#     assert r == a_should_revert

#     if r == False:
#         # "allowance"
#         _, res = helper_call(connector, clean_wallet.getAddress(), deployed, contract, 'allowance', [wallet.getAddress(), clean_wallet.getAddress()])
#         assert int(res['decoded']['0']) == approveAmount
#         # "transferFrom"
#         r, receipt = helper_transact(connector, wallet, deployed, contract, 'transferFrom', [wallet.getAddress(), clean_wallet.getAddress(), outAmount])
#         assert r == t_should_revert

#         if r == False:
#             # Check balance of both wallets
#             _, res = helper_call(connector, clean_wallet.getAddress(), deployed, contract, 'balanceOf', [wallet.getAddress()])
#             assert int(res['decoded']['0']) == inAmount - outAmount
#             _, res = helper_call(connector, clean_wallet.getAddress(), deployed, contract, 'balanceOf', [clean_wallet.getAddress()])
#             assert int(res['decoded']['0']) == outAmount


@pytest.mark.parametrize(
    'vetAmount, wait_for_blocks, vthoOutAmount, should_revert',
    [
        (1*10**18, 1, 0, False),
        (1*10**18, 1, 0, False), # Over claim vtho
    ]
)
def test_staking_by_claim(deployed, connector, wallet, contract, vetAmount, wait_for_blocks, vthoOutAmount, should_revert):
    ''' Test generated vtho by claim '''
    # Deposit VET
    r, receipt = helper_transact(connector, wallet, deployed, contract, 'deposit', [], vetAmount)
    assert r == False
    assert type(receipt['meta']['blockTimestamp']) == int
    packed_timestamp = receipt['meta']['blockTimestamp']
    # Wait for some blocks
    helper_wait_for_block(connector, wait_for_blocks)
    # Check generated VTHO balance
    best_block = connector.get_block()
    current_timestamp = best_block['timestamp']
    r, res = helper_call(connector, wallet.getAddress(), deployed, contract, 'vthoBalance', [wallet.getAddress()])
    current_vtho = res['decoded']['0']
    assert current_vtho == (current_timestamp - packed_timestamp) * 5 / (10**9) * vetAmount
    # Claim vtho back to his own wallet
    # Wait for pack
    # Check vtho balance (immediatly)


def test_staking_by_transfer():
    ''' Test generated vtho by transfer vvet '''
    # Deposit VET
    # wait for 2 blocks
    # Check generated vtho balance
    # transfer vvet to other wallet
    # wait for 2 blocks
    # check vtho balance of 2 people


def test_staking_by_withdraw():
    ''' Test generated vtho by withdraw vvet to vet '''
    # Deposit VET
    # wait for 2 blocks
    # Check generated vtho balance
    # withdraw VET
    # wait for 2 blocks
    # check the vtho balance
    pass


def test_staking_by_approve():
    ''' Test generated vtho by approve other people some vvet '''
    # Desposit VET
    # wait for 2 blocks
    # Check generated vtho balance
    # approve other wallet some VET
    # check generated vtho balance
    # transferFrom vvet to other wallet
    # check vtho balance of two wallets
    # wait for 2 blocks
    # check vtho balance of two wallets
    pass
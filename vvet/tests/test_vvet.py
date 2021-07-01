import pytest
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


def _calculate_vtho(t_1, t_2, vetAmount):
    '''' 5x10^(-9) vtho per vet per second '''
    assert t_1 <= t_2
    return vetAmount * (t_2 - t_1) * 5 / (10**9)


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


def _stake_vet(amount_vet, deployed, connector, wallet, contract):
    ''' stake amount of vet into smart contract '''
    # Deposit VET
    r, receipt = helper_transact(connector, wallet, deployed, contract, 'deposit', [], amount_vet)
    assert r == False
    assert type(receipt['meta']['blockTimestamp']) == int
    packed_timestamp = receipt['meta']['blockTimestamp']

    # timestamp, amount_vet
    return packed_timestamp, amount_vet


def _view_vtho_balance(deployed, connector, wallet, contract):
    ''' view generated VTHO balance on the smart contract '''
    best_block = connector.get_block()
    current_timestamp = best_block['timestamp']
    r, res = helper_call(connector, wallet.getAddress(), deployed, contract, 'vthoBalance', [wallet.getAddress()])
    assert r == False
    current_vtho = res['decoded']['0']
    return current_timestamp, current_vtho


# @pytest.mark.parametrize(
#     'amount_vet, blocks_number',
#     [
#         (1*10**18, 1),
#         (2*10**18, 1)
#     ]
# )
# def test_staking(amount_vet, blocks_number, deployed, connector, wallet, contract):
#     ''' Stake vet then check the vtho generated '''
#     # Deposit
#     packed_timestamp, _ = _stake_vet(amount_vet, deployed, connector, wallet, contract)
    
#     # Wait
#     helper_wait_for_block(connector, blocks_number)
    
#     # Check balance
#     current_timestamp, current_vtho = _view_vtho_balance(deployed, connector, wallet, contract)

#     # Verify balance
#     assert current_vtho == _calculate_vtho(packed_timestamp, current_timestamp, amount_vet)

# @pytest.mark.parametrize(
#     'amount_vet, blocks_number, claim_amount, should_revert',
#     [
#         (1*10**18, 1, 5*10**9, False), # normal claim
#         (1*10**18, 1, 1*10**18, True), # over claim
#         (1*10**18, 1, 2**105, True), # over claim, with overflow
#         (1*10**18, 1, 0, False), # claim 0 vtho (success)
#     ]
# )
# def test_staking_by_claim(amount_vet, blocks_number, claim_amount, should_revert, deployed, connector, wallet, contract):
#     ''' Stake vet then claim vtho '''
#     # Deposit vet
#     packed_timestamp, _ = _stake_vet(amount_vet, deployed, connector, wallet, contract)
#     # Wait
#     helper_wait_for_block(connector, blocks_number)
#     # claim some vtho (but won't withdraw vet)
#     r, receipt = helper_transact(connector, wallet, deployed, contract, 'claimVTHO', [wallet.getAddress(), claim_amount])
#     assert r == should_revert
#     if r == False:
#         # Wait
#         helper_wait_for_block(connector, 1)
#         # Check vtho balance
#         current_timestamp, current_vtho = _view_vtho_balance(deployed, connector, wallet, contract)
#         assert _calculate_vtho(packed_timestamp, current_timestamp, amount_vet) - claim_amount == current_vtho

@pytest.mark.parametrize(
    'amount_vet, transfer_amount, t_should_revert',
    [
        (1*10**18, 5*10**17, False), # transfer half of vvet
    ]
)
def test_staking_by_transfer(amount_vet, transfer_amount, t_should_revert, deployed, connector, wallet, contract, clean_wallet):
    ''' Stake vet, transfer vvet '''
    # Deposit VET
    packed_timestamp, _ = _stake_vet(amount_vet, deployed, connector, wallet, contract)
    # wait for blocks
    helper_wait_for_block(connector)
    # transfer vvet to other wallet
    r, receipt = helper_transact(connector, wallet, deployed, contract, 'transfer', [clean_wallet.getAddress(), transfer_amount])
    assert r == t_should_revert
    changed_timestamp = receipt['meta']['blockTimestamp']
    # check vtho balance of 2 people
    if r == False:
        # wait for blocks
        helper_wait_for_block(connector)
        # Check vtho balance of the receiver
        t, v = _view_vtho_balance(deployed, connector, clean_wallet, contract)
        assert _calculate_vtho(changed_timestamp, t, transfer_amount) == v
        # Check vtho balance of the sender
        t, v = _view_vtho_balance(deployed, connector, wallet, contract)
        assert _calculate_vtho(packed_timestamp, changed_timestamp, amount_vet) + _calculate_vtho(changed_timestamp, t, transfer_amount) == v


def test_staking_by_withdraw():
    ''' Stake vet, withdraw vet '''
    # Deposit VET
    # wait for blocks
    # withdraw VET
    # wait for blocks
    # check the vtho balance
    pass


def test_staking_by_approve():
    ''' Stake vet, approve vvet, transferFrom vvet '''
    # Desposit VET
    # wait for blocks
    # approve other wallet some VET
    # transferFrom vvet to other wallet
    # check vtho balance of two wallets
    # wait for blocks
    # check vtho balance of two wallets
    pass

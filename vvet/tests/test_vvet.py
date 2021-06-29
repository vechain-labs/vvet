import pytest
from thor_requests import connect
from .helpers import (
    helper_deploy,
    helper_call,
    helper_transact,
    helper_wait_one_block
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


@pytest.mark.parametrize(
    'amount, should_revert',
    [
        (3*10**18, False), # normal deposit: 3 vet
        (15*10**18, False), # normal deposit: 15 vet
        (2**105, True), # too big deposit: overflow amount
    ]
)
def test_deposit_vet(deployed, connector, wallet, contract, amount, should_revert):
    '''
        User "deposit" vet to exchange for vvet,
        then check "balanceOf" user's vvet.

        Include reverted and non-reverted cases.
    '''

    r, receipt = helper_transact(connector, wallet, deployed, contract, 'deposit', [], amount)
    assert r == should_revert
    
    if not should_revert:
        r, res = helper_call(connector, wallet.getAddress(), deployed, contract, 'balanceOf', [wallet.getAddress()])
        assert r == False
        assert int(res['decoded']['0']) == amount


@pytest.mark.parametrize(
    'inAmount, outAmount, should_revert',
    [
        (2*10**18, 1*10**18, False), # normal withdraw
        (1*10**18, 2*10**18, True), # over withdraw
        (1*10**18, 2**105, True), # over withdraw with overflow amount
    ]
)
def test_withdraw_vet(deployed, connector, wallet, contract, inAmount, outAmount, should_revert):
    ''' User withdraw vet with vvet '''
    # First, deposit
    r, receipt = helper_transact(connector, wallet, deployed, contract, 'deposit', [], inAmount)
    assert r == False

    # Wait for pack
    helper_wait_one_block(connector)

    # Next, withdraw
    r, receipt = helper_transact(connector, wallet, deployed, contract, 'withdraw', [outAmount])
    assert r == should_revert


@pytest.mark.parametrize(
    'inAmount, outAmount, should_revert',
    [
        (2*10**18, 1*10**18, False), # normal transfer (success)
        (2*10**18, 2*10**18, False), # all transfer (success)
        (1*10**18, 2*10**18, True), # over transfer (fail)
        (1*10**18, 2**105, True), # over transfer with overflow amount (fail)
    ]
)
def test_transfer_vvet(deployed, connector, wallet, clean_wallet ,contract, inAmount, outAmount, should_revert):
    ''' User transfer his vvet to other person '''
    # First, deposit
    r, receipt = helper_transact(connector, wallet, deployed, contract, 'deposit', [], inAmount)
    assert r == False

    # Wait for pack
    helper_wait_one_block(connector)

    # Next, transfer to other person
    r, receipt = helper_transact(connector, wallet, deployed, contract, 'transfer', [clean_wallet.getAddress(), outAmount])
    assert r == should_revert

    # Wait for pack
    helper_wait_one_block(connector)

    # Finally, check "balanceOf" of two people
    if r == False:
        _, res = helper_call(connector, wallet.getAddress(), deployed, contract, 'balanceOf', [wallet.getAddress()])
        assert int(res['decoded']['0']) == inAmount - outAmount
        _, res = helper_call(connector, wallet.getAddress(), deployed, contract, 'balanceOf', [clean_wallet.getAddress()])
        assert int(res['decoded']['0']) == outAmount
    else:
        _, res = helper_call(connector, wallet.getAddress(), deployed, contract, 'balanceOf', [wallet.getAddress()])
        assert int(res['decoded']['0']) == inAmount
        _, res = helper_call(connector, wallet.getAddress(), deployed, contract, 'balanceOf', [clean_wallet.getAddress()])
        assert int(res['decoded']['0']) == 0


# def test_approve():
#     ''' Test approve of one's funds to be spend by other person '''
#     pass


# def test_claim_vtho():
#     ''' Normal claim of generated vtho '''
#     pass


# def test_claim_vtho_to_other_wallet():
#     ''' Claim vtho to another wallet than the caller itself '''
#     pass

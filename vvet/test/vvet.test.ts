import { expect, assert } from 'chai'
import path from 'path'
import BN from 'bn.js'

import { Framework } from '@vechain/connex-framework'
import { Driver, SimpleNet, SimpleWallet } from '@vechain/connex-driver'

import { soloAccounts } from 'myvetools/dist/builtin'
import { compileContract, randBytes } from 'myvetools/dist/utils'
import { Contract } from 'myvetools/dist/contract'
import { getReceipt } from 'myvetools/dist/connexUtils'

import { batchSend } from '../../utils'

describe('Test VVET9 contract', () => {
	const wallet = new SimpleWallet()
	// Add private keys
	soloAccounts.forEach(val => { wallet.import(val) })

	// Set to connect to a local Thor node
	const url = 'http://localhost:8669/'

	let driver: Driver
	let connex: Framework

	before(async () => {
		try {
			driver = await Driver.connect(new SimpleNet(url), wallet)
			connex = new Framework(driver)
		} catch (err) {
			assert.fail('Failed to connect: ' + err)
		}
	})

	after(() => {
		driver.close()
	})

	let vvet = new Contract({
		abi: JSON.parse(compileContract(
			path.resolve(process.cwd(), './vvet/contracts/VVET9.sol'),
			'VVET9', 'abi'
		)),
		bytecode: compileContract(
			path.resolve(process.cwd(), './vvet/contracts/VVET9.sol'),
			'VVET9', 'bytecode'
		)
	})

	let energy = new Contract({
		abi: JSON.parse(compileContract(
			path.resolve(process.cwd(), './vvet/contracts/IEnergy.sol'),
			'IEnergy', 'abi'
		)),
		address: '0x0000000000000000000000000000456E65726779'
	})
	

	it('deploy vvet contract', async () => {
		const txResp = await connex.vendor.sign('tx', [vvet.deploy(0)]).request()
		const receipt = await getReceipt(connex, 5, txResp.txid)
		expect(receipt.reverted).to.eql(false)

		vvet.connex(connex)
		if (receipt.outputs[0].contractAddress) {
			vvet.at(receipt.outputs[0].contractAddress)
		}
	})

	it('Check VTHO balance after depositing', async () => {
		// deposit = random number in [0, 1] * 1e8 * 1e18
		const value = new BN(Math.random() * 1000).mul(new BN('1' + '0'.repeat(8 + 18 - 3)))
		// const value = new BN('2' + '0'.repeat(18 + 4))
		const sender = wallet.list[1].address

		// Send 1e8 VET to vVET
		const clause = { to: vvet.address, value: '0x' + value.toString(16) }
		const txResp = await connex.vendor.sign('tx', [clause])
			.signer(sender)
			.request()
		const receipt = await getReceipt(connex, 5, txResp.txid)
		expect(receipt.reverted).to.eql(false)

		// console.log(`deposit: ${receipt.meta.blockTimestamp}`)

		const ticker = connex.thor.ticker()
		await ticker.next()
		await ticker.next()

		// Check whether the sender's vtho balance computed by the contract 
		// is equal to the vtho balance of the contract
		const bal = await vvet.getBalance()
		const callOut = await vvet.call('vthoBalanceOf', sender)
		expect(bal.energy.slice(2)).to.eql(new BN(callOut.data.slice(2, 66), 16).toString(16))
	})

	it('VTHO over withdraw', async () => {
		const from = wallet.list[1].address
		const to = randBytes(20)
		const callOut = await vvet.call('vthoBalanceOf', from)
		const amount = new BN(callOut.data.slice(2, 66), 16).mul(new BN(2))
		const dryRunOut = await connex.thor.explain(
			[vvet.send('vthoWithdraw', 0, to, '0x' + amount.toString(16))]
		).caller(from).execute()
		expect(dryRunOut[0].revertReason).to.eql('builtin: insufficient balance')
	})

	it('VTHO withdraw', async () => {
		const from = wallet.list[1].address
		const to = randBytes(20)
		let callOut = await vvet.call('vthoBalanceOf', from)
		const amount = 10
		const txResp = await connex.vendor.sign('tx',
			[vvet.send('vthoWithdraw', 0, to, amount)]
		).signer(from).request()
		const receipt = await getReceipt(connex, 5, txResp.txid)
		expect(receipt.reverted).to.eql(false)

		energy.connex(connex)
		callOut = await energy.call('balanceOf', to)
		expect(parseInt(callOut.data.slice(2, 66), 16)).to.eql(amount)
	})

	it('Check VTHO balance after transfering vVET', async () => {
		const from = wallet.list[1].address
		const to = wallet.list[2].address
		const ticker = connex.thor.ticker()

		let callOut = await vvet.call('balanceOf', from)
		const amount = new BN(callOut.data.slice(2, 66), 16).div(new BN(2))
		const txResp = await connex.vendor.sign(
			'tx', [vvet.send('transfer', 0, to, '0x' + amount.toString(16))]
		).signer(from).request()
		const receipt = await getReceipt(connex, 5, txResp.txid)
		expect(receipt.reverted).to.eql(false)

		// console.log(`transfer: ${receipt.meta.blockTimestamp}`)
		// callOut = await vvet.call('balanceOf', to)
		// console.log(`to: ${parseInt(callOut.data.slice(2, 66), 16)}`)

		await ticker.next()
		await ticker.next()

		let sum = new BN(0)
		for (let i = 1; i <= 2; i++) {
			let callOut = await vvet.call('vthoBalanceOf', wallet.list[i].address)
			// console.log(`vtho${i}: ${new BN(callOut.data.slice(2, 66), 16).toString(10)}`)
			sum = sum.add(new BN(callOut.data.slice(2, 66), 16))
		}
		const bal = await vvet.getBalance()
		// console.log(`vVET: ${new BN(bal.energy.slice(2), 16).toString(10)}`)
		expect(bal.energy.slice(2)).to.eql(sum.toString(16))
	})

	it('Check VTHO balance after withdrawing', async () => {
		const ticker = connex.thor.ticker()

		const clauses: Connex.VM.Clause[][] = []
		for (let i = 1; i <= 2; i++) {
			const callOut = await vvet.call('balanceOf', wallet.list[i].address)
			const value = new BN(callOut.data.slice(2, 66), 16)
			clauses.push([vvet.send('withdraw', 0, '0x' + value.toString(16))])
		}
		const receipts = await batchSend(
			connex, clauses,
			[wallet.list[1].address, wallet.list[2].address]
		)
		receipts.forEach(receipt => { expect(receipt.reverted).to.eql(false) })

		// console.log(`withdraw1: ${receipts[0].meta.blockTimestamp}`)
		// console.log(`withdraw2: ${receipts[0].meta.blockTimestamp}`)

		await ticker.next()
		await ticker.next()

		let sum = new BN(0)
		for (let i = 1; i <= 2; i++) {
			let callOut = await vvet.call('vthoBalanceOf', wallet.list[i].address)
			// console.log(`vtho${i}: ${new BN(callOut.data.slice(2, 66), 16).toString(10)}`)
			sum = sum.add(new BN(callOut.data.slice(2, 66), 16))
		}
		const bal = await vvet.getBalance()
		// console.log(`vVET: ${new BN(bal.energy.slice(2), 16).toString(10)}`)
		expect(bal.energy.slice(2)).to.eql(sum.toString(16))
	})
})
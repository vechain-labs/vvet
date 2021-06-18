import { getReceipt } from "myvetools/dist/connexUtils"

export async function batchSend(
	conn: Connex,
	txs: Connex.VM.Clause[][],
	signers: string[]
): Promise<Connex.Thor.Transaction.Receipt[]> {
	let resps: Connex.Vendor.TxResponse[] = []
	let receipts: Connex.Thor.Transaction.Receipt[] = []
	for (let i = 0; i < txs.length; i++) {
		resps.push(await conn.vendor.sign('tx', txs[i]).signer(signers[i]).request())
	}

	for (let r of resps) {
		receipts.push(await getReceipt(conn, 5, r.txid))
	}

	return receipts
}

export async function getErr(
	connex: Connex, clauses: Connex.VM.Clause[], caller: string
): Promise<string> {
	const dryRunOut = await connex.thor.explain(clauses).execute()
	for (let out of dryRunOut) {
		if (typeof out.revertReason === 'string') {
			return out.revertReason
		}
	}
	return "No error"
}
# UMAD-07: Post-transaction compliance hooks

UMA offers a mechanism by which VASPs can notify each other of the UTXOs used to complete a transaction. This is useful
for compliance purposes, as it allows VASPs to submit those UTXOs to their compilance providers for transaction
monitoring.

**Note:** VASPs only need to receive post-transaction hooks from their counterparty VASP for the UTXO-based compliance
flow, i.e. for cases where their Compliance Provider does not support lookups and registration via node public key. If
the compliance provider supports using the node public key instead, VASPs can omit the `utxoCallback` field. However,
VASPs do still need to send post-transaction hooks for their counter-party if the other VASP has provided a
`utxoCallback` themselves.

As mentioned in [UMAD-05](/umad-05-payreq-request.md), in the payreq request, the sending VASP specifies a
`payerdata.compliance.utxoCallback` field which is a URL that the receiving VASP should call on transaction completion
to notify the sending VASP of the UTXOs used to complete the transaction. Similarly, in the payreq response, the
receiving VASP specifies a `compliance.utxoCallback` field which is a URL that the sending VASP should call on
transaction completion to notify the receiving VASP of the UTXOs used to complete the transaction. This request from
each VASP to the other is called a "post-transaction hook". It is a POST request with the following structure:

```http
POST <utxoCallback>

{
  "utxos": { "utxo": string, "amountMsats": number }[],
  // Domain name of the VASP calling this endpoint. Used when validating the signature.
  "vaspDomain": string,
  // The VASP's signature over sha256_hash(signatureNonce + signatureTimestamp),
  "signature": string,
  "signatureNonce": string,
  "signatureTimestamp": number, // in seconds since epoch
}
```

The request body is JSON with a single field, `utxos`, which is an array of objects containing the UTXO and the
corresponding amount in millisats that went over each channel used to complete the transaction. Both VASPs can
register the incoming UTXOs with their Compliance Provider for transaction monitoring.

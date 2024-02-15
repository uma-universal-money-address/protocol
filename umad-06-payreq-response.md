# UMAD-06: Payreq Response

The response to the payreq request is an extension of LNURL's [LUD-06](https://github.com/lnurl/luds/blob/luds/06.md).
It contains the actual lightning invoice, as well as some additional fields for compliance and currency conversion.
The full structure of the LNURLP response is:

```raw
{
  // The encoded BOLT-11 invoice
  "pr": string,
  // Empty for legcy LNURL reasons.
  "routes": [],
  "compliance": {
    // Public key of the recipient node for pre-screening.
    "nodePubKey": string,
    // A list of the expected UTXOs over which the receiver may receive the transaction (receiver's channels).
    "utxos": string[],
    // A url which the sending VASP should call on transaction completion to notify the receiving VASP of
    // the utxos used to complete the transaction. See [UMAD-07](/umad-07-post-tx-hooks.md).
    "utxoCallback": string,
    // The receiving VASP's signature over sha256_hash(<sender UMA> (eg. $alice@vasp1.com) + signatureNonce + signatureTimestamp).
    "signature": string,
    "signatureNonce": string,
    "signatureTimestamp": number, // in seconds since epoch
  },
  "paymentInfo": {
    // The currency code of the receiving currency (eg. "USD"). This should match the requested currency in the payreq
    // request.
    "currencyCode": string,
    // Millisats per "unit" of the receiving currency (eg. 1 cent in USD). A double-precision floating point number.
    // In this context, this is just for convenience. The conversion rate is also baked into the invoice amount itself.
    // `invoice amount = amount * multiplier + exchangeFeesMillisatoshi`
    "multiplier": number,
    // Number of digits after the decimal point for the receiving currency. For example, in USD, by convention, there are
    // 2 digits for cents - $5.95. In this case, `decimals` would be 2. This should align with the currency's `decimals`
    // field in the LNURLP response. It is included here for convenience. See [UMAD-04](/uma-04-local-currency.md) for
    // details, edge cases, and examples.
    "decimals": number,
    // The fees charged (in millisats) by the receiving VASP to convert to the target currency.
    // This is separate from the multiplier rate.
    "exchangeFeesMillisatoshi": number
  },
  "umaVersion": "1.0",
}
```

**NOTE:** The conversion rate is implicitly valid as long as the lightning invoice. VASPs can set a short invoice
expiry to avoid large swings in conversion rate between invoice generation and payment. The invoice expiry is used as
a hard cap on the conversion rate validity.

As described in [UMAD-05](/umad-05-payreq-request.md), the `nodePubKey` and `utxos` fields are used for pre-screening
by the sending VASP. The `utxoCallback` field is used by the receiving VASP to notify the sending VASP of the utxos
used to complete the transaction. See [UMAD-07](/umad-07-post-tx-hooks.md) for details.

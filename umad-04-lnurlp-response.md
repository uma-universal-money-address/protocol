# UMAD-04: LNURLP Response

The response to the LNURLP request is an extension of LNURL's [LUD-06](https://github.com/lnurl/luds/blob/luds/06.md).
It also utilizes the payer data spec as described in [LUD-18](https://github.com/lnurl/luds/blob/luds/18.md) and a
slightly modified version of the local currency spec proposed in [LUD-21](https://github.com/lnurl/luds/pull/251).
The full structure of the LNURLP response is:

```raw
{
  "callback": string,
  // Max millisatoshi amount the receiver is willing to receive.
  "maxSendable": number,
  // Min millisatoshi amount the receiver is willing to receive, can not be less than 1 or more than `maxSendable`
  "minSendable": number,
  // See LUD-16 for details.
  "metadata": string,
  // Prefered receiving currencies of the receiver in order of preference.
  "currencies": [
    {
      "code": string, // eg. "PHP",
      "name": string, // eg. "Philippine Pesos",
      "symbol": string, // eg. "₱",
      // Estimated millisats per "unit" (eg. 1 cent in USD). A double-precision floating point number.
      "multiplier": number,
      // Number of digits after the decimal point for display on the sender side, and to add clarity around what the
      // "smallest unit" of the currency is. For example, in USD, by convention, there are 2 digits for cents - $5.95.
      // In this case, `decimals` would be 2. Note that the multiplier is still always in the smallest unit (cents).
      // In addition to display purposes, this field can be used to resolve ambiguity in what the multiplier
      // means. For example, if the currency is "BTC" and the multiplier is 1000, really we're exchanging in SATs, so
      // `decimals` would be 8.
      "decimals": number,
      // The inclusion of a convertible field implies the receiving VASP can quote and guarantee a price for a given
      // currency.
      "convertible": {
        // Minimum and maximium amounts the receiver is willing/able to convert to this currency in the smallest unit of
        // the currency. For example, if the currency is USD, the smallest unit is cents.
        "min": number, // 64-bit integer (long/int64)
        "max": number, // 64-bit integer (long/int64)
      }
    },
  ],
  // Required data about the payer. See LUD-18 for details.
  "payerData": {
    "identifier": { "mandatory": true },
    "name": { "mandatory": boolean },
    "email": { "mandatory": boolean },
    // Indicates we want TR data and/or utxos. This is UMA-specific and not in LUD-18. 
    "compliance": { "mandatory": boolean },
  },
  // UMA-specific authentication and compliance info.
  "compliance" {
    "isSubjectToTravelRule": boolean, // true if VASP2 needs travel rule info
    "kycStatus": KycStatus, // [enum] KYC state indicating whether the receiver is a KYC'd customer of VASP2.
    "signature": string, // hex encoded
    "signatureNonce": string,
    "signatureTimestamp": number // secs since epoch
    "receiverIdentifier": string // The identity of the receiver at VASP2
  },
  "umaVersion": "1.0", // The UMA protocol version that will be used for this transaction.
  "tag": "payRequest",
}
```

The signature here is over `sha256_hash(<receiver UMA> (eg. "$bob@vasp2.com") + nonce + timestamp)`.
The receiving VASPs `signingPubKey` can be used by the sending VASP to verify the signature as described in [UMAD-02](/umad-02-keys-and-authentication.md).

## Currency examples

Here are some additional examples of the `currencies` field to illustrate how the `multiplier` and `decimals` fields work.

```json
{
  "code": "USD",
  "name": "US Dollars",
  "symbol": "$",
  "multiplier": 23400,
  "decimals": 2,
  "convertible": {
    "min": 1,
    "max": 1000000
  },
}
```

In this case, the `decimals` field is 2, indicating that the smallest unit of the currency is cents (one hundredth of a dollar).
The `multiplier` field is 23400, indicating that there are 23,400 millisats per USD cent. This struct also indicates that
the receiving user can receive between 1 cent and $10,000 USD. If a sender wanted to send $5.95 USD, they would specify
`amount: 595, currency: USD` in their [payreq request](/umad-05-payreq-request.md), which should in turn create a Lightning
invoice for 13,923,000 millisats (595 * 23,400) plus applicable conversion fees.

```json
{
  "code": "BTC",
  "name": "Bitcoin",
  "symbol": "₿",
  "multiplier": 1000,
  "decimals": 8,
  "convertible": {
    "min": 1,
    "max": 100000000
  },
},
```

In this case, the `decimals` field is 8, indicating that the smallest unit of the currency is SATs (one hundred millionth
of a BTC). The `multiplier` field is 1,000, indicating that there are 1,000 millisats per SAT. This struct also indicates
that the receiving user can receive between 1 SAT and 1 BTC. If a sender wanted to send 0.0000001 BTC (10 sats), they would
specify `amount: 10, currency: BTC` in their [payreq request](/umad-05-payreq-request.md), which should in turn create a
Lightning invoice for 10,000 millisats (10 * 1,000) plus applicable conversion fees.

```json
{
  "code": "USDC",
  "name": "USDC",
  "symbol": "USDC",
  "multiplier": 2.34,
  "decimals": 6,
  "convertible": {
    "min": 1000000, // 1M
    "max": 1000000000000 // 1T
  },
}
```

In this case, the `decimals` field is 6, indicating that the smallest unit of the currency is one USDC / 10^6.
The `multiplier` field is 2.466, indicating that there are 2.466 millisats per USDC/10^6. This struct also indicates that
the receiving user can receive between 1 USDCent and 10,000 USDC. If a sender wanted to send 5.95 USDC, they would
specify `amount: 5950000, currency: USDC` in their [payreq request](/umad-05-payreq-request.md), which should in turn create
a Lightning invoice for 14,677,700 millisats (5,950,000 * 2.466) plus applicable conversion fees.

## Note for very small currency units

If the smallest unit of a currency is very small (eg. `multiplier` is .0001), it may be necessary to round up to a larger
unit when actually sending the payment so that the `amount` field in the [payreq request](/umad-05-payreq-request.md)
can fit in an int64 and can be represented in millisats. For example, DAI has 18 decimals, so the smallest unit is 10^-18.
In this case, trying to send 20 DAI would result in an `amount` of 20 * 10^18, which is too large to fit in an int64. For
this reason, the maximum `decimals` allowed is 8. If a currency has more than 8 decimals, the `multiplier` should be
increased to reduce the number of decimals. For example, if a currency has 10 decimals, the `multiplier` should be
`100 * the number of millisats per the real smallest unit`, and you should set `decimals` to 8. Tweaking the `multiplier`
and `decimals` fields in this way should allow the smallest unit to be represented in millisats and fit in an int64,
although it may result in some loss of precision.

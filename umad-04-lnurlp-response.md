# UMAD-04: LNURLP Response

The response to the LNURLP request is an extension of LNURL's [LUD-06](https://github.com/lnurl/luds/blob/luds/06.md).
It also utilizes the payer data spec as described in [LUD-18](https://github.com/lnurl/luds/blob/luds/18.md) and a
slightly modified version of the local currency spec proposed in [LUD-21](https://github.com/lnurl/luds/pull/207).
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
      "minSendable": number,
      "maxSendable": number,
      // Estimated millisats per "unit" (eg. 1 cent in USD)
      "multiplier": number,
      // Number of digits after the decimal point for display on the sender side. For example,
      // in USD, by convention, there are 2 digits for cents - $5.95. in this case, `displayDecimals`
      // would be 2. Note that the multiplier is still always in the smallest unit (cents). This field
      // is only for display purposes.
      "displayDecimals": number,
    },
    {
      "code": string, // eg. "BTC",
      "name": string, // eg. "Bitcoin",
      "symbol": string, // eg. "₿",
      "minSendable": number,
      "maxSendable": number,
      "multiplier": 1 // estimated millisats per "unit" (eg. 1 cent in USD)
      "displayDecimals": number,
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

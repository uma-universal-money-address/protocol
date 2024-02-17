# UMAD-05: Payreq Request

The first request in the UMA protocol is the payreq request, which aligns with the same request in LNURL-PAY
([LUD-06](https://github.com/lnurl/luds/blob/luds/06.md)), but with a few added query parameters for compliance,
currency conversion, and authentication. This request tells the receiving VASP to generate an invoice for a specified
amount on behalf of the receiving user.

**NOTE:** This needs to be a POST request instead of a GET (like in LNURL) because with travel rule info, the
payerData field might be too long to fit in a URL.

```http
POST vasp2.com/<callback>
```

`<callback>` is the URL returned in the `callback` field of the LNURLP response.

The body of the request is a JSON object with the following fields:

```raw
{
  "payerData": {
    // See LUD-18 for details.
    <json payerdata>
  },
  // An amount (int64) followed optionally by a "." and the sending currency code. For example: "100.USD" would send
  // an amount equivalent to $1 USD. Note that the amount is specified in the smallest unit of the specified
  // currency (eg. cents for USD). Omitting the currency code will default to specifying the amount in millisats.
  "amount": string,
  // The currency code of the receiving currency (eg. "USD") to which the receiving VASP will convert into when the
  // transaction completes. This must be one of the currencies returned in the LNURLP response, and it must have
  // been a currency with a "convertible" field.
  "convert": string,
  // The UMA protocol version that will be used for this transaction. See [UMAD-08](/umad-08-versioning.md).
  "umaVersion": "1.0",
  "payeeData":  {
    "compliance": { "mandatory": boolean },
    "name": { "mandatory": boolean },
    "identifier": { "mandatory": boolean },
    "countryCode": { "mandatory": boolean },
    ... All fields optional and more fields may be negotiated. See [LUD-22](https://github.com/lnurl/luds/pull/252)
  },
}
```

## Currency field examples

The currency spec here is as specified by [LUD-21](https://github.com/lnurl/luds/pull/251), with the caveat that UMA's
payreq request uses a POST and JSON body instead of a GET request with query parameters. Please see the spec for more
examples. As it pertains to UMA, there are two main UX cases to accommodate:

1. **The sender wants to send exactly a certain amount in the receiving currency.**

  For example, if a user in the US is paying for some goods or services in Europe, they might need to send *exactly* some
  amount in euros. In this case, the sender would enter the amount in the receiving currency. Fields specified by the
  sending VASP in the payreq request would look like:

  ```json
  {
    "amount": "100.EUR",
    "convert": "EUR",
    // ... other fields
  }
  ```

  This informs the receiving VASP to construct a Lightning invoice which will be converted to 100 euros for their user. This
  should include the conversion rate and any fees in the invoice itself to ensure that the receiver gets exactly 100 euros.

1. **The sender wants to send exactly a certain amount in their own currency.**

  For example, the sending user has $100 USD and they want to send exactly that amount to their family in Mexico. They would
  enter the amount in their own currency. However, their own sending VASP is responsible for the onramp from their sending
  currency to bitcoin. The sending VASP can guarantee that conversion rate to their user out-of-band of the UMA protocol.
  For example, maybe they've agreed that for $100, they will give the user exactly 191,000 satoshis. Fields specified by
  the sending VASP in the payreq request would then look like:

  ```json
  {
    "amount": "191000000", // 191,000,000 millisats, so the currency code is omitted.
    "convert": "MXN",
    // ... other fields
  }
  ```

  This informs the receiving VASP to construct a Lightning invoice for exactly 191,000 satoshis and to give their receiving
  user the equivalent in Mexican pesos according to their agreed-upon conversion rate. This allows the sender to lock in
  the amount they want to send in their own currency.

## Payee Data

The `payeeData` field is optional and is used to request additional information about the receiving user. The `mandatory`
field in each subfield indicates whether the receiving VASP is required to provide that information to proceed with the transaction.
See [LUD-22](https://github.com/lnurl/luds/pull/252) for more details. Note that the receiving VASP may choose to avoid sending
any payee identity information for privacy reasons, which may cause the payment to fail if the sending VASP requires it.
For that reason, the sender SHOULD NOT require any payee identity information to be sent by the receiver unless it is
absolutely necessary.

### Common Payee Data Fields

The following is a non-exhaustive list of common payee data fields that *may* be requested by the sender:

- `name`: The full name of the receiving user.
- `identifier`: The canonical receiving UMA address of the receiver.
- `countryCode`: The ISO 3166-1 alpha-2 country code of the receiving user.
- `email`: The email address of the receiving user.
- `accountNumber`: The account number of the receiving user at the receiving VASP.

Note that this struct is extensible, so any field can be added as long as it is agreed upon by both VASPs.

## Payer Data

The `payerData` field is a JSON object that contains information about the payer as described in
[LUD-18](https://github.com/lnurl/luds/blob/luds/18.md). There's also an UMA-specific payerdata field - `compliance`.
Its structure is:

```raw
{
  "compliance": {
    // The public key of the node that sender will use to send the payment. This can be used in place of utxos
    // if your compliance provider supports it.
    "nodePubKey": string|undefined,
    // A list of the expected UTXOs over which sender side may send transaction (sender's channels).
    // This is only needed if your compliance provider does not support checks via node public key.
    "utxos": string[]
    // The travel rule info for the transaction encrypted with the receiving VASP's encryptionPublicKey.
    "encryptedTravelRuleInfo": string|undefined,
    // The message format or protocol for the encryptedTravelRuleInfo. It is an optional string of the format
    // <protocol>@version (e.g. IVMS@101.2023). If this field is empty, assume raw freeform JSON.
    "travelRuleFormat": string|undefined,
    // An enum indicating whether the payer is a KYC'd customer of the sendingVASP.
    "kycStatus": KycStatus (enum),
    // The sending VASP's signature over sha256_hash(<sender UMA> (eg. $alice@vasp1.com) + signatureNonce + signatureTimestamp),
    "signature": string,
    "signatureNonce": string,
    "signatureTimestamp": number,
    // A url which the receiving VASP should call on transaction completion to notify the sending VASP of
    // the utxos used to complete the transaction. See [UMAD-07](/umad-07-post-tx-hooks.md).
    "utxoCallback": string|undefined,
  }
}
```

The `nodePubKey` and `utxos` fields can be used by the receiving VASP to pre-screen the transaction with a compliance
provider. The information included in the `encryptedTravelRuleInfo` field is dependent on regulations enforced on the
Sending VASP. It can be in any format, but if the `travelRuleFormat` field is included, the receiving VASP can use it
to parse the `encryptedTravelRuleInfo` field. For example, [IVMS](https://www.intervasp.org/#IVMS-1012023) is a
standardized format for Travel Rule information, which is supported by many VASPs.

# UMAD-09 Invoice

An UMA invoice is a data structure that describes payments that can be coordinated using UMA and
provides a way for a payment sender to have proof of payment–without having to use the existing
LNURLPRequest/Response handshake flow.

UMA invoices allow a payment recipient to specify an amount they want to receive in any currency,
along with some details on how to pay. This is useful in many cases where the recipient is the
initiator of a payment. For example, merchant checkout flows, a bill from any vendor or service
provider, etc.

## Invoice Format

The full structure of the invoice is:

```raw
{
    // Receiving UMA address
    ReceiverUma: string, 

    // Invoice UUID Served as both the identifier of the UMA invoice, and the validation of proof of payment.
    InvoiceUUID: string,

    // The amount of invoice to be paid in the smalest unit of the ReceivingCurrency.
    Amount: number,

    // The currency of the invoice
    ReceivingCurrency: {
        // Code is the ISO 4217 (if applicable) currency code (eg. "USD"). For cryptocurrencies, 
        // this will be a ticker symbol, such as BTC for Bitcoin.
        Code: string, 

        // Name is the full display name of the currency (eg. US Dollars).
        Name: string, 

        // Symbol is the symbol of the currency (eg. $ for USD).
        Symbol: string,

        // Decimals is the number of digits after the decimal point for display on the sender side
        Decimals: number,
    },

    // The unix timestamp the UMA invoice expires
    Expiration: number,

    // Indicates whether the VASP is a financial institution that requires travel rule information.
    IsSubjectToTravelRule: boolean,

    // Required data about the payer. See LUD-18 for details.
    RequiredPayerData: {
        "identifier": { "mandatory": true },
        "name": { "mandatory": boolean },
        "email": { "mandatory": boolean },
        // Indicates we want TR data and/or utxos. This is UMA-specific and not in LUD-18. 
        "compliance": { "mandatory": boolean },
    }

    // The versions of the UMA protocol supported by the VASP. It should include the highest minor
    // version for all major versions supported by the VASP, separated by commas.
    UmaVersions: string,

    // Optional field. CommentCharsAllowed is the number of characters that the sender can include 
    // in the comment field of the pay request.
    CommentCharsAllowed: number,

    // Optional field. The sender's UMA address. If this field presents, the UMA invoice should 
    // directly go to the sending VASP instead of showing in other formats.
    SenderUma: string,

    // Optional field. The maximum number of the invoice can be paid. If this field doesn't present,
    // there's no limit for the invoice.
    MaxNumPayments: number,

    // Optional field. [enum] KYC state indicating whether the receiver is a KYC'd customer of VASP2.
    KycStatus: KycStatus, 

    // The callback url that the sender should send the PayRequest to.
    Callback: string

    // The signature of the UMA invoice
    Signature: bytes
}

```

## Proof of Payment

When creating the lightning invoice from the UMA invoice, the invoice UUID should be included in the
metadata field. It should be one extra item for the metadata field. See the LUD-06 for details.

```text
["text/uma-invoice", invoiceUUID]
```

Once this is included in the metadata field for the lightning invoice, the UMA invoice can be tied
to the lightning invoice. Then the proof of payment for the lightning invoice can be used as the
proof of payment for the UMA invoice.

## Encoding

Bech32 encoding is used for the invoice without the 90 character limit.

### Human Readable Part

The human-readable part of the Bech32 encoding is `uma`.

### Data Part

The data part of the Bech32 encoding is the invoice encoded in TLV format. The TLV format is as
follows:

```raw
1 byte: Type + 1 byte: Length + Length bytes: Value
```

TLV fields are encoded in the following order:

- 0: ReceiverUma
- 1: InvoiceUUID
- 2: Amount
- 3: ReceivingCurrency, the receiving currency itself is encoded in TLV format
- 4: Expiration
- 5: IsSubjectToTravelRule
- 6: RequiredPayerData, the required payer data itself is encoded to field:boolean pairs separated
by a comma
- 7: UmaVersions
- 8: CommentCharsAllowed
- 9: SenderUma
- 10: MaxNumPayments
- 11: KycStatus
- 12: Callback
- 100: Signature

### Signature Calculation

The message for creating the signature is SHA256 of the TLV values without the signature field. Then
the signature is appended to the TLV encoded invoice.

## Reader requirements

- The invoice reader must validate that all non-optional fields are present.
- The invoice reader must validate that the invoice has not expired.
- The invoice reader must validate that the signature is valid using the receiver's public key.

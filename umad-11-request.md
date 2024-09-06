# UMAD-11 Request

UMA requests are a way to deliver UMA invoices to sending wallets through methods like
deep/universal links on mobile, notifications, etc.

## Request for non-specified sender

To deliver a UMA invoice to a sending wallet, the receiver can create a UMA invoice, and then
deliver the encoded UMA invoice string to the sending wallet.

The invoice string should be delivered using the following URL pattern:

```raw
uma://<invoice_string>
```

This can be displayed as a QR code, or a deep link on mobile. The sending wallet should register
the `uma` scheme to handle the UMA invoice string.

## Request for specified sender

To deliver an UMA invoice with a specified sender, the receiver can create a UMA invoice, and then
directly send the UMA invoice to the sending VASP.

The request URL should be defined in the uma-configuration scheme (See UMAD-10 for details) as:

```raw
"uma_request_endpoint": "https://vasp1.com/path/to/request/url"
```

The sending VASP should implement the request endpoint as a POST endpoint that accepts the UMA
invoice. The payload should be a JSON object with the following fields:

```raw
{
  "invoice": "<UMA invoice string>"
}
```

Once sending VASP receives the UMA invoice, it should notify the sending user to confirm the
payment.

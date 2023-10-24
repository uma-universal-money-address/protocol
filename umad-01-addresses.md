# UMAD-01: UMA Addresses

The UMA address format is based on Lightning Addresses ([LUD-16](https://github.com/lnurl/luds/blob/luds/16.md)), and
are themselves valid LNURL Lightning Addresses when the $ is stripped. They are in the format _$\<username>@\<domainname>_
(eg. _$alice@somevasp.com_). Similar to Lightning Addresses ([LUD-16](https://github.com/lnurl/luds/blob/luds/16.md)),
the domain will be used to make the first lnurlp call to somevasp.com.

![UMA Address Diagram](/images/address_diagram.png)

## Requirements

- Must start with a $ symbol. This is to differentiate from email addresses and clearly identify an uma address.
- The \<username> portion is limited to `a-z0-9-_.+`
- Addresses are case-insensitive, but by convention are written only with lowercase letters
- Like email addresses, the maximum number of characters for the \<username> portion of the address is 64 characters
(including the $).

The UMA SDKs validate these requirements and will throw an error if they are not met.

## Lightning Address Inter-op

UMA addresses are valid Lightning Addresses when the leading $ is stripped. Receiving VASPs who choose to support
plain LNURL-PAY transactions (which is a subset of UMA) should treat an incoming LNURLP request to a receiver
without a leading $ as a request to pay the receiver directly via LNURL-PAY. This way, users can still have a
single user name compatible with both UMA and LNURL, while keeping a clear distinction between the two for cases
where a VASP has to understand regulatory requirements.

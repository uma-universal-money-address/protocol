# UMA Addresses

The UMA address format is based on Lightning Addresses ([LUD-16](https://github.com/lnurl/luds/blob/luds/16.md)), and are themselves valid LNURL Lightning Addresses. They are in the format _$\<username>@\<domainname>_ (eg. _$alice@somevasp.com_). Similar to Lightning Addresses ([LUD-16](https://github.com/lnurl/luds/blob/luds/16.md)), the domain will be used to make the first lnurlp call to somevasp.com.

![UMA Address Diagram](/images/address_diagram.png)

## Requirements

- Must start with a $ symbol. This is to differentiate from email addresses and clearly identify an uma address.
- The \<username> portion is limited to `a-z0-9-_.+`
- Addresses are case-insensitive, but by convention are written only with lowercase letters
- Like email addresses, the maximum number of characters for the \<username> portion of the address is 64 characters (including the $).

The UMA SDKs validate these requirements and will throw an error if they are not met.

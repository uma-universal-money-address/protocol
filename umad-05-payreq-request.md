# UMAD-05: Payreq Request

The first request in the UMA protocol is the payreq request, which aligns with the same request in LNURL-PAY
([LUD-06](https://github.com/lnurl/luds/blob/luds/06.md)), but with a few added query parameters for compliance,
currency conversion, and authentication. This request tells the receiving VASP to generate an invoice for a specified
amount on behalf of the receiving user.

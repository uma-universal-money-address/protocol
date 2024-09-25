# UMAD-10: Configuration Document

UMA VASPs may provide a JSON configuration document similar to the
[OIDC Discovery Document](https://openid.net/specs/openid-connect-discovery-1_0.html) to allow client applications and
VASP counterparties to discover information about the VASP's UMA implementation.

This document should be made available
at `/.well-known/uma-configuration` on the VASP's domain. For example, for a VASP which provides UMA addresses at
`<username>@coolvasp.net`, the configuration document would be available at
`https://coolvasp.net/.well-known/uma-configuration`.

The configuration document should be served with the `application/json` content type, should be publicly accessible, and
should set [CORS headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) such that it is accessible from any
web origin, ie. `Access-Control-Allow-Origin: *`.

If present, the configuration document MUST contain the following fields:

- `name`: The human-readable name of the VASP.
- `uma_major_versions`: The major versions of the UMA protocol that the VASP supports. This should be an array of integers.

The configuration document MAY contain the following fields:

- `uma_request_endpoint`: The URL to which UMA requests can be sent. This should be a URL that the receiving VASP can use
  to send UMA requests to the sending VASP. See [UMAD-11](/umad-11-request.md) for more details.

These fields are required if implementing [UMA Auth (UMADE-01)](/extensions/umade-01-auth.md), but should not be provided
otherwise:

- `authorization_endpoint`: Like in OAuth/OIDC, the URL of the VASP's authorization endpoint. This is where the client
  application should send the user to authenticate and authorize the client application to access their wallet.
- `token_endpoint`: Like in OAuth/OIDC, the URL of the VASP's token endpoint. This is where the client application
  exchanges an authorization code for an access token (a new NWC Connection), and where the client application can
  refresh an access token.
- `nwc_commands_supported`: An array of strings representing the NWC commands that the VASP supports. This should be an
  array of strings, where each string is a valid NWC command name. See [UMADE-01](/extensions/umade-01-auth.md) for more
  details.
- `grant_types_supported`: An array of strings representing the OAuth grant types that the VASP supports. For now, in
  most cases, this should just be `["authorization_code"]`.
- `code_challenge_methods_supported`: An array of strings representing the PKCE code challenge methods that the VASP
  supports. For now, in most cases, this should just be `["S256"]`.
- `connection_management_endpoint`: The URL of the VASP's connection management endpoint. This is where the user can
  can create, update, and delete NWC Connections.
- `revocation_endpoint`: The URL of the VASP's revocation endpoint. This is where the client application can revoke an
  access token (NWC Connection).

## Example Configuration Document

```http
GET https://coolvasp.net/.well-known/uma-configuration

HTTP/1.1 200 OK
Content-Type: application/json
Access-Control-Allow-Origin: *

{
  "name": "Cool VASP",
  "uma_major_versions": [0, 1],
  "uma_request_endpoint": "https://coolvasp.net/path/to/request/url",

  "authorization_endpoint": "https://coolvasp.net/oauth/auth",
  "token_endpoint": "https://coolvasp.net/oauth/token",
  "nwc_commands_supported": [
    "pay_invoice",
    "make_invoice",
    "lookup_invoice",
    "get_balance",
    "get_budget",
    "get_info",
    "list_transactions",
    "pay_keysend",
    "lookup_user",
    "fetch_quote",
    "execute_quote",
    "pay_to_address",
  ],
  "grant_types_supported": ["authorization_code"],
  "code_challenge_methods_supported": ["S256"],
  "connection_management_endpoint": "https://coolvasp.net/nwc/connections",
  "revocation_endpoint": "https://coolvasp.net/oauth/revoke"
}
```

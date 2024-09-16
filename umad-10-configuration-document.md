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

## Example Configuration Document

```http
GET https://coolvasp.net/.well-known/uma-configuration

HTTP/1.1 200 OK
Content-Type: application/json
Access-Control-Allow-Origin: *

{
  "name": "Cool VASP",
  "uma_major_versions": [0, 1],
  "uma_request_endpoint": "https://coolvasp.net/path/to/request/url"
}
```

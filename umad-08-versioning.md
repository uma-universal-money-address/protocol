# UMAD-08 Versioning

UMA is a protocol that is designed to evolve over time. This document describes how version negotiation works in UMA.

The UMA protocol provides a method for version negotiation as part of the initial `LNURLP` Request. UMA versions
include major and minor components in the format `<major>.<minor>` (eg. `1.2`). Minor version bumps are
non-breaking, but may contain minor new **optional** features. Major version bumps include breaking changes. If a VASP
only supports versions `1.X`, they may not be able to talk to a VASP on version `2.X`. The version negotiation flow is
as follows:

![UMA Version Negotiation](/images/uma_version_negotiation.png)

1. The sender makes an initial `LnurlpRequest` to the receiver with the `umaVersion` query parameter set to the
   highest version it supports.
2. The receiver checks its compatibility and responds as such:
    - If the receiver supports that version, it will respond with a `LnurlpResponse` with the `umaVersion` field set
       to the same version.
    - If the receiver does not support that version, but supports the specified major version and a
       lower minor or patch version, it will respond with a `LnurlpResponse` with the `umaVersion` field set to the
       highest version it supports.
    - If the receiver does not support the major version specified, it will respond with a 412 HTTP status code and
       a body containing a list of its supported major versions.
3. If the sender gets a 200 response, it will proceed with the rest of the protocol as normal. However, if it gets a
   412 response, it will check if the receiver supports any of the major versions it supports. If so, it will re-issue
   the `LnurlpRequest` with the `umaVersion` query parameter set to the highest version both VASP's support. If it
   does not support any of the major versions the receiver supports, it will return an error to the user and abort the
   transaction.

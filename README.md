# UMA Protocol Spec

This is the source of truth protocol definition for UMA. All proposed spec changes should be sent as PRs to this repo.
Note that UMA is an extension of LNURL. If your proposal is also applicable to LNURL, the preference should be to
[propose a new LUD](https://github.com/lnurl/luds).

This repo is organized as a set of individual documents describing a single message or component of the protocol.

| Link                                           | Title                                |
| ---------------------------------------------- | ------------------------------------ |
| [UMAD-01](/umad-01-addresses.md)               | Address Format                       |
| [UMAD-02](/umad-02-keys-and-authentication.md) | Keys, Authentication, and Encryption |
| [UMAD-03](/umad-03-lnurlp-request.md)          | Initial LNURLP Request               |
| [UMAD-04](/umad-04-lnurlp-response.md)         | LNURLP Response                      |
| [UMAD-05](/umad-05-payreq-request.md)          | Payreq Request                       |
| [UMAD-06](/umad-06-payreq-response.md)         | Payreq Response                      |
| [UMAD-07](/umad-07-post-tx-hooks.md)           | Post Transaction Compliance Hooks    |
| [UMAD-08](/umad-08-versioning.md)              | Versioning                           |
| [UMAD-09](/umad-09-invoice.md)                 | Invoice                              |
| [UMAD-11](/umad-11-request.md)                 | Request                              |

## Extensions

UMA has a number of extensions that can be implemented by VASPs to provide additional functionality. These extensions are
not part of the core UMA payment protocol, but are defined here for reference.

| Link                                           | Title                                |
| ---------------------------------------------- | ------------------------------------ |
| [UMADE-01](/extensions/umade-01-auth.md)                  | UMA Auth                             |

## Additional Resources

- [Full Documentation and Guides](https://docs.uma.me)
- **UMA SDKs:**
  - [Golang](https://github.com/uma-universal-money-address/uma-go-sdk)
  - [Python](https://github.com/uma-universal-money-address/uma-python-sdk)
  - [Rust](https://github.com/uma-universal-money-address/uma-rust-sdk)
  - [Typescript](https://github.com/uma-universal-money-address/uma-js-sdk)
  - [Kotlin/Java](https://github.com/uma-universal-money-address/uma-kotlin-sdk)
  - [Shared Crypto Lib](https://github.com/uma-universal-money-address/uma-crypto-uniffi)
- **Example VASP Implementations or Tests:**
  - [Golang VASP using Gin](https://github.com/lightsparkdev/go-sdk/tree/main/examples/uma-server)
  - [Rust VASP using activex_web](https://github.com/lightsparkdev/lightspark-rs/blob/main/examples/uma-demo/src/main.rs)
  - [Kotlin VASP using ktor](https://github.com/lightsparkdev/kotlin-sdk/tree/develop/umaserverdemo)
  - [Java tests for UMA](https://github.com/uma-universal-money-address/uma-kotlin-sdk/blob/main/javatest/src/test/java/me/uma/javatest/UmaTest.java)
  - [Python Tests](https://github.com/uma-universal-money-address/uma-python-sdk/blob/main/uma/__tests__/test_uma.py)
  - [Typescript VASP using express](https://github.com/lightsparkdev/js-sdk/tree/main/apps/examples/uma-vasp)
- [UMA Discord](https://discord.gg/K4e7ghAJ)

## Protocol Sequence Diagram

![UMA Protocol Diagram](https://static.swimlanes.io/45937cd6863fe73964d5f1217320d80e.png)

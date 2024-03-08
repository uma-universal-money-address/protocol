# UMAD-02: Keys, Authentication, and Encryption

## Keys

Before VASPs start sending and receiving UMA payments, they need to generate keys which will be used to authenticate
themselves to other VASPs and to receive and decrypt encrypted blobs for sensitive information (like payment and Travel
Rule data).

**The keys used in UMA are secp256k1 keys**. They are used to sign, verify, encrypt, and decrypt messages. As an example,
to create secp256k1 keys using openssl, run:

```bash
# Generate a secp256k1 key:
$ openssl ecparam -genkey -name secp256k1 -out ec_key.pem

# Print out the key data:
$ openssl ec -in ec_key.pem -noout -text
```

There are two secp256k1 key pairs used in the UMA protocol, the signing key and encryption key. The signing key is used
for signing messages sent to other VASPs and for verifying that other VASPs are who they claim to be. The encryption
key is used to encrypt sensitive data sent to you, like payment and Travel Rule information. Note that in practice,
these can actually be the same key for convenience. Keys can also be configured to expire as described in the following
section.

## Public Key Exchange

The UMA protocol relies on X.509 certificates for public key exchange among VASPs. VASPs expose their certificates to
other VASPs by responding to `GET` requests at the endpoint `https://<vaspdomain>/.well-known/lnurlpubkey`. This
endpoint returns a JSON object with the following structure:

```json
{
  // Used to verify signatures from VASP1. PEM-encoded X.509 certificate string.
  "signingCertificate": string,
  // Used to encrypt TR info sent to VASP1. PEM-encoded X.509 certificate string.
  "encryptionCertificate": string,
  // [Optional] Sec since epoch at which these certificates must be revalidated or refreshed.
  // If not specified, the certificates will not be cached.
  "expirationTimestamp": number
}
```

If a VASP trusts the party that they wish to transact with, typically established through prior communication,
self-signed certificates are a suitable solution for key exchange. VASPs can create self-signed certificates wrapping
the public keys generated above using common tools such as `openssl`, and expose these certificates to counterparties
via the public API outlined above. It is important to note that self-signed certificates don't provide a good
revocation mechanism, so it is recommended to use a short caching duration (on the order of a few minutes) to minimize
the risk of key compromise.

Because the `/.well-known/lnurlpubkey` endpoint is hosted directly on the VASP's domain, it is easy for other VASPs to
verify that the keys they receive are actually from the VASP they are trying to communicate with. It does, however,
imply trust in the VASP's domain and DNS. As an additional security measure, VASPs can also verify the authenticity of
the certificates they receive by communicating with a **VASP Identity Authority**, a trusted 3rd party who maintains a
mapping from VASP domains to certificates. This step is optional and any VASP ID Authority will provide APIs or
interfaces separate from UMA.

A VASP can inspire more trust from its counterparties by retrieving and using a certificate signed by a trusted VASP ID
Authority. When a VASP receives a signed certificate, they can check if it is signed by an authority that they trust,
and hence, trust the underlying VASP. VASPs have the ability to invalidate their certificates in the case of key
compromise or security-related key rotations. The issuing ID authority must keep track of certificates that are
revoked, and provide this information to counterparties via Certificate Revocation Lists (CRLs) or an Online
Certificate Status Protocol (OCSP) server. The URLs for accessing an ID authority's CRL/OCSP can be found inside the
certificate, and VASPs should periodically check the validity of the certificates they receive to ensure compliance and
security. In the event that the counterparty's certificate is revoked, the VASP can request a new set of certificates
and validate them. Optionally, the counterparty can specify an expiration timestamp at which the VASP is required to
revalidate the certificates, in addition to periodic validation.

## Authentication

Some messages in the UMA protocol must be signed by the VASP who created the message using ECDSA and the secp256k1 keys
as described above. Signatures are created using a VASP's private signing key. The signature is then verified by the
receiving VASP using the sending VASP's signing public key from the `signingCertificate`. The signature is included in
the message itself, along with the sending VASP's domain if needed. The receiving VASP can then verify the signature
using the public key and ensure that the message was not tampered with.

## Encryption

VASPs encrypt sensitive information like payment and Travel Rule information using the receiving VASP's encryption
public key from the `encryptionCertificate` via
[ECIES](https://cryptobook.nakov.com/asymmetric-key-ciphers/ecies-public-key-encryption). The receiving VASP can then
decrypt the data using their private encryption key only when required for compliance reasons.

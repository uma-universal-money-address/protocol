# UMAD-02: Keys, Authentication, and Encryption

## Keys

Before VASPs start sending and receiving UMA payments, they need to generate keys which are be used to authenticate
themselves to other VASPs and to receive and decrypt encrypted blobs for sensitive information (like payment and Travel
Rule data).

**The keys used in UMA are secp256k1 keys**. They are used to sign, verify, encrypt, and decrypt messages. As an example,
to create secp256k1 keys using openssl, run:

```bash
# Generate a secp256k1 key:
$ openssl ecparam -genkey -name secp256k1 -out ec_key.pem -param_enc explicit

# Print out the key data:
$ openssl ec -in ec_key.pem -noout -text
```

There are two secp256k1 key pairs used in the UMA protocol, the signing key and encryption key. The signing key is used
for signing messages sent to other VASPs and for verifying that other VASPs are who they claim to be. The encryption
key is used to encrypt sensitive data sent to you, like payment and Travel Rule information. Note that in practice,
these can actually be the same key for convenience. Keys can also be configured to expire as described in the following
section.

## Public Key Exchange

VASPs expose their public keys to other VASPs by responding to `GET` requests at the endpoint
`https://<vaspdomain>/.well-known/lnurlpubkey`. This endpoint returns a JSON object with the following structure:

```json
{
  // Used to verify signatures from VASP1. Hex-encoded secp256k1 pub key string.
  "signingPubKey": string,
  // Used to encrypt TR info sent to VASP1. Hex-encoded secp256k1 pub key string.
  "encryptionPubKey": string,
  // [Optional] Sec since epoch at which these pub keys must be refreshed.
  // They can be safely cached until this expiration.
  "expirationTimestamp": number
}
```

VASPs can also use this endpoint to refresh their keys by returning a new set of keys with a new expiration timestamp.
This is useful if a VASP's keys are compromised or if they want to rotate their keys for security reasons. When receiving
a new set of keys, VASPs can cache them until the expiration timestamp.

Because the `/.well-known/lnurlpubkey` endpoint is hosted directly on the VASP's domain, it is easy for other VASPs to
verify that the keys they receive are actually from the VASP they are trying to communicate with. It does, however, imply
trust in the VASP's domain and DNS. As an additional security measure, VASPs can also verify the authenticity of the
keys they receive by communicating with a **VASP Identity Authority**, a trusted 3rd party who maintains a mapping from
VASP domains to public keys. This step is optional and any VASP ID Authority will provide APIs or interfaces separate
from UMA.

## Authentication

Some messages in the UMA protcol must be signed by the VASP who created the message using ECDSA and the secp256k1 keys
as described above. Signatures are created using a VASP's private signing key. The signature is then verified by the
receiving VASP using the sending VASP's `signingPubKey`. The signature is included in the message itself, along with the
sending VASP's domain if needed. The receiving VASP can then verify the signature using the public key and ensure that
the message was not tampered with.

## Encryption

VASPs encrypt sensitive information like payment and Travel Rule information using the receiving VASP's `encryptionPubKey`
via [ECIES](https://cryptobook.nakov.com/asymmetric-key-ciphers/ecies-public-key-encryption). The receiving VASP can
then decrypt the data using their private encryption key only when required for compliance reasons.

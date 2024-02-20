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

TThe UMA protocol relies on X.509 certificates for public key exchange among VASPs. In order to obtain an X.509 certificate, the
VASP is required to submit a request to a trusted certificate authority (CA), which issues the certificate. The issuing CA must keep
track of certificates that are revoked, and provide this information to other parties via Certificate Revocation Lists (CRLs)
or an Online Certificate Status Protocol (OCSP) server. The URLs for accessing a CA's CRL/OCSP can be found inside the certificate,
and VASPs should ensure the validity of all of the certificates they receive to ensure compliance and security.

It is not recommended for VASPs to use self-signed certificates when communicating with other VASPs outside their organization.
They should only be used in test environments. To generate a self-signed X.509 certificate based on the key generated above,
run:

```bash
# Generate a certificate based on the key we generated:
$ openssl req -new -x509 -key ec_key.pem -sha256 -nodes -out ec_crt.crt -days <expiration in days>

# Print out the certificate data:
$ openssl x509 -in ec_crt.crt -noout -text
```

VASPs expose their certificates to other VASPs by responding to `GET` requests at the endpoint
`https://<vaspdomain>/.well-known/lnurlpubkey`. This endpoint returns a JSON object with the following structure:

```json
{
  // Used to verify signatures from VASP1. Base64-encoded X.509 certificate string.
  "signingCertificate": string,
  // Used to encrypt TR info sent to VASP1. Base64-encoded X.509 certificate string.
  "encryptionCertificate": string,
  // [Optional] Sec since epoch at which these certificates must be revalidated or refreshed.
  "expirationTimestamp": number
}
```

VASPs can revoke their certificates if their keys are compromised or if they want to rotate their keys for security reasons. For this
reason, VASPs should periodically check certificates for revocation. In the event that the counter party's certificate is revoked, the VASP
can request a new set of certificates at the same endpoint and validate them. Optionally, the counter party can specify an expiration
timestamp at which the VASP is required to revalidate or refresh their certificates, outside of periodic validation.

## Authentication

Some messages in the UMA protcol must be signed by the VASP who created the message using ECDSA and the secp256k1 keys
as described above. Signatures are created using a VASP's private signing key. The signature is then verified by the
receiving VASP using the sending VASP's signing public key from the `signingCertificate`. The signature is included in the message
itself, along with the sending VASP's domain if needed. The receiving VASP can then verify the signature using the public key and
 ensure that the message was not tampered with.

## Encryption

VASPs encrypt sensitive information like payment and Travel Rule information using the receiving VASP's encryption public key from
the `encryptionCertificate` via [ECIES](https://cryptobook.nakov.com/asymmetric-key-ciphers/ecies-public-key-encryption). The receiving
VASP can then decrypt the data using their private encryption key only when required for compliance reasons.

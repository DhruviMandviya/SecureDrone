import oqs

SIGNATURE_ALGORITHM = "ML-DSA-65"

print("=" * 50)
print("ML-DSA Signature Demo")
print("=" * 50)

with oqs.Signature(SIGNATURE_ALGORITHM) as signer:

    public_key = signer.generate_keypair()

    private_key = signer.export_secret_key()

    print("\nSigning Key Pair Generated")

    print("Public Key Length :", len(public_key), "bytes")

    print("Private Key Length:", len(private_key), "bytes")
    message = b"SecureDrone Controller Authentication"
    signature = signer.sign(message)
    print("\nMessage Signed Successfully")
    print("Message :", message.decode())
    print("Signature Length:", len(signature), "bytes")
    is_valid = signer.verify(message, signature, public_key)
    print("\nSignature Verification:", is_valid)
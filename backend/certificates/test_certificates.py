from backend.security.keypair import KeyPair

from backend.certificates.ca import CertificateAuthority
from backend.certificates.certificate import create_certificate
from backend.certificates.serializer import CertificateSerializer
from backend.certificates.certificate_store import CertificateStore
from backend.certificates.verifier import CertificateVerifier

print("=" * 70)
print("SecureDrone PKI Test Suite")
print("=" * 70)

# ---------------------------------------------------
print("\n[1] Testing KeyPair")

keys = KeyPair()
keys.generate()

print("✓ KeyPair Generated")

# ---------------------------------------------------
print("\n[2] Testing Certificate Authority")

ca = CertificateAuthority()

ca.generate_keys()

print("✓ Certificate Authority Working")

# ---------------------------------------------------
print("\n[3] Testing Save/Load Keys")

ca.save_keys()
ca.load_keys()

print("✓ Key Persistence Working")

# ---------------------------------------------------
print("\n[4] Testing Certificate Creation")

certificate = create_certificate(
    "drone001",
    "drone",
    "TEST_PUBLIC_KEY"
)

print("✓ Certificate Created")

# ---------------------------------------------------
print("\n[5] Testing Serialization")

json_data = CertificateSerializer.to_json(
    certificate
)

certificate = CertificateSerializer.from_json(
    json_data
)

print("✓ Serialization Working")

# ---------------------------------------------------
print("\n[6] Testing Certificate Store")

store = CertificateStore()

store.save(certificate)

certificate = store.load("drone001")

print("✓ Store Working")

# ---------------------------------------------------
print("\n[7] Testing Certificate Signing")

certificate = ca.sign_certificate(
    certificate
)

print("✓ Signing Working")

# ---------------------------------------------------
print("\n[8] Testing Certificate Verification")

valid = CertificateVerifier.verify(
    certificate,
    ca.keys.public_key
)

if valid:
    print("✓ Verification Working")
else:
    raise Exception("Verification Failed")

# ---------------------------------------------------

print("\n" + "=" * 70)
print("🎉 ALL PKI TESTS PASSED SUCCESSFULLY")
print("=" * 70)
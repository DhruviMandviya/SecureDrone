from backend.certificates.ca import CertificateAuthority
from backend.certificates.certificate import create_certificate
from backend.certificates.certificate_store import CertificateStore
from backend.certificates.verifier import CertificateVerifier

print("=" * 70)
print("SecureDrone PKI Demonstration")
print("=" * 70)

# Create Root CA
ca = CertificateAuthority()

print("\n[1] Generating Root CA Keys")
ca.generate_keys()

print("\n[2] Saving Root CA Keys")
ca.save_keys()

print("\n[3] Loading Root CA Keys")
ca.load_keys()

print("\n[4] Creating Drone Certificate")

certificate = create_certificate(
    "drone001",
    "drone",
    "TEST_PUBLIC_KEY"
)

print("\n[5] Signing Certificate")

certificate = ca.sign_certificate(
    certificate
)

print("\n[6] Saving Certificate")

store = CertificateStore()

store.save(certificate)

print("\n[7] Loading Certificate")

loaded_certificate = store.load(
    "drone001"
)

print("\n[8] Verifying Certificate")

valid = CertificateVerifier.verify(
    loaded_certificate,
    ca.keys.public_key
)

print()

if valid:
    print("🎉 SecureDrone PKI Demo Completed Successfully")
else:
    print("❌ Verification Failed")
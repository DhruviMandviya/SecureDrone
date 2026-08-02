from backend.authentication.identity import DeviceIdentity
from backend.authentication.handshake import SecureHandshake

from backend.certificates.ca import CertificateAuthority
from backend.certificates.certificate import create_certificate

from backend.communication.telemetry import Telemetry
from backend.communication.secure_channel import SecureChannel

print("=" * 70)
print("SecureDrone Authentication & Communication Test Suite")
print("=" * 70)

# --------------------------------------------------
print("\n[1] Testing Device Identity")

certificate = create_certificate(
    "drone001",
    "drone",
    "TEST_PUBLIC_KEY"
)

identity = DeviceIdentity.create(
    "drone001",
    "drone",
    certificate
)

print("✓ Device Identity Passed")

# --------------------------------------------------
print("\n[2] Testing Certificate Authority")

ca = CertificateAuthority()

ca.generate_keys()

print("✓ Certificate Authority Passed")

# --------------------------------------------------
print("\n[3] Testing Certificate Signing")

certificate = ca.sign_certificate(
    certificate
)

print("✓ Certificate Signing Passed")

# --------------------------------------------------
print("\n[4] Testing Secure Handshake")

session = SecureHandshake.establish(
    identity,
    ca.keys.public_key
)

print("✓ Secure Handshake Passed")

# --------------------------------------------------
print("\n[5] Testing Secure Session")

print("Authenticated :", session.authenticated)

print("✓ Secure Session Passed")

# --------------------------------------------------
print("\n[6] Testing Telemetry Encryption")

telemetry = Telemetry.sample()

encrypted = SecureChannel.encrypt(
    session,
    telemetry
)

print("✓ Encryption Passed")

# --------------------------------------------------
print("\n[7] Testing Telemetry Decryption")

decrypted = SecureChannel.decrypt(
    session,
    encrypted
)

if (
    decrypted["latitude"] == telemetry.latitude
    and
    decrypted["longitude"] == telemetry.longitude
):
    print("✓ Decryption Passed")
else:
    raise Exception("Telemetry Verification Failed")

# --------------------------------------------------

print("\n" + "=" * 70)
print("🎉 ALL AUTHENTICATION & COMMUNICATION TESTS PASSED")
print("=" * 70)
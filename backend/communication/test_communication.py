from backend.authentication.identity import DeviceIdentity
from backend.authentication.handshake import SecureHandshake

from backend.certificates.ca import CertificateAuthority
from backend.certificates.certificate import create_certificate

from backend.communication.telemetry import Telemetry
from backend.communication.secure_channel import SecureChannel

print("=" * 70)
print("Testing Secure Communication")
print("=" * 70)

# Root CA
ca = CertificateAuthority()
ca.generate_keys()

# Certificate
certificate = create_certificate(
    "drone001",
    "drone",
    "TEST_PUBLIC_KEY"
)

certificate = ca.sign_certificate(
    certificate
)

# Identity
identity = DeviceIdentity.create(
    "drone001",
    "drone",
    certificate
)

# Secure Session
session = SecureHandshake.establish(
    identity,
    ca.keys.public_key
)

# Sample Telemetry
telemetry = Telemetry.sample()

# Encrypt
encrypted = SecureChannel.encrypt(
    session,
    telemetry
)

# Decrypt
decrypted = SecureChannel.decrypt(
    session,
    encrypted
)

print()

print("Latitude :", decrypted["latitude"])
print("Longitude :", decrypted["longitude"])
print("Altitude :", decrypted["altitude"])
print("Battery :", decrypted["battery"])
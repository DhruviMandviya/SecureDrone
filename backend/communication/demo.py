from backend.authentication.identity import DeviceIdentity
from backend.authentication.handshake import SecureHandshake

from backend.certificates.ca import CertificateAuthority
from backend.certificates.certificate import create_certificate

from backend.communication.telemetry import Telemetry
from backend.communication.secure_channel import SecureChannel

print("=" * 70)
print("SecureDrone Complete Communication Demo")
print("=" * 70)

print("\n[1] Creating Root Certificate Authority")

ca = CertificateAuthority()
ca.generate_keys()

print("\n[2] Creating Drone Certificate")

certificate = create_certificate(
    "drone001",
    "drone",
    "TEST_PUBLIC_KEY"
)

certificate = ca.sign_certificate(
    certificate
)

print("\n[3] Creating Device Identity")

identity = DeviceIdentity.create(
    "drone001",
    "drone",
    certificate
)

print("\n[4] Authenticating and Establishing Secure Session")

session = SecureHandshake.establish(
    identity,
    ca.keys.public_key
)

print("\n[5] Generating Telemetry")

telemetry = Telemetry.sample()

print(telemetry)

print("\n[6] Encrypting Telemetry")

encrypted = SecureChannel.encrypt(
    session,
    telemetry
)

print("\nEncrypted Packet")

print(encrypted)

print("\n[7] Decrypting Telemetry")

decrypted = SecureChannel.decrypt(
    session,
    encrypted
)

print("\nRecovered Telemetry")

print(decrypted)

print("\n" + "=" * 70)
print("🎉 SecureDrone End-to-End Communication Successful")
print("=" * 70)
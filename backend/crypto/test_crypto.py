# from crypto_core import (
#     generate_keypair,
#     encapsulate,
#     decapsulate,
#     derive_session_key,
#     encrypt_telemetry_payload,
#     decrypt_telemetry_payload,
#     rotate_session_key
# )

# print("=" * 60)
# print("FINAL TEST - SecureDrone Crypto Module")
# print("=" * 60)

# # Generate key pair
# public_key, private_key = generate_keypair()
# print("✓ Key Pair Generated")

# # Key exchange
# ciphertext, gcs_secret = encapsulate(public_key)
# drone_secret = decapsulate(private_key, ciphertext)

# assert gcs_secret == drone_secret
# print("✓ Key Exchange Successful")

# # Session key derivation
# gcs_key = derive_session_key(gcs_secret)
# drone_key = derive_session_key(drone_secret)

# assert gcs_key == drone_key
# print("✓ Session Key Derived")

# # Sample telemetry
# telemetry = {
#     "lat": 19.0760,
#     "lon": 72.8777,
#     "altitude": 120,
#     "battery": 78,
#     "speed": 10
# }

# # Encrypt
# encrypted = encrypt_telemetry_payload(gcs_key, telemetry)
# print("✓ Telemetry Encrypted")

# # Decrypt
# decrypted = decrypt_telemetry_payload(drone_key, encrypted)

# assert telemetry == decrypted
# print("✓ Telemetry Decrypted Successfully")

# # Test key rotation
# new_key = rotate_session_key()

# assert len(new_key) == 32
# assert new_key != gcs_key

# print("✓ Session Key Rotated")

# print("\nAll tests passed successfully!")
# print("=" * 60)
# print("🎉 SecureDrone crypto_core.py is COMPLETE!")
# print("=" * 60)
# from crypto_core import generate_signing_keypair

# print("=" * 50)
# print("Testing generate_signing_keypair()")
# print("=" * 50)

# public_key, private_key = generate_signing_keypair()

# print("✓ Signing Key Pair Generated")

# print("Public Key Length :", len(public_key), "bytes")
# print("Private Key Length:", len(private_key), "bytes")
# from crypto_core import generate_signing_keypair, sign

# print("=" * 50)
# print("Testing sign()")
# print("=" * 50)

# # Generate signing keys
# public_key, private_key = generate_signing_keypair()

# print("✓ Signing Key Pair Generated")

# # Message to sign
# message = b"SecureDrone Controller Authentication"

# # Sign the message
# signature = sign(private_key, message)

# print("✓ Message Signed Successfully")

# print("Message:", message.decode())
# print("Signature Length:", len(signature), "bytes")
# from crypto_core import (
#     generate_signing_keypair,
#     sign,
#     verify
# )

# print("=" * 60)
# print("Testing ML-DSA Identity Layer")
# print("=" * 60)

# # Step 1 - Generate signing keys
# public_key, private_key = generate_signing_keypair()

# print("✓ Signing Key Pair Generated")

# # Step 2 - Create message
# message = b"SecureDrone Controller Authentication"

# print("✓ Message Created")

# # Step 3 - Sign message
# signature = sign(private_key, message)

# print("✓ Message Signed")

# # Step 4 - Verify signature
# is_valid = verify(public_key, message, signature)

# print("✓ Signature Verification Result:", is_valid)

# assert is_valid == True

# print("\n🎉 ML-DSA Identity Layer Working Successfully")
from crypto_core import (
    generate_keypair,
    encapsulate,
    decapsulate,
    derive_session_key,
    encrypt_telemetry_payload,
    decrypt_telemetry_payload,
    rotate_session_key,
    generate_signing_keypair,
    sign,
    verify
)

print("=" * 70)
print("SecureDrone Crypto Module - Complete Test")
print("=" * 70)

# ==================================================
# ML-KEM TEST
# ==================================================

print("\n[1] Testing ML-KEM Handshake")

public_key, private_key = generate_keypair()

ciphertext, gcs_secret = encapsulate(public_key)

drone_secret = decapsulate(private_key, ciphertext)

assert gcs_secret == drone_secret

print("✓ ML-KEM Handshake Successful")

# ==================================================
# HKDF TEST
# ==================================================

print("\n[2] Testing HKDF")

gcs_key = derive_session_key(gcs_secret)

drone_key = derive_session_key(drone_secret)

assert gcs_key == drone_key

print("✓ Session Key Generated")

# ==================================================
# AES TEST
# ==================================================

print("\n[3] Testing AES-256-GCM")

telemetry = {
    "lat": 19.0760,
    "lon": 72.8777,
    "battery": 78,
    "altitude": 120,
    "speed": 10
}

encrypted = encrypt_telemetry_payload(
    gcs_key,
    telemetry
)

decrypted = decrypt_telemetry_payload(
    drone_key,
    encrypted
)

assert telemetry == decrypted

print("✓ Encryption Successful")
print("✓ Decryption Successful")

# ==================================================
# KEY ROTATION TEST
# ==================================================

print("\n[4] Testing Key Rotation")

new_key = rotate_session_key()

assert len(new_key) == 32

print("✓ Key Rotation Successful")

# ==================================================
# ML-DSA TEST
# ==================================================

print("\n[5] Testing ML-DSA Identity Layer")

sign_public_key, sign_private_key = generate_signing_keypair()

message = b"SecureDrone Controller Authentication"

signature = sign(sign_private_key, message)

assert verify(sign_public_key, message, signature)

print("✓ Signing Successful")
print("✓ Verification Successful")

print("\n" + "=" * 70)
print("🎉 ALL CRYPTO TESTS PASSED SUCCESSFULLY")
print("=" * 70)
from crypto_core import (
    generate_keypair,
    encapsulate,
    decapsulate,
    derive_session_key,
    encrypt_telemetry_payload,
    decrypt_telemetry_payload,
    rotate_session_key
)

print("=" * 60)
print("FINAL TEST - SecureDrone Crypto Module")
print("=" * 60)

# Generate key pair
public_key, private_key = generate_keypair()
print("✓ Key Pair Generated")

# Key exchange
ciphertext, gcs_secret = encapsulate(public_key)
drone_secret = decapsulate(private_key, ciphertext)

assert gcs_secret == drone_secret
print("✓ Key Exchange Successful")

# Session key derivation
gcs_key = derive_session_key(gcs_secret)
drone_key = derive_session_key(drone_secret)

assert gcs_key == drone_key
print("✓ Session Key Derived")

# Sample telemetry
telemetry = {
    "lat": 19.0760,
    "lon": 72.8777,
    "altitude": 120,
    "battery": 78,
    "speed": 10
}

# Encrypt
encrypted = encrypt_telemetry_payload(gcs_key, telemetry)
print("✓ Telemetry Encrypted")

# Decrypt
decrypted = decrypt_telemetry_payload(drone_key, encrypted)

assert telemetry == decrypted
print("✓ Telemetry Decrypted Successfully")

# Test key rotation
new_key = rotate_session_key()

assert len(new_key) == 32
assert new_key != gcs_key

print("✓ Session Key Rotated")

print("\nAll tests passed successfully!")
print("=" * 60)
print("🎉 SecureDrone crypto_core.py is COMPLETE!")
print("=" * 60)
import os
import json
import base64
import oqs

from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

KEM_ALGORITHM = "ML-KEM-768"


# -----------------------------
# Generate AES-256 Session Key
# -----------------------------
def derive_session_key(shared_secret):
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"securedrone-v1"
    )
    return hkdf.derive(shared_secret)


# -----------------------------
# Encrypt Telemetry
# -----------------------------
def encrypt_data(session_key, telemetry):

    plaintext = json.dumps(telemetry).encode()

    nonce = os.urandom(12)

    aes = AESGCM(session_key)

    encrypted = aes.encrypt(nonce, plaintext, None)

    ciphertext = encrypted[:-16]
    tag = encrypted[-16:]

    return {
        "nonce": base64.b64encode(nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "tag": base64.b64encode(tag).decode()
    }


# -----------------------------
# Decrypt Telemetry
# -----------------------------
def decrypt_data(session_key, encrypted):

    nonce = base64.b64decode(encrypted["nonce"])
    ciphertext = base64.b64decode(encrypted["ciphertext"])
    tag = base64.b64decode(encrypted["tag"])

    aes = AESGCM(session_key)

    plaintext = aes.decrypt(
        nonce,
        ciphertext + tag,
        None
    )

    return json.loads(plaintext)


# ======================================================
# MAIN PROGRAM
# ======================================================

print("="*50)
print("SecureDrone Encryption Demo")
print("="*50)

# Drone
with oqs.KeyEncapsulation(KEM_ALGORITHM) as drone:

    public_key = drone.generate_keypair()

    # Ground Station
    with oqs.KeyEncapsulation(KEM_ALGORITHM) as gcs:

        ciphertext, secret_gcs = gcs.encap_secret(public_key)

    secret_drone = drone.decap_secret(ciphertext)

assert secret_drone == secret_gcs

print("\nShared Secret Generated")

session_key = derive_session_key(secret_drone)

print("AES Session Key Generated")
print("Key Length:", len(session_key), "bytes")

telemetry = {
    "lat": 19.0760,
    "lon": 72.8777,
    "altitude": 120,
    "battery": 78,
    "speed": 10
}

print("\nOriginal Telemetry")
print(telemetry)

encrypted = encrypt_data(session_key, telemetry)

print("\nEncrypted Payload")
print(encrypted)

decrypted = decrypt_data(session_key, encrypted)

print("\nDecrypted Telemetry")
print(decrypted)

print("\nSUCCESS")
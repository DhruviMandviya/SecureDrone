import os
import json
import base64
import oqs

from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

KEM_ALGORITHM = "ML-KEM-768"
def generate_keypair():
    """
    Generates a ML-KEM-768 key pair.

    Returns:
        tuple: (public_key, private_key)
    """

    kem = oqs.KeyEncapsulation(KEM_ALGORITHM)

    public_key = kem.generate_keypair()

    private_key = kem.export_secret_key()

    kem.free()

    return public_key, private_key
def encapsulate(peer_public_key):
    """
    Generates a ciphertext and shared secret
    using the peer's public key.

    Returns:
        tuple: (ciphertext, shared_secret)
    """

    kem = oqs.KeyEncapsulation(KEM_ALGORITHM)

    ciphertext, shared_secret = kem.encap_secret(peer_public_key)

    kem.free()

    return ciphertext, shared_secret
def decapsulate(private_key, ciphertext):
    """
    Recovers the shared secret using the
    private key and ciphertext.

    Returns:
        shared_secret
    """

    with oqs.KeyEncapsulation(KEM_ALGORITHM, private_key) as kem:
        shared_secret = kem.decap_secret(ciphertext)

    return shared_secret
def derive_session_key(shared_secret):
    """
    Derives a 32-byte AES-256 session key
    from the shared secret using HKDF-SHA256.

    Returns:
        bytes: 32-byte AES session key
    """

    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"securedrone-v1"
    )

    session_key = hkdf.derive(shared_secret)

    return session_key
def encrypt_telemetry_payload(session_key, telemetry):
    """
    Encrypts a telemetry dictionary using AES-256-GCM.

    Returns:
        dict containing:
            nonce
            ciphertext
            tag
    """

    plaintext = json.dumps(telemetry).encode()

    nonce = os.urandom(12)

    aes = AESGCM(session_key)

    encrypted = aes.encrypt(
        nonce,
        plaintext,
        None
    )

    ciphertext = encrypted[:-16]
    tag = encrypted[-16:]

    return {
        "nonce": base64.b64encode(nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "tag": base64.b64encode(tag).decode()
    }
def decrypt_telemetry_payload(session_key, encrypted_payload):
    """
    Decrypts an AES-256-GCM encrypted telemetry payload.

    Returns:
        Original telemetry dictionary
    """

    nonce = base64.b64decode(encrypted_payload["nonce"])
    ciphertext = base64.b64decode(encrypted_payload["ciphertext"])
    tag = base64.b64decode(encrypted_payload["tag"])

    aes = AESGCM(session_key)

    plaintext = aes.decrypt(
        nonce,
        ciphertext + tag,
        None
    )

    return json.loads(plaintext)
def rotate_session_key():
    """
    Generates a fresh 32-byte AES-256 session key.

    This can be used to periodically rotate encryption
    keys for enhanced security.
    """

    return AESGCM.generate_key(bit_length=256)
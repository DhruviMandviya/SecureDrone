from backend.crypto.crypto_core import (
    generate_keypair,
    decapsulate,
    derive_session_key
)


class HandshakeManager:
    """
    Handles ML-KEM key exchange.
    """

    def __init__(self):

        self.public_key = None
        self.private_key = None

    def start(self):

        self.public_key, self.private_key = (
            generate_keypair()
        )

        print(
            "✓ Ground Station Key Pair Generated"
        )

        return self.public_key

    def complete(
        self,
        ciphertext
    ):

        shared_secret = decapsulate(
            self.private_key,
            ciphertext
        )

        session_key = derive_session_key(
            shared_secret
        )

        print(
            "✓ Ground Station Session Key Created"
        )

        return session_key
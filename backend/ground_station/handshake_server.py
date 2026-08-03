from backend.crypto.crypto_core import (
    generate_keypair
)


class HandshakeServer:
    """
    Handles ML-KEM handshake for the Ground Control Station.
    """

    def __init__(self):

        self.public_key = None
        self.private_key = None

    def create_keypair(self):

        self.public_key, self.private_key = (
            generate_keypair()
        )

        print("✓ Ground Station ML-KEM Key Pair Generated")

        return {
            "public_key": self.public_key.hex()
        }
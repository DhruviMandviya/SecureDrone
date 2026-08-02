from backend.authentication.authenticator import Authenticator
from backend.authentication.session import SecureSession

from backend.crypto.crypto_core import (
    generate_keypair,
    encapsulate,
    decapsulate,
    derive_session_key
)


class SecureHandshake:
    """
    Performs authenticated ML-KEM handshake.
    """

    @staticmethod
    def establish(identity, ca_public_key):

        if not Authenticator.authenticate(
            identity,
            ca_public_key
        ):
            raise Exception(
                "Authentication Failed"
            )

        public_key, private_key = generate_keypair()

        ciphertext, shared_secret_sender = encapsulate(
            public_key
        )

        shared_secret_receiver = decapsulate(
            private_key,
            ciphertext
        )

        session_key = derive_session_key(
            shared_secret_receiver
        )

        session = SecureSession.create(
            identity,
            shared_secret_receiver,
            session_key
        )

        print("✓ ML-KEM Handshake Completed")

        return session
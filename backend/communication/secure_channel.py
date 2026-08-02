from backend.crypto.crypto_core import (
    encrypt_telemetry_payload,
    decrypt_telemetry_payload
)


class SecureChannel:
    """
    Secure telemetry communication.
    """

    @staticmethod
    def encrypt(session, telemetry):

        encrypted = encrypt_telemetry_payload(
            session.session_key,
            telemetry.to_dict()
        )

        print("✓ Telemetry Encrypted")

        return encrypted

    @staticmethod
    def decrypt(session, encrypted_payload):

        telemetry = decrypt_telemetry_payload(
            session.session_key,
            encrypted_payload
        )

        print("✓ Telemetry Decrypted")

        return telemetry
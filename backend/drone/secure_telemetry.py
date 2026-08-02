from backend.communication.secure_channel import SecureChannel


class SecureTelemetry:
    """
    Encrypts and decrypts live telemetry.
    """

    def __init__(self, session):
        self.session = session

    def encrypt(self, telemetry):
        """
        Encrypt telemetry using the secure session.
        """

        return SecureChannel.encrypt(
            self.session,
            telemetry
    )

    def decrypt(self, encrypted_packet):
        """
        Decrypt telemetry using the secure session.
        """

        return SecureChannel.decrypt(
            self.session,
            encrypted_packet
        )
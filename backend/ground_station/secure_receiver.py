from backend.communication.secure_channel import (
    SecureChannel
)


class SecureReceiver:
    """
    Decrypts encrypted telemetry received by the
    Ground Control Station.
    """

    def __init__(self, session):
        self.session = session

    def decrypt(self, packet):

        print()
        print("Decrypting Packet...")

        telemetry = SecureChannel.decrypt(
            self.session,
            packet
        )

        print("✓ Packet Decrypted")

        return telemetry
from backend.ground_station.models import (
    EncryptedTelemetry,
    GroundStationResponse
)

from backend.ground_station.session_manager import (
    SessionManager
)

from backend.ground_station.secure_receiver import (
    SecureReceiver
)
from backend.ground_station.telemetry_store import (
    TelemetryStore
)

class GroundStationReceiver:
    """
    Receives encrypted telemetry.
    """

    @staticmethod
    def receive(packet: EncryptedTelemetry):

        print()
        print("Ground Control Station")
        print("Encrypted Packet Received")

        session = SessionManager.get(
    packet.device_id
    )

        if session is None:

            return GroundStationResponse(
                status="error",
                message="No Secure Session."
            )

        receiver = SecureReceiver(
            session
        )

        packet_data = packet.model_dump()

        packet_data.pop("device_id")

        telemetry = receiver.decrypt(
    packet_data
)

        TelemetryStore.add(
            telemetry
        )

        print()

        print("Recovered Telemetry")

        print(telemetry)

        print()

        print(
            f"Telemetry History Size : {len(TelemetryStore.all())}"
        )

        return GroundStationResponse(
            status="success",
            message="Telemetry Decrypted Successfully."
        )
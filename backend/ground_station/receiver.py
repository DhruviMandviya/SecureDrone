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
from backend.ground_station.log_store import LogStore

class GroundStationReceiver:
    """
    Receives encrypted telemetry.
    """

    @staticmethod
    def receive(packet: EncryptedTelemetry):

        print()
        print("Ground Control Station")
        print("Encrypted Packet Received")

        session = SessionManager.get(packet.device_id)

        if session is None:
            return GroundStationResponse(
                status="error",
                message="No Secure Session."
            )

        receiver = SecureReceiver(session)

        packet_data = packet.model_dump()
        packet_data.pop("device_id")

        telemetry = receiver.decrypt(packet_data)
        LogStore.add("Telemetry packet decrypted", "SUCCESS")

        print("===================================")
        print("DECRYPTED TELEMETRY RECEIVED")
        print(telemetry)
        print("===================================")

        TelemetryStore.add(telemetry)
        LogStore.add("Telemetry stored successfully", "INFO")

        info = SessionManager.get_info(packet.device_id)

        if info:
            info.bytes_received += len(packet.ciphertext)
            info.bytes_sent += len(packet.ciphertext)
            LogStore.add(
            f"Encrypted packet received ({len(packet.ciphertext)} bytes)",
            "INFO"
        )

        print("STORE SIZE =", len(TelemetryStore.all()))

        return GroundStationResponse(
            status="success",
            message="Telemetry Decrypted Successfully."
        )
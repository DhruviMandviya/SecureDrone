import asyncio
import requests
from backend.certificates.ca import CertificateAuthority
from backend.authentication.identity import DeviceIdentity

from backend.drone.authentication_client import AuthenticationClient
from backend.drone.handshake_client import HandshakeClient
from backend.drone.ground_station_client import GroundStationClient

from backend.drone.px4_connection import PX4Connection
from backend.drone.telemetry_reader import TelemetryReader
from backend.drone.drone_controller import DroneController
from backend.drone.secure_telemetry import SecureTelemetry

from backend.crypto.crypto_core import (
    encapsulate,
    derive_session_key
)

from backend.drone.telemetry_streamer import (
    TelemetryStreamer
)


def update_mission(status):
    try:
        requests.post(
            "http://127.0.0.1:8000/mission/update",
            json={"status": status},
            timeout=2
        )
    except Exception:
        pass

class Session:
    """
    Holds the AES session key.
    """

    def __init__(self, session_key):
        self.session_key = session_key



async def main():

    print("=" * 70)
    print("SecureDrone Live Telemetry Demo")
    print("=" * 70)

    # -------------------------------------------------
    # CONNECT TO PX4
    # -------------------------------------------------

    connection = PX4Connection()
    drone = await connection.connect()

    # -------------------------------------------------
    # CREATE SECURE SESSION
    # -------------------------------------------------

    print()
    print("Creating Secure Session...")

    ca = CertificateAuthority()
    ca.generate_keys()

    identity = DeviceIdentity.create(
        "drone001",
        "drone",
        ca
    )

    authentication = AuthenticationClient()
    handshake = HandshakeClient()
    ground_station = GroundStationClient()

    authentication.authenticate(
        identity,
        None
    )
    update_mission("AUTHENTICATED")

    print()
    print("Requesting Ground Station Public Key...")

    handshake_response = handshake.start()

    ground_station_public_key = bytes.fromhex(
        handshake_response["public_key"]
    )

    ciphertext, shared_secret = encapsulate(
        ground_station_public_key
    )

    session_key = derive_session_key(
        shared_secret
    )

    handshake.complete(
        identity.device_id,
        ciphertext
    )
    update_mission("HANDSHAKE")

    session = Session(session_key)

    secure_channel = SecureTelemetry(session)

    print("✓ Real ML-KEM Handshake Completed")

    # -------------------------------------------------
    # DRONE OBJECTS
    # -------------------------------------------------

    controller = DroneController(drone)

    reader = TelemetryReader(drone)

    telemetry = await reader.read_telemetry()

    state = reader.get_state()

    print()
    print("Drone State")
    print(state)

    print()
    print("Live Telemetry")
    print(telemetry)

    print()
    print("Encrypting Telemetry...")

    secure_channel.encrypt(telemetry)

    # -------------------------------------------------
    # START LIVE TELEMETRY
    # -------------------------------------------------

    streamer = TelemetryStreamer(
    reader,
    secure_channel,
    ground_station
    )

    print()
    print("=" * 60)
    print("LIVE TELEMETRY STARTED")
    print("=" * 60)

    telemetry_task = asyncio.create_task(
        streamer.stream()
    )

    mission_task = asyncio.create_task(
        controller.demo_mission()
    )

    await mission_task

    telemetry_task.cancel()

    try:
        await telemetry_task
        
    except asyncio.CancelledError:
        pass


if __name__ == "__main__":
    asyncio.run(main())
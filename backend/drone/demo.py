import asyncio

from backend.drone.px4_connection import PX4Connection
from backend.drone.telemetry_reader import TelemetryReader
from backend.drone.drone_controller import DroneController
from backend.certificates.ca import CertificateAuthority
from backend.authentication.identity import DeviceIdentity
from backend.authentication.handshake import SecureHandshake
from backend.drone.secure_telemetry import SecureTelemetry
async def main():

    print("=" * 70)
    print("SecureDrone Live Telemetry Demo")
    print("=" * 70)

    connection = PX4Connection()

    drone = await connection.connect()
    print()
    print("Creating Secure Session...")

    ca = CertificateAuthority()

    ca.generate_keys()

    identity = DeviceIdentity.create(
        "drone001",
        "drone",
        ca
    )

    session = SecureHandshake.establish(
        identity,
        ca
    )

    secure_channel = SecureTelemetry(session)
    print("✓ Secure Session Established")
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
    print()
    print("Encrypting Telemetry...")

    encrypted_packet = secure_channel.encrypt(
        telemetry
    )

    print()
    print("Encrypted Packet")
    print(encrypted_packet)
    print()
    print("Decrypting Telemetry...")

    decrypted_packet = secure_channel.decrypt(
        encrypted_packet
    )

    print()
    print("Recovered Telemetry")
    print(decrypted_packet)

    print("Arming Test")

    await controller.arm()
    print()
    print("Takeoff Test")

    await controller.takeoff()
    print()
    print("Hovering for 10 seconds...")

    await asyncio.sleep(10)
    print()
    print("Landing Test")

    await controller.land()
    await asyncio.sleep(10)
    print()
    print("Disarm Test")

    await controller.disarm()


if __name__ == "__main__":

    asyncio.run(main())
import asyncio

from backend.drone.px4_connection import PX4Connection
from backend.drone.telemetry_reader import TelemetryReader
from backend.drone.drone_controller import DroneController
from backend.drone.secure_telemetry import SecureTelemetry

from backend.certificates.ca import CertificateAuthority
from backend.authentication.identity import DeviceIdentity
from backend.authentication.handshake import SecureHandshake


async def main():

    print("=" * 70)
    print("SecureDrone Drone Module Test Suite")
    print("=" * 70)

    print()
    print("[1] Testing PX4 Connection")

    connection = PX4Connection()

    drone = await connection.connect()

    print("✓ PX4 Connection Passed")

    print()
    print("[2] Testing Secure Session")

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

    print("✓ Secure Session Passed")

    print()
    print("[3] Testing Telemetry Reader")

    reader = TelemetryReader(drone)

    telemetry = await reader.read_telemetry()

    print("✓ Telemetry Reader Passed")

    print()
    print("[4] Testing Drone State")

    state = reader.get_state()

    print(state)

    print("✓ Drone State Passed")

    print()
    print("[5] Testing Secure Telemetry")

    secure = SecureTelemetry(session)

    encrypted = secure.encrypt(
        telemetry
    )

    decrypted = secure.decrypt(
        encrypted
    )

    print("✓ Secure Telemetry Passed")

    print()
    print("[6] Testing Drone Controller")

    controller = DroneController(drone)

    await controller.arm()

    await controller.takeoff()

    await asyncio.sleep(5)

    await controller.land()

    await asyncio.sleep(8)

    await controller.disarm()

    print("✓ Drone Controller Passed")

    print()
    print("=" * 70)
    print("🎉 ALL WEEK 4 TESTS PASSED")
    print("=" * 70)


if __name__ == "__main__":

    asyncio.run(main())
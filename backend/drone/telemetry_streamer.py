import asyncio

from backend.drone.secure_telemetry import SecureTelemetry


class TelemetryStreamer:
    """
    Continuously reads, encrypts,
    and sends telemetry.
    """

    def __init__(
        self,
        reader,
        secure_channel,
        ground_station
    ):

        self.reader = reader
        self.secure_channel = secure_channel
        self.ground_station = ground_station

    async def stream(
        self,
        interval=1
    ):

        print()
        print("Starting Live Secure Telemetry Stream...")
        print()

        while True:

            telemetry = await self.reader.read_telemetry()

            encrypted = self.secure_channel.encrypt(
                telemetry
            )

            response = self.ground_station.send(
                encrypted
            )

            print("--------------------------------")

            print("Packet Sent")

            print(response)

            await asyncio.sleep(
                interval
            )
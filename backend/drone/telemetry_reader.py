from mavsdk import System
from backend.communication.telemetry import Telemetry
from backend.drone.drone_state import DroneState

class TelemetryReader:
    """
    Reads live telemetry from the PX4 simulator.
    """

    def __init__(self, drone: System):
        self.drone = drone
        self.state = DroneState()

    async def read_position(self):
        """
        Read the current GPS position from PX4.
        """
        async for position in self.drone.telemetry.position():
            return position

    async def read_battery(self):
        """
        Read battery percentage from PX4.
        """
        async for battery in self.drone.telemetry.battery():
            percentage = battery.remaining_percent

            if percentage <= 1:
                percentage *= 100

            return round(percentage, 2)

    async def read_velocity(self):
        """
        Read NED velocity from PX4.
        """
        async for velocity in self.drone.telemetry.velocity_ned():
            return velocity

    async def read_attitude(self):
        """
        Read drone attitude from PX4.
        """
        async for attitude in self.drone.telemetry.attitude_euler():
            return attitude

    async def read_telemetry(self):
        """
        Read complete telemetry from PX4.
        """

        print("Reading position...")
        position = await self.read_position()

        print("Reading battery...")
        battery = await self.read_battery()

        print("Reading velocity...")
        velocity = await self.read_velocity()

        print("Reading attitude...")
        attitude = await self.read_attitude()

        print("Creating telemetry...")

        telemetry = Telemetry(
            latitude=position.latitude_deg,
            longitude=position.longitude_deg,
            altitude=position.relative_altitude_m,
            velocity=(
                velocity.north_m_s ** 2 +
                velocity.east_m_s ** 2 +
                velocity.down_m_s ** 2
            ) ** 0.5,
            battery=battery,
            pitch=round(attitude.pitch_deg, 2),
            roll=round(attitude.roll_deg, 2),
            yaw=round(attitude.yaw_deg, 2)
        )
        self.state.connected = True

        self.state.latitude = telemetry.latitude
        self.state.longitude = telemetry.longitude
        self.state.altitude = telemetry.altitude

        self.state.velocity = telemetry.velocity

        self.state.battery = telemetry.battery

        self.state.pitch = telemetry.pitch
        self.state.roll = telemetry.roll
        self.state.yaw = telemetry.yaw

        return telemetry
    def get_state(self):
        """
        Returns the latest drone state.
        """
        return self.state
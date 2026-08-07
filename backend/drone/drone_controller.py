import asyncio
from mavsdk import System


class DroneController:
    """
    Controls the PX4 drone.
    """

    def __init__(self, drone: System):
        self.drone = drone

    async def demo_mission(self):
        """
        Autonomous demo mission.
        """

        print()
        print("=" * 60)
        print("AUTONOMOUS DEMO MISSION")
        print("=" * 60)

        await asyncio.sleep(2)

        await self.arm()

        await asyncio.sleep(3)

        await self.takeoff()

        print("Hovering...")
        await asyncio.sleep(15)

        await self.land()

        print("Waiting for landing...")
        await asyncio.sleep(15)

        await self.disarm()

        print("✓ Mission Completed")

    async def arm(self):
        """
        Arm the drone.
        """

        print("Arming Drone...")

        await self.drone.action.arm()

        print("✓ Drone Armed")

    async def takeoff(self):
        """
        Take off the drone.
        """

        print("Setting Takeoff Altitude...")

        await self.drone.action.set_takeoff_altitude(5.0)

        print("Taking Off...")

        await self.drone.action.takeoff()

        print("✓ Takeoff Command Sent")

    async def land(self):
        """
        Land the drone.
        """

        print("Landing Drone...")

        await self.drone.action.land()

        print("✓ Landing Command Sent")

    async def disarm(self):
        """
        Disarm the drone.
        """

        print("Disarming Drone...")

        await self.drone.action.disarm()

        print("✓ Drone Disarmed")
import asyncio
import requests
from mavsdk import System


def update_mission(status):
    try:
        requests.post(
            "http://127.0.0.1:8000/mission/update",
            json={"status": status},
            timeout=2
        )
    except Exception:
        pass


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

        # ARM
        update_mission("ARMING")
        await self.arm()

        update_mission("ARMED")

        await asyncio.sleep(3)

        # TAKEOFF
        await self.takeoff()

        update_mission("TAKEOFF")

        print("Hovering...")
        update_mission("HOVERING")

        await asyncio.sleep(15)

        # LAND
        update_mission("LANDING")
        await self.land()

        print("Waiting for landing...")
        await asyncio.sleep(15)

        # DISARM
        await self.disarm()

        update_mission("COMPLETED")

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
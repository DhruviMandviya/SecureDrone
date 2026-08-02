from mavsdk import System


class PX4Connection:
    """
    Handles connection to the PX4 drone using MAVSDK.
    """

    def __init__(self):
        self.drone = System()

    async def connect(self):
        """
        Connect to the PX4 simulator.
        """

        print("Connecting to PX4...")

        await self.drone.connect(
            system_address="udpin://0.0.0.0:14540"
        )
        async for state in self.drone.core.connection_state():

            if state.is_connected:

                print("✓ Connected to PX4")

                break

        return self.drone
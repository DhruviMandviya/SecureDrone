from dataclasses import dataclass


@dataclass
class DroneState:
    """
    Represents the current state of the drone.
    """

    connected: bool = False
    armed: bool = False

    latitude: float = 0.0
    longitude: float = 0.0
    altitude: float = 0.0

    velocity: float = 0.0

    battery: float = 0.0

    pitch: float = 0.0
    roll: float = 0.0
    yaw: float = 0.0

    flight_mode: str = "UNKNOWN"
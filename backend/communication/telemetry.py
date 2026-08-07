from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Telemetry:

    timestamp: str

    latitude: float

    longitude: float

    altitude: float

    velocity: float

    battery: float

    pitch: float

    roll: float

    yaw: float

    gps_sats: int

    mode: str

    armed: bool

    def to_dict(self):
        return asdict(self)
    @classmethod
    def sample(cls):
        """
        Generate sample telemetry.
        """

        return cls(
            latitude=19.0760,
            longitude=72.8777,
            altitude=120.5,
            velocity=15.2,
            battery=87.4,
            pitch=2.3,
            roll=1.5,
            yaw=182.7
        )
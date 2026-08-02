from dataclasses import dataclass, asdict


@dataclass
class Telemetry:

    latitude: float

    longitude: float

    altitude: float

    velocity: float

    battery: float

    pitch: float

    roll: float

    yaw: float

    def to_dict(self):
        """
        Convert telemetry into dictionary.
        """

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
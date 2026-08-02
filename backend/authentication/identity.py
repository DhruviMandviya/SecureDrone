from dataclasses import dataclass

from backend.security.keypair import KeyPair
from backend.certificates.certificate import Certificate


@dataclass
class DeviceIdentity:
    """
    Represents the identity of a SecureDrone device.
    """

    device_id: str

    device_type: str

    keypair: KeyPair

    certificate: Certificate

    @classmethod
    def create(
        cls,
        device_id,
        device_type,
        certificate
    ):
        """
        Create a new device identity.
        """

        keys = KeyPair()

        keys.generate()

        return cls(
            device_id=device_id,
            device_type=device_type,
            keypair=keys,
            certificate=certificate
        )
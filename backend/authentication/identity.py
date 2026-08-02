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
        certificate_authority
    ):
        """
        Create a new device identity.
        """

        keys = KeyPair()

        keys.generate()

        certificate = certificate_authority.issue_certificate(
            device_id=device_id,
            device_type=device_type,
            public_key=keys.public_key
        )

        return cls(
            device_id=device_id,
            device_type=device_type,
            keypair=keys,
            certificate=certificate
        )
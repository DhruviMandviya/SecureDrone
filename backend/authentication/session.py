from dataclasses import dataclass

from backend.authentication.identity import DeviceIdentity


@dataclass
class SecureSession:
    """
    Represents an authenticated secure session.
    """

    identity: DeviceIdentity

    shared_secret: bytes

    session_key: bytes

    authenticated: bool = True

    @classmethod
    def create(
        cls,
        identity,
        shared_secret,
        session_key
    ):
        """
        Create a secure session.
        """

        return cls(
            identity=identity,
            shared_secret=shared_secret,
            session_key=session_key,
            authenticated=True
        )
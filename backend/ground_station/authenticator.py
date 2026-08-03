from backend.ground_station.session_manager import (
    SessionManager
)

from backend.ground_station.models import (
    AuthenticationResponse
)


class GroundStationAuthenticator:
    """
    Authenticates drones.
    """

    @staticmethod
    def authenticate(
        request,
        session
    ):

        SessionManager.create(
            request.device_id,
            session
        )

        return AuthenticationResponse(
            status="success",
            message="Drone Authenticated Successfully."
        )
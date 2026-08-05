from fastapi import APIRouter

from backend.ground_station.models import (
    AuthenticationRequest,
    EncryptedTelemetry
)

from backend.ground_station.receiver import (
    GroundStationReceiver
)

from backend.ground_station.authenticator import (
    GroundStationAuthenticator
)

from backend.ground_station.handshake_manager import (
    HandshakeManager
)

from backend.ground_station.models import (
    HandshakeCompleteRequest,
    HandshakeCompleteResponse
)
from backend.ground_station.session_manager import (
    SessionManager
)
from backend.ground_station.telemetry_store import (
    TelemetryStore
)
router = APIRouter()
handshake = HandshakeManager()
CURRENT_SESSION = None


@router.post("/authenticate")
async def authenticate(
    request: AuthenticationRequest
):

    global CURRENT_SESSION

    return GroundStationAuthenticator.authenticate(
        request,
        CURRENT_SESSION
    )

@router.post("/handshake/start")
async def handshake_start():

    public_key = handshake.start()

    return {
        "public_key": public_key.hex()
    }


@router.post("/handshake/complete")
async def handshake_complete(
    request: HandshakeCompleteRequest
):

    session_key = handshake.complete(
        bytes.fromhex(request.ciphertext)
    )

    class Session:

        def __init__(self, key):

            self.session_key = key

    session = Session(
        session_key
    )

    SessionManager.create(
        request.device_id,
        session
    )

    return HandshakeCompleteResponse(
        status="success"
    )

@router.post("/telemetry")
async def receive_telemetry(
    packet: EncryptedTelemetry
):

    return GroundStationReceiver.receive(
        packet
    )
@router.get("/telemetry/latest")
async def latest_telemetry():

    latest = TelemetryStore.latest()

    if latest is None:

        return {
            "status": "No Telemetry"
        }

    return latest
@router.get("/telemetry/history")
async def telemetry_history():

    return TelemetryStore.all()
@router.get("/sessions")
async def active_sessions():

    return {
        "active_sessions": SessionManager.all(),
        "count": len(
            SessionManager.all()
        )
    }
@router.get("/status")
async def system_status():

    latest = TelemetryStore.latest()

    return {
        "ground_station": "Running",
        "active_sessions": len(
            SessionManager.all()
        ),
        "telemetry_packets": len(
            TelemetryStore.all()
        ),
        "latest_available": latest is not None
    }
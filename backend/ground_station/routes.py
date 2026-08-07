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
from backend.ground_station.log_store import LogStore
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

    print(">>> HANDSHAKE START CALLED")

    public_key = handshake.start()

    return {
        "public_key": public_key.hex()
    }

@router.post("/handshake/complete")
async def handshake_complete(request: HandshakeCompleteRequest):

    print(">>> HANDSHAKE COMPLETE CALLED")
    print(request)

    session_key = handshake.complete(
        bytes.fromhex(request.ciphertext)
    )

    class Session:
        def __init__(self, key):
            self.session_key = key

    session = Session(session_key)

    print(">>> CREATING SESSION")

    SessionManager.create(
        request.device_id,
        session
    )

    print(">>> SESSION CREATED")

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


from fastapi.encoders import jsonable_encoder

@router.get("/telemetry/latest")
async def latest_telemetry():

    latest = TelemetryStore.latest()

    print("========== LATEST ==========")
    print(type(latest))
    print(latest)
    print("============================")

    if latest is None:
        return {"status": "No Telemetry"}

    return jsonable_encoder(latest)
@router.get("/telemetry/history")
async def telemetry_history():

    return TelemetryStore.all()
@router.get("/sessions")
async def active_sessions():

    sessions = []

    for info in SessionManager.all():

        sessions.append({
            "session_id": info.session_id,
            "active": info.active,
            "kem_algorithm": info.kem_algorithm,
            "cipher": info.cipher,
            "bytes_sent": info.bytes_sent,
            "bytes_received": info.bytes_received,
            "packets_dropped": info.packets_dropped,
            "established_at": info.established_at
        })

    return sessions
@router.get("/status")
async def system_status():

    latest = TelemetryStore.latest()

    return {
        "ground_station": "Running",
        "drone_connection": "connected" if latest else "disconnected",
        "telemetry_packets": len(TelemetryStore.all()),
        "latest_available": latest is not None,
        "active_sessions": len(SessionManager.all()),
        "link_quality": 98,
        "active_alarms": []
    }
@router.get("/logs")
async def logs():

    return LogStore.all()
from datetime import datetime
from zoneinfo import ZoneInfo


class SessionInfo:
    """
    Stores all information about an active secure session.
    """

    def __init__(self, device_id, session):
        self.device_id = device_id
        self.session = session

        self.session_id = device_id

        # Store IST time
        self.established_at = datetime.now(
            ZoneInfo("Asia/Kolkata")
        ).isoformat()

        self.kem_algorithm = "ML-KEM-768"
        self.cipher = "AES-256-GCM"

        self.bytes_sent = 0
        self.bytes_received = 0
        self.packets_dropped = 0

        self.active = True


class SessionManager:
    """
    Stores active drone sessions.
    """

    sessions = {}

    @classmethod
    def create(cls, device_id, session):

        cls.sessions[device_id] = SessionInfo(
            device_id,
            session
        )

        print(f"✓ Session Created : {device_id}")

    @classmethod
    def get(cls, device_id):

        info = cls.sessions.get(device_id)

        if info is None:
            return None

        return info.session

    @classmethod
    def get_info(cls, device_id):

        return cls.sessions.get(device_id)

    @classmethod
    def all(cls):

        return list(cls.sessions.values())
import json
import requests

from backend.ground_station.session_manager import SessionManager


class GroundStationClient:
    """
    Sends encrypted telemetry to the Ground Control Station.
    """

    def __init__(self, url="http://127.0.0.1:8000"):
        self.url = url

    def send(self, encrypted_packet, device_id="drone001"):

        payload = {
            "device_id": device_id,
            "nonce": encrypted_packet["nonce"],
            "ciphertext": encrypted_packet["ciphertext"],
            "tag": encrypted_packet["tag"],
        }

        # -------- Update Session Statistics --------
        session = SessionManager.get_info(device_id)

        if session is not None:
            packet_size = len(json.dumps(payload).encode())

            session.bytes_sent += packet_size
            session.bytes_received += packet_size

        # -------------------------------------------

        response = requests.post(
            f"{self.url}/telemetry",
            json=payload,
            timeout=5,
        )

        try:
            return response.json()

        except Exception:
            return {
                "status": "error",
                "code": response.status_code,
                "message": response.text,
            }
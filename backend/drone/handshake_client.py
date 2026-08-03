import requests


class HandshakeClient:
    """
    Performs ML-KEM handshake.
    """

    def __init__(
        self,
        url="http://127.0.0.1:8000"
    ):

        self.url = url

    def start(self):

        response = requests.post(
            f"{self.url}/handshake/start"
        )

        return response.json()

    def complete(
        self,
        device_id,
        ciphertext
    ):

        response = requests.post(

            f"{self.url}/handshake/complete",

            json={
                "device_id": device_id,
                "ciphertext": ciphertext.hex()
            }
        )

        return response.json()
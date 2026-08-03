import requests

from dataclasses import asdict


class AuthenticationClient:
    """
    Authenticates the drone with the
    Ground Control Station.
    """

    def __init__(
        self,
        url="http://127.0.0.1:8000"
    ):

        self.url = url

    def authenticate(
        self,
        identity,
        session=None
    ):

        payload = {

            "device_id":
                identity.device_id,

            "device_type":
                identity.device_type,

            "certificate":
                asdict(
                    identity.certificate
                )
        }

        response = requests.post(

            f"{self.url}/authenticate",

            json=payload
        )

        print()
        print("Ground Station Authentication")

        print(response.json())

        return response.json()
import os

from backend.certificates.serializer import (
    CertificateSerializer
)


class CertificateStore:

    def __init__(self):

        self.base_directory = os.path.dirname(
            os.path.abspath(__file__)
        )

        self.certificate_directory = os.path.join(
            self.base_directory,
            "data",
            "certs"
        )

        os.makedirs(
            self.certificate_directory,
            exist_ok=True
        )

    def save(self, certificate):

        file_path = os.path.join(

            self.certificate_directory,

            f"{certificate.device_id}.json"

        )

        with open(file_path, "w") as file:

            file.write(

                CertificateSerializer.to_json(
                    certificate
                )

            )

        print("✓ Certificate Saved")

    def load(self, device_id):

        file_path = os.path.join(

            self.certificate_directory,

            f"{device_id}.json"

        )

        with open(file_path, "r") as file:

            return CertificateSerializer.from_json(
                file.read()
            )
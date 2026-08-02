import json
from dataclasses import asdict

from backend.certificates.certificate import Certificate


class CertificateSerializer:

    @staticmethod
    def to_json(certificate: Certificate):
        """
        Convert Certificate object to JSON.
        """

        return json.dumps(
            asdict(certificate),
            indent=4
        )

    @staticmethod
    def from_json(json_string):
        """
        Convert JSON back to Certificate object.
        """

        data = json.loads(json_string)

        return Certificate(**data)
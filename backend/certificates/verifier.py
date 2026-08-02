import json
import base64
import oqs

from dataclasses import asdict


class CertificateVerifier:

    @staticmethod
    def verify(certificate, public_key):
        """
        Verify a signed certificate.
        """

        signature = base64.b64decode(
            certificate.signature
        )

        certificate.signature = ""

        certificate_data = json.dumps(
            asdict(certificate),
            sort_keys=True
        ).encode()

        with oqs.Signature(
            "ML-DSA-65"
        ) as verifier:

            result = verifier.verify(
                certificate_data,
                signature,
                public_key
            )

        certificate.signature = base64.b64encode(
            signature
        ).decode()

        return result
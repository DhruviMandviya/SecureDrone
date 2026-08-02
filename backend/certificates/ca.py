import os
import json
import base64
import oqs

from backend.certificates.certificate import (
    Certificate,
    create_certificate
)
from backend.security.keypair import KeyPair

from dataclasses import asdict

from backend.certificates.certificate import Certificate


class CertificateAuthority:
    """
    SecureDrone Root Certificate Authority
    """

    def __init__(self):

        self.algorithm = "ML-DSA-65"

        self.base_directory = os.path.dirname(
            os.path.abspath(__file__)
        )

        self.key_directory = os.path.join(
            self.base_directory,
            "data",
            "keys"
        )

        self.public_key_file = os.path.join(
            self.key_directory,
            "ca_public.key"
        )

        self.private_key_file = os.path.join(
            self.key_directory,
            "ca_private.key"
        )

        self.keys = KeyPair()

    def generate_keys(self):
        """
        Generate the Root CA key pair.
        """

        self.keys.generate()

        print("✓ CA Key Pair Generated")
    def save_keys(self):
        """
        Save the CA key pair to disk.
        """

        os.makedirs(self.key_directory, exist_ok=True)

        with open(self.public_key_file, "wb") as file:
            file.write(
                base64.b64encode(
                    self.keys.public_key
                )
            )

        with open(self.private_key_file, "wb") as file:
            file.write(
                base64.b64encode(
                    self.keys.private_key
                )
            )

        print("✓ CA Keys Saved Successfully")
    def load_keys(self):
        """
        Load the CA key pair from disk.
        """

        with open(self.public_key_file, "rb") as file:
            self.keys.public_key = base64.b64decode(
                file.read()
            )

        with open(self.private_key_file, "rb") as file:
            self.keys.private_key = base64.b64decode(
                file.read()
            )

        print("✓ CA Keys Loaded Successfully")
    def issue_certificate(
        self,
        device_id: str,
        device_type: str,
        public_key: bytes
    ):
        """
        Creates and signs a certificate.
        """

        certificate = create_certificate(
            device_id=device_id,
            device_type=device_type,
            public_key=base64.b64encode(
                public_key
            ).decode()
        )

        return self.sign_certificate(
            certificate
    )   
    def sign_certificate(self, certificate: Certificate):
        """
        Sign a certificate using the CA private key.
        """

        certificate.signature = ""

        certificate_data = json.dumps(
            asdict(certificate),
            sort_keys=True
        ).encode()

        with oqs.Signature(
            self.algorithm,
            secret_key=self.keys.private_key
        ) as signer:

            signature = signer.sign(
                certificate_data
            )

        certificate.signature = base64.b64encode(
            signature
        ).decode()

        print("✓ Certificate Signed")

        return certificate
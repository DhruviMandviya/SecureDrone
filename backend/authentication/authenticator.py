from backend.certificates.verifier import CertificateVerifier


class Authenticator:
    """
    Authenticates SecureDrone devices using certificates.
    """

    @staticmethod
    def authenticate(identity, ca_public_key):
        """
        Verify the device certificate.
        """

        valid = CertificateVerifier.verify(
            identity.certificate,
            ca_public_key
        )

        if valid:
            print("✓ Device Authenticated")
        else:
            print("✗ Authentication Failed")

        return valid
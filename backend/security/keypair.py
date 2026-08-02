import oqs


class KeyPair:
    """
    Generic ML-DSA Key Pair

    This class is reused by:
    - Certificate Authority
    - Drone
    - Ground Control Station
    """

    def __init__(self, algorithm="ML-DSA-65"):

        self.algorithm = algorithm

        self.public_key = None

        self.private_key = None

    def generate(self):
        """
        Generate a new ML-DSA key pair.
        """

        with oqs.Signature(self.algorithm) as signer:

            self.public_key = signer.generate_keypair()

            self.private_key = signer.export_secret_key()

        return self
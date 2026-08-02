from dataclasses import dataclass
import uuid
from datetime import datetime, timedelta
def create_certificate(
    device_id: str,
    device_type: str,
    public_key: str
):
    """
    Creates an unsigned certificate.
    """

    return Certificate(

        certificate_id=str(uuid.uuid4()),

        device_id=device_id,

        device_type=device_type,

        public_key=public_key,

        issued_by="SecureDrone Root CA",

        issued_at=datetime.utcnow().isoformat(),

        expires_at=(
            datetime.utcnow() +
            timedelta(days=365)
        ).isoformat(),

        signature=""
    )

@dataclass
class Certificate:
    """
    SecureDrone Certificate
    """

    certificate_id: str
    device_id: str
    device_type: str
    public_key: str
    issued_by: str
    issued_at: str
    expires_at: str
    signature: str = ""
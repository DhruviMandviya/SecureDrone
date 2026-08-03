from pydantic import BaseModel


class AuthenticationRequest(BaseModel):
    """
    Drone authentication request.
    """

    device_id: str

    device_type: str

    certificate: dict


class AuthenticationResponse(BaseModel):
    """
    Authentication response.
    """

    status: str

    message: str

class HandshakeResponse(BaseModel):
    """
    ML-KEM handshake response.
    """

    public_key: str


class HandshakeRequest(BaseModel):
    """
    Drone handshake request.
    """

    device_id: str

    ciphertext: str

class EncryptedTelemetry(BaseModel):
    """
    Encrypted telemetry packet.
    """

    device_id: str

    nonce: str

    ciphertext: str

    tag: str


class GroundStationResponse(BaseModel):
    """
    Telemetry response.
    """

    status: str

    message: str
class HandshakeStartResponse(BaseModel):

    public_key: str


class HandshakeCompleteRequest(BaseModel):

    device_id: str

    ciphertext: str


class HandshakeCompleteResponse(BaseModel):

    status: str
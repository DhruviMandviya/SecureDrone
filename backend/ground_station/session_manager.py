class SessionManager:
    """
    Stores active drone sessions.
    """

    sessions = {}

    @classmethod
    def create(
        cls,
        device_id,
        session
    ):

        cls.sessions[device_id] = session

        print(
            f"✓ Session Created : {device_id}"
        )

    @classmethod
    def get(
        cls,
        device_id
    ):

        return cls.sessions.get(
            device_id
        )
    @classmethod
    def all(cls):

        return list(
            cls.sessions.keys()
        )
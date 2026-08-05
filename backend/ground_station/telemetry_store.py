class TelemetryStore:
    """
    Stores recently received telemetry.
    """

    history = []

    MAX_HISTORY = 100

    @classmethod
    def add(
        cls,
        telemetry
    ):

        cls.history.append(
            telemetry
        )

        if len(cls.history) > cls.MAX_HISTORY:

            cls.history.pop(0)

    @classmethod
    def latest(
        cls
    ):

        if not cls.history:

            return None

        return cls.history[-1]

    @classmethod
    def all(
        cls
    ):

        return cls.history
class MissionStore:

    status = "CONNECTED"

    @classmethod
    def set(cls, status):
        cls.status = status

    @classmethod
    def get(cls):
        return cls.status
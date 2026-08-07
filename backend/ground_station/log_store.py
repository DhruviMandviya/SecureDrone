from datetime import datetime
from zoneinfo import ZoneInfo


class LogStore:

    logs = []

    @classmethod
    def add(cls, message, level="INFO"):

        cls.logs.append({
            "timestamp": datetime.now(
                ZoneInfo("Asia/Kolkata")
            ).isoformat(),
            "level": level,
            "message": message
        })

        cls.logs = cls.logs[-100:]

    @classmethod
    def all(cls):
        return cls.logs
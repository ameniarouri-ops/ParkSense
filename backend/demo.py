from datetime import datetime

from duration_module.manager import SessionManager
from duration_module.validation import ParkingDurationError


def at(hour, minute):
    return datetime(2026, 11, 24, hour, minute)


def try_it(title, action):
    print("\n---", title)

    try:
        print(action())

    except ParkingDurationError as error:
        print("Error:", error)


manager = SessionManager()

try_it(
    "10:00 registration for 120 minutes",
    lambda: manager.register(
        "123 TUN 4567",
        120,
        now=at(10, 0)
    )
)

try_it(
    "11:00 status",
    lambda: manager.get_status(
        "123 TUN 4567",
        now=at(11, 0)
    )
)

try_it(
    "12:15 status",
    lambda: manager.get_status(
        "123 TUN 4567",
        now=at(12, 15)
    )
)

try_it(
    "12:20 driver leaves",
    lambda: manager.close(
        "123 TUN 4567",
        now=at(12, 20)
    )
)

try_it(
    "Close unknown plate",
    lambda: manager.close(
        "999 TUN 1",
        now=at(10, 0)
    )
)
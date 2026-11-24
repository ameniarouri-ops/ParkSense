import json
from datetime import datetime

from duration_module import SessionManager, ParkingDurationError


def at(hour, minute):
    return datetime(2026, 11, 24, hour, minute)


def check(test_id, actual, expected):
    assert actual == expected, (
        f"{test_id} FAILED\n"
        f"Expected: {expected}\n"
        f"Actual:   {actual}"
    )
    print(f"{test_id}: PASS")


# One manager instance for all three vehicles
manager = SessionManager()

# L2-T01: Register vehicle A
a = manager.register("123 TUN 4567", 120, now=at(10, 0))
check("L2-T01", a["estimated_departure"], "2026-11-24T12:00:00")

# L2-T02: Register vehicle B
b = manager.register("222 TUN 2222", 60, now=at(10, 0))
check("L2-T02", b["estimated_departure"], "2026-11-24T11:00:00")

# L2-T03: Register vehicle C
c = manager.register("333 TUN 3333", 30, now=at(10, 0))
check("L2-T03", c["estimated_departure"], "2026-11-24T10:30:00")

# L2-T04: Check independent sessions at 10:15
expected_a = {
    "plate": "123 TUN 4567",
    "status": "ACTIVE",
    "start_time": "2026-11-24T10:00:00",
    "estimated_departure": "2026-11-24T12:00:00",
    "elapsed_minutes": 15,
    "remaining_minutes": 105,
    "overstay_minutes": 0,
}

expected_b = {
    "plate": "222 TUN 2222",
    "status": "ACTIVE",
    "start_time": "2026-11-24T10:00:00",
    "estimated_departure": "2026-11-24T11:00:00",
    "elapsed_minutes": 15,
    "remaining_minutes": 45,
    "overstay_minutes": 0,
}

expected_c = {
    "plate": "333 TUN 3333",
    "status": "ACTIVE",
    "start_time": "2026-11-24T10:00:00",
    "estimated_departure": "2026-11-24T10:30:00",
    "elapsed_minutes": 15,
    "remaining_minutes": 15,
    "overstay_minutes": 0,
}

check("L2-T04-A", manager.get_status("123 TUN 4567", now=at(10, 15)), expected_a)
check("L2-T04-B", manager.get_status("222 TUN 2222", now=at(10, 15)), expected_b)
check("L2-T04-C", manager.get_status("333 TUN 3333", now=at(10, 15)), expected_c)

# L2-T05: Vehicle C is 10 minutes overdue at 10:40
expected_overstay = {
    **expected_c,
    "status": "OVERSTAY",
    "elapsed_minutes": 40,
    "remaining_minutes": 0,
    "overstay_minutes": 10,
}

check(
    "L2-T05",
    manager.get_status("333 TUN 3333", now=at(10, 40)),
    expected_overstay,
)

# L2-T06: JSON serialization and deserialization
for plate in ("123 TUN 4567", "222 TUN 2222", "333 TUN 3333"):
    original = manager.get_status(plate, now=at(10, 15))

    assert all(type(v) in (str, int) for v in original.values())

    restored = json.loads(json.dumps(original))
    check(f"L2-T06-{plate}", restored, original)

# L2-T07: Close vehicle B at 10:45
expected_closed = {
    "plate": "222 TUN 2222",
    "status": "CLOSED",
    "start_time": "2026-11-24T10:00:00",
    "estimated_departure": "2026-11-24T11:00:00",
    "elapsed_minutes": 45,
    "remaining_minutes": 15,
    "overstay_minutes": 0,
    "outcome": "EARLY",
}

check(
    "L2-T07",
    manager.close("222 TUN 2222", now=at(10, 45)),
    expected_closed,
)

# L2-T08: A closed session cannot be retrieved as active
try:
    manager.get_status("222 TUN 2222", now=at(10, 50))
except ParkingDurationError as error:
    assert str(error) == "No active session for plate 222 TUN 2222."
    print("L2-T08: PASS")
else:
    raise AssertionError("L2-T08 FAILED: expected ParkingDurationError")

print("\nAll L2 contract tests passed.")

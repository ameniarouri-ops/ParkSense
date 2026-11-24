import json
from duration_module import SessionManager, ParkingDurationError
from datetime import datetime


def at(h, m):
    return datetime(2026, 11, 24, h, m)


m = SessionManager()

# 1. Results must convert to JSON (what a backend sends to the app)
result = m.register("123 TUN 4567", 120, now=at(10, 0))
print("JSON:", json.dumps(result))

# 2. Errors must carry a readable message the backend can forward
try:
    m.close("999 TUN 1", now=at(10, 5))
except ParkingDurationError as e:
    print("Error message to forward:", str(e))

# 3. Results are plain data: only text and integers
for key, value in result.items():
    assert isinstance(value, (str, int)), key
print("All values are plain text or integers: OK")

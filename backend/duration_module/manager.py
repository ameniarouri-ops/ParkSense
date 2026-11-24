from datetime import datetime, timedelta
from typing import Optional

from . import calculations as calc
from .session import ParkingSession
from .validation import (
    ParkingDurationError,
    normalize_plate,
    validate_duration,
)


class SessionManager:

    def __init__(self):
        self._active = {}
        self._closed = []

    def register(
        self,
        plate,
        duration_minutes,
        now: Optional[datetime] = None
    ) -> dict:

        now = now or datetime.now()

        plate = normalize_plate(plate)
        duration_minutes = validate_duration(duration_minutes)

        if plate in self._active:
            raise ParkingDurationError(
                f"Plate {plate} already has an active session."
            )

        session = ParkingSession(
            plate=plate,
            start_time=now,
            expected_duration=timedelta(
                minutes=duration_minutes
            ),
        )

        self._active[plate] = session

        return self._snapshot(session, now)

    def get_status(
        self,
        plate,
        now: Optional[datetime] = None
    ) -> dict:

        now = now or datetime.now()

        session = self._find_active(plate)

        return self._snapshot(session, now)

    def close(
        self,
        plate,
        now: Optional[datetime] = None
    ) -> dict:

        now = now or datetime.now()

        session = self._find_active(plate)

        session.end_time = now

        del self._active[session.plate]

        self._closed.append(session)

        result = self._snapshot(session, now)

        if now < session.estimated_departure:
            result["outcome"] = "EARLY"

        elif now > session.estimated_departure:
            result["outcome"] = "OVERSTAY"

        else:
            result["outcome"] = "ON_TIME"

        return result

    def _find_active(self, plate) -> ParkingSession:
        plate = normalize_plate(plate)

        if plate not in self._active:
            raise ParkingDurationError(
                f"No active session for plate {plate}."
            )

        return self._active[plate]

    def _snapshot(
        self,
        session: ParkingSession,
        now: datetime
    ) -> dict:

        over = calc.overstay(session, now)

        if not session.is_active:
            status = "CLOSED"

        elif over > timedelta(0):
            status = "OVERSTAY"

        else:
            status = "ACTIVE"

        return {
            "plate": session.plate,
            "status": status,
            "start_time": session.start_time.isoformat(
                timespec="seconds"
            ),
            "estimated_departure":
                session.estimated_departure.isoformat(
                    timespec="seconds"
                ),
            "elapsed_minutes": calc.minutes(
                calc.elapsed(session, now)
            ),
            "remaining_minutes": calc.minutes(
                calc.remaining(session, now)
            ),
            "overstay_minutes": calc.minutes(over),
        }
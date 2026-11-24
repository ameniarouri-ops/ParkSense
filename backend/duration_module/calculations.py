from datetime import datetime, timedelta

from .session import ParkingSession


def reference_time(
    session: ParkingSession,
    now: datetime
) -> datetime:
    if session.end_time is not None:
        return session.end_time

    return now


def elapsed(
    session: ParkingSession,
    now: datetime
) -> timedelta:
    duration = reference_time(session, now) - session.start_time

    return max(duration, timedelta(0))


def remaining(
    session: ParkingSession,
    now: datetime
) -> timedelta:
    duration = session.estimated_departure - reference_time(
        session, now
    )

    return max(duration, timedelta(0))


def overstay(
    session: ParkingSession,
    now: datetime
) -> timedelta:
    duration = reference_time(session, now) - session.estimated_departure

    return max(duration, timedelta(0))


def minutes(duration: timedelta) -> int:
    return int(duration.total_seconds() // 60)
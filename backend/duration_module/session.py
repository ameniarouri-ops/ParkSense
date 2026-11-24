from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class ParkingSession:
    plate: str
    start_time: datetime
    expected_duration: timedelta
    end_time: Optional[datetime] = None

    @property
    def estimated_departure(self) -> datetime:
        return self.start_time + self.expected_duration

    @property
    def is_active(self) -> bool:
        return self.end_time is None
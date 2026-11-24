class ParkingDurationError(Exception):
    """Raised when a parking request is invalid."""


MIN_DURATION_MINUTES = 1
MAX_DURATION_MINUTES = 24 * 60


def normalize_plate(plate) -> str:
    if not isinstance(plate, str) or not plate.strip():
        raise ParkingDurationError("Plate is required.")

    return " ".join(plate.upper().split())


def validate_duration(minutes):
    if isinstance(minutes, bool) or not isinstance(
        minutes, (int, float)
    ):
        raise ParkingDurationError(
            "Duration must be a number of minutes."
        )

    if not (
        MIN_DURATION_MINUTES
        <= minutes
        <= MAX_DURATION_MINUTES
    ):
        raise ParkingDurationError(
            f"Duration must be between "
            f"{MIN_DURATION_MINUTES} and "
            f"{MAX_DURATION_MINUTES} minutes."
        )

    return minutes
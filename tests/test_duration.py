
from datetime import datetime

from duration_module.manager import SessionManager
from duration_module.validation import ParkingDurationError


def at(hour, minute):
    return datetime(2026, 11, 24, hour, minute)


def expect_error(action):
    try:
        action()
    except ParkingDurationError:
        return

    raise AssertionError("Expected a ParkingDurationError")


def new_session(plate="123 TUN 4567", minutes=120):
    manager = SessionManager()
    manager.register(plate, minutes, now=at(10, 0))
    return manager


def test_estimated_departure():
    info = new_session().get_status(
        "123 TUN 4567", now=at(10, 0)
    )
    assert info["estimated_departure"] == "2026-11-24T12:00:00"


def test_elapsed_and_remaining():
    info = new_session().get_status(
        "123 TUN 4567", now=at(11, 0)
    )
    assert info["elapsed_minutes"] == 60
    assert info["remaining_minutes"] == 60


def test_exact_departure():
    info = new_session().get_status(
        "123 TUN 4567", now=at(12, 0)
    )
    assert info["remaining_minutes"] == 0
    assert info["overstay_minutes"] == 0


def test_overstay():
    info = new_session().get_status(
        "123 TUN 4567", now=at(12, 15)
    )
    assert info["status"] == "OVERSTAY"
    assert info["overstay_minutes"] == 15


def test_close_early():
    info = new_session().close(
        "123 TUN 4567", now=at(11, 30)
    )
    assert info["outcome"] == "EARLY"
    assert info["remaining_minutes"] == 30


def test_close_on_time():
    info = new_session().close(
        "123 TUN 4567", now=at(12, 0)
    )
    assert info["outcome"] == "ON_TIME"


def test_close_late():
    info = new_session().close(
        "123 TUN 4567", now=at(12, 20)
    )
    assert info["outcome"] == "OVERSTAY"
    assert info["overstay_minutes"] == 20


def test_plate_normalized():
    manager = SessionManager()
    manager.register("123  tun 4567 ", 60, now=at(10, 0))
    info = manager.get_status("123 TUN 4567", now=at(10, 5))
    assert info["plate"] == "123 TUN 4567"


def test_invalid_duration():
    for value in (0, -5, 1441, "abc", None, True):
        expect_error(
            lambda: SessionManager().register(
                "123 TUN 4567", value, now=at(10, 0)
            )
        )


def test_missing_plate():
    for plate in ("", "   ", None):
        expect_error(
            lambda: SessionManager().register(
                plate, 60, now=at(10, 0)
            )
        )


def test_duplicate_active_plate():
    expect_error(
        lambda: new_session().register(
            "123 tun 4567", 30, now=at(10, 5)
        )
    )


def test_unknown_plate():
    expect_error(
        lambda: SessionManager().close(
            "999 TUN 1", now=at(10, 0)
        )
    )


def test_reregister_after_close():
    manager = new_session()
    manager.close("123 TUN 4567", now=at(11, 0))
    manager.register("123 TUN 4567", 30, now=at(13, 0))


def test_status_after_close():
    manager = new_session()
    manager.close("123 TUN 4567", now=at(11, 0))
    expect_error(
        lambda: manager.get_status(
            "123 TUN 4567", now=at(11, 5)
        )
    )


if __name__ == "__main__":
    tests = [
        function
        for name, function in globals().copy().items()
        if name.startswith("test_")
    ]

    for test in tests:
        test()
        print("PASS", test.__name__)

    print(f"All {len(tests)} tests passed")

# Parking Duration Module: interface sheet

Pure Python, no dependencies. It only measures parking time. It does not use
MQTT, the ESP32 or the car counter, and it does not decide whether the parking
is full.

## How to use it
    from duration_module import SessionManager, ParkingDurationError
    manager = SessionManager()      # create ONE instance and keep it alive

Sessions are kept in memory: they disappear when the program restarts.
Permanent storage is the backend's decision.

## Functions
| Function | Called when | Input | Returns |
|---|---|---|---|
| register(plate, duration_minutes) | Driver submits plate + duration | plate (text), minutes (number, 1 to 1440) | status dictionary |
| get_status(plate) | App asks for remaining time | plate | status dictionary |
| close(plate) | Driver taps "I'm leaving" | plate | status dictionary + "outcome" |

## Status dictionary (only text and integers, ready for JSON)
- plate: normalized plate (uppercase, single spaces)
- status: ACTIVE, OVERSTAY or CLOSED
- start_time, estimated_departure: ISO text, e.g. 2026-11-24T12:00:00
- elapsed_minutes, remaining_minutes, overstay_minutes: integers
- outcome (only from close): EARLY, ON_TIME or OVERSTAY

## Errors
Every refusal raises ParkingDurationError with a readable message:
- missing plate, invalid duration, plate already has an active session,
  no active session for that plate (also after it was closed).

## Notes
- Start time = moment register() is called (server clock).
- Times are server-local, without timezone.
- Overstay is detected when status is requested; the module sends no alerts.

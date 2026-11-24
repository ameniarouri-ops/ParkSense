# Integration Test Plan: Parking Duration Module

Author: Amani (Hardware + Parking Duration Module)
Status: L1 and L2 completed; L3 and L4 pending

## 1. Objective
Prove that the parking-duration module behaves as described in INTERFACE.md,
first on its own, then when called by the team's backend, then in the complete
Smart Parking system.

## 2. Scope
In scope:
- Registering a session, reading its status, closing it.
- Time calculations: estimated departure, elapsed, remaining, overstay.
- Input validation and error messages.
- Format of results (JSON-compatible dictionaries).

Out of scope (belongs to teammates):
- Car counter, barriers, MQTT parking status (Rym)
- MQTT broker, backend, database, endpoints (Baraa)
- Mobile screens (Farah)

## 3. Test levels
| Level | Description | Depends on | Status |
|---|---|---|---|
| L1 Module | Logic tests (test_duration.py, 14 tests) | nothing | DONE |
| L2 Contract | Fake caller, three vehicles, JSON round trip | nothing | DONE (12/12 checks) |
| L3 Backend integration | Baraa's backend calls the module | Baraa | WAITING |
| L4 End to end | App + backend + MQTT + ESP32 together | Baraa, Farah, Rym | WAITING |

## 4. Test environment
- Python 3.12, Windows, run with: py &lt;file&gt;
- Fake times (the now parameter), so tests do not depend on the real clock.
- Sessions in memory only (no database).

## 5. Entry criteria (when a level can start)
- L2: module passes L1.
- L3: Baraa's backend code available and the module copied in.
- L4: L3 passed, and the app and ESP32 firmware available.

## 6. Pass / fail rule
A test passes only if the actual result equals the expected result written
BEFORE running it. Any difference is recorded as a defect (see section 8).

## 7. Test case format
ID | Level | Scenario | Preconditions | Steps | Expected result | Needs teammate | Status
(test cases are added in the next steps)

## 8. Defect log
ID | Found in | Description | Whose component | Status
(empty for now)

## 9. Dependencies on teammates
(listed in a later step, once the integration points are defined)


## 10. L2 execution results

- Test file: test_contract.py
- Python version: 3.12.4
- Execution count: 2
- Result: PASS on both executions
- Checks passed: 12
- Checks failed: 0

### Tested scenarios

| Test ID | Scenario | Result |
|---|---|---|
| L2-T01 | Register vehicle A | PASS |
| L2-T02 | Register vehicle B | PASS |
| L2-T03 | Register vehicle C | PASS |
| L2-T04-A | Independent status of vehicle A | PASS |
| L2-T04-B | Independent status of vehicle B | PASS |
| L2-T04-C | Independent status of vehicle C | PASS |
| L2-T05 | Overstay detection | PASS |
| L2-T06 | JSON round trip for three vehicles | PASS (3 checks) |
| L2-T07 | Close vehicle B early | PASS |
| L2-T08 | Reject lookup of closed vehicle | PASS |

No defects identified during L2 execution.


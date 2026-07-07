import json

import pytest

from oomwoo_recovery_safety.core import ControllerState, DecisionKind, RecoveryController, Situation


def test_bumper_recovery_escalates_and_terminates():
    controller = RecoveryController()

    decision = controller.trigger(Situation.BUMPER_LEFT)
    assert decision.kind == DecisionKind.START_STEP
    assert decision.step.name == "back_up"

    seen = [decision.step.name]
    for _ in range(10):
        decision = controller.step_failed("test failure")
        if decision.kind == DecisionKind.START_STEP:
            seen.append(decision.step.name)
            continue
        break

    assert seen == [
        "back_up",
        "rotate_away_from_left_bumper",
        "wiggle_free",
        "clear_costmap",
    ]
    assert controller.state == ControllerState.PAUSED
    assert controller.last_status.reason_code == "RECOVERY_EXHAUSTED"
    assert controller.last_status.recoverable is True


def test_success_stops_ladder():
    controller = RecoveryController()
    controller.trigger("bumper_front")

    decision = controller.step_succeeded()

    assert decision.kind == DecisionKind.STATUS_ONLY
    assert controller.state == ControllerState.RECOVERED
    assert controller.last_status.reason_code == "RECOVERED"


@pytest.mark.parametrize(
    ("situation", "reason"),
    [
        (Situation.E_STOP, "E_STOP"),
        (Situation.CLIFF, "SAFETY_CLIFF"),
        (Situation.WHEEL_DROP, "SAFETY_WHEEL_DROP"),
        (Situation.PICKUP, "SAFETY_PICKUP"),
    ],
)
def test_safety_events_pause_immediately(situation, reason):
    controller = RecoveryController()

    decision = controller.trigger(situation)

    assert decision.kind == DecisionKind.STATUS_ONLY
    assert controller.state == ControllerState.PAUSED
    assert controller.last_status.reason_code == reason
    assert controller.last_status.recoverable is False


def test_duplicate_trigger_is_ignored_while_recovering():
    controller = RecoveryController()
    controller.trigger(Situation.BUMPER_RIGHT)

    decision = controller.trigger(Situation.WEDGED)

    assert decision.kind == DecisionKind.IGNORED
    assert controller.state == ControllerState.RECOVERING
    assert controller.last_status.reason_code == "RECOVERY_ALREADY_ACTIVE"


def test_reset_returns_to_idle_after_pause():
    controller = RecoveryController()
    controller.trigger(Situation.E_STOP)

    decision = controller.reset()

    assert decision.kind == DecisionKind.STATUS_ONLY
    assert controller.state == ControllerState.IDLE
    assert controller.last_status.reason_code == "READY"


def test_paused_controller_ignores_new_recovery_until_reset():
    controller = RecoveryController()
    controller.trigger(Situation.E_STOP)

    decision = controller.trigger(Situation.BUMPER_LEFT)

    assert decision.kind == DecisionKind.IGNORED
    assert controller.state == ControllerState.PAUSED
    assert controller.last_status.reason_code == "RECOVERY_PAUSED"


def test_status_json_shape():
    controller = RecoveryController()
    controller.trigger(Situation.NO_VALID_PATH)

    payload = json.loads(controller.last_status.to_json())

    assert payload["state"] == "recovering"
    assert payload["reason_code"] == "RECOVERY_STARTED"
    assert payload["recoverable"] is True
    assert payload["source"] == "oomwoo_recovery_safety"
    assert payload["situation"] == "no_valid_path"
    assert payload["behavior"] == "clear_costmap"

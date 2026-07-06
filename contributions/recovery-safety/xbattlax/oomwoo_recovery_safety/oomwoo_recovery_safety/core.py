from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
import json
from typing import Mapping


class Situation(str, Enum):
    BUMPER_LEFT = "bumper_left"
    BUMPER_RIGHT = "bumper_right"
    BUMPER_FRONT = "bumper_front"
    WEDGED = "wedged"
    NO_VALID_PATH = "no_valid_path"
    LOCALIZATION_LOST = "localization_lost"
    CLIFF = "cliff"
    WHEEL_DROP = "wheel_drop"
    PICKUP = "pickup"
    E_STOP = "e_stop"


class ControllerState(str, Enum):
    IDLE = "idle"
    RECOVERING = "recovering"
    RECOVERED = "recovered"
    PAUSED = "paused"


class DecisionKind(str, Enum):
    START_STEP = "start_step"
    STATUS_ONLY = "status_only"
    IGNORED = "ignored"


@dataclass(frozen=True)
class RecoveryStep:
    name: str
    command: str
    duration_sec: float
    linear_x: float = 0.0
    angular_z: float = 0.0


@dataclass(frozen=True)
class RecoveryStatus:
    state: str
    reason_code: str
    message: str
    recoverable: bool
    source: str = "oomwoo_recovery_safety"
    situation: str | None = None
    behavior: str | None = None
    step_index: int | None = None
    ladder_length: int | None = None

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True)


@dataclass(frozen=True)
class Decision:
    kind: DecisionKind
    status: RecoveryStatus
    step: RecoveryStep | None = None


SAFETY_SITUATIONS = {
    Situation.CLIFF,
    Situation.WHEEL_DROP,
    Situation.PICKUP,
    Situation.E_STOP,
}


DEFAULT_LADDERS: Mapping[Situation, tuple[RecoveryStep, ...]] = {
    Situation.BUMPER_LEFT: (
        RecoveryStep("back_up", "twist", 0.8, linear_x=-0.12),
        RecoveryStep("rotate_away_from_left_bumper", "twist", 1.0, linear_x=-0.06, angular_z=-0.55),
        RecoveryStep("wiggle_free", "twist", 0.7, linear_x=-0.04, angular_z=0.85),
        RecoveryStep("clear_costmap", "clear_costmap", 0.1),
    ),
    Situation.BUMPER_RIGHT: (
        RecoveryStep("back_up", "twist", 0.8, linear_x=-0.12),
        RecoveryStep("rotate_away_from_right_bumper", "twist", 1.0, linear_x=-0.06, angular_z=0.55),
        RecoveryStep("wiggle_free", "twist", 0.7, linear_x=-0.04, angular_z=-0.85),
        RecoveryStep("clear_costmap", "clear_costmap", 0.1),
    ),
    Situation.BUMPER_FRONT: (
        RecoveryStep("back_up", "twist", 0.9, linear_x=-0.14),
        RecoveryStep("rotate_left", "twist", 0.8, angular_z=0.6),
        RecoveryStep("rotate_right", "twist", 0.8, angular_z=-0.6),
        RecoveryStep("clear_costmap", "clear_costmap", 0.1),
    ),
    Situation.WEDGED: (
        RecoveryStep("back_up", "twist", 1.0, linear_x=-0.12),
        RecoveryStep("wiggle_left", "twist", 0.6, linear_x=-0.04, angular_z=0.9),
        RecoveryStep("wiggle_right", "twist", 0.6, linear_x=-0.04, angular_z=-0.9),
        RecoveryStep("rotate_in_place", "twist", 1.2, angular_z=0.7),
        RecoveryStep("clear_costmap", "clear_costmap", 0.1),
    ),
    Situation.NO_VALID_PATH: (
        RecoveryStep("clear_costmap", "clear_costmap", 0.1),
        RecoveryStep("nudge_reverse", "twist", 0.6, linear_x=-0.08),
        RecoveryStep("rotate_in_place", "twist", 1.0, angular_z=0.6),
    ),
    Situation.LOCALIZATION_LOST: (
        RecoveryStep("stop_and_wait", "stop", 0.1),
        RecoveryStep("rotate_to_collect_scans", "twist", 1.5, angular_z=0.45),
    ),
}


class RecoveryController:
    def __init__(self, ladders: Mapping[Situation, tuple[RecoveryStep, ...]] | None = None):
        self._ladders = dict(ladders or DEFAULT_LADDERS)
        self._state = ControllerState.IDLE
        self._situation: Situation | None = None
        self._step_index = 0
        self._current_step: RecoveryStep | None = None
        self._last_status = self._make_status("READY", "Recovery controller ready", True)

    @property
    def state(self) -> ControllerState:
        return self._state

    @property
    def last_status(self) -> RecoveryStatus:
        return self._last_status

    def trigger(self, situation: Situation | str) -> Decision:
        parsed = self._parse_situation(situation)

        if parsed in SAFETY_SITUATIONS:
            return self._pause(
                parsed,
                reason_code=self._safety_reason(parsed),
                message=f"Safety event {parsed.value} paused the robot",
                recoverable=False,
            )

        if self._state == ControllerState.RECOVERING:
            status = self._make_status(
                "RECOVERY_ALREADY_ACTIVE",
                f"Ignoring {parsed.value}; already recovering from {self._situation.value}",
                True,
            )
            self._last_status = status
            return Decision(DecisionKind.IGNORED, status)

        if self._state == ControllerState.PAUSED:
            status = self._make_status(
                "RECOVERY_PAUSED",
                f"Ignoring {parsed.value}; controller is paused and needs reset",
                self._last_status.recoverable,
            )
            self._last_status = status
            return Decision(DecisionKind.IGNORED, status)

        ladder = self._ladders.get(parsed)
        if not ladder:
            return self._pause(
                parsed,
                reason_code="NO_RECOVERY_LADDER",
                message=f"No recovery ladder configured for {parsed.value}",
                recoverable=True,
            )

        self._state = ControllerState.RECOVERING
        self._situation = parsed
        self._step_index = 0
        self._current_step = ladder[0]
        status = self._make_status(
            "RECOVERY_STARTED",
            f"Starting recovery step {self._current_step.name}",
            True,
        )
        self._last_status = status
        return Decision(DecisionKind.START_STEP, status, self._current_step)

    def step_succeeded(self) -> Decision:
        if self._state != ControllerState.RECOVERING:
            status = self._make_status("NO_ACTIVE_RECOVERY", "No active recovery to complete", True)
            self._last_status = status
            return Decision(DecisionKind.IGNORED, status)

        self._state = ControllerState.RECOVERED
        self._current_step = None
        status = self._make_status("RECOVERED", "Recovery succeeded", True)
        self._last_status = status
        return Decision(DecisionKind.STATUS_ONLY, status)

    def step_failed(self, detail: str = "step failed") -> Decision:
        if self._state != ControllerState.RECOVERING or self._situation is None:
            status = self._make_status("NO_ACTIVE_RECOVERY", "No active recovery to fail", True)
            self._last_status = status
            return Decision(DecisionKind.IGNORED, status)

        ladder = self._ladders[self._situation]
        next_index = self._step_index + 1
        if next_index >= len(ladder):
            return self._pause(
                self._situation,
                reason_code="RECOVERY_EXHAUSTED",
                message=f"Recovery ladder exhausted after {detail}",
                recoverable=True,
            )

        self._step_index = next_index
        self._current_step = ladder[next_index]
        status = self._make_status(
            "RECOVERY_ESCALATED",
            f"Escalating after {detail}; starting {self._current_step.name}",
            True,
        )
        self._last_status = status
        return Decision(DecisionKind.START_STEP, status, self._current_step)

    def reset(self) -> Decision:
        self._state = ControllerState.IDLE
        self._situation = None
        self._step_index = 0
        self._current_step = None
        status = self._make_status("READY", "Recovery controller reset", True)
        self._last_status = status
        return Decision(DecisionKind.STATUS_ONLY, status)

    def _pause(
        self,
        situation: Situation,
        *,
        reason_code: str,
        message: str,
        recoverable: bool,
    ) -> Decision:
        self._state = ControllerState.PAUSED
        self._situation = situation
        self._current_step = None
        status = self._make_status(reason_code, message, recoverable)
        self._last_status = status
        return Decision(DecisionKind.STATUS_ONLY, status)

    def _make_status(self, reason_code: str, message: str, recoverable: bool) -> RecoveryStatus:
        ladder_length = None
        if self._situation in self._ladders:
            ladder_length = len(self._ladders[self._situation])

        return RecoveryStatus(
            state=self._state.value,
            reason_code=reason_code,
            message=message,
            recoverable=recoverable,
            situation=self._situation.value if self._situation else None,
            behavior=self._current_step.name if self._current_step else None,
            step_index=self._step_index if self._current_step else None,
            ladder_length=ladder_length,
        )

    @staticmethod
    def _parse_situation(situation: Situation | str) -> Situation:
        if isinstance(situation, Situation):
            return situation
        try:
            return Situation(str(situation).strip().lower())
        except ValueError as exc:
            raise ValueError(f"Unknown recovery situation: {situation}") from exc

    @staticmethod
    def _safety_reason(situation: Situation) -> str:
        if situation == Situation.E_STOP:
            return "E_STOP"
        return f"SAFETY_{situation.value.upper()}"

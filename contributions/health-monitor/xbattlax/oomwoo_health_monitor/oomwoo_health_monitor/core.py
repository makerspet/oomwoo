from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from typing import Iterable


HEALTHY_LEVELS = {"ok", "healthy"}


@dataclass(frozen=True)
class ComponentSpec:
    component_id: str
    critical: bool = True
    max_age_sec: float = 0.5

    def __post_init__(self):
        if not self.component_id:
            raise ValueError("component_id is required")
        if self.max_age_sec <= 0.0:
            raise ValueError("max_age_sec must be positive")


@dataclass(frozen=True)
class HealthRoster:
    task_id: str
    components: tuple[ComponentSpec, ...]

    def __post_init__(self):
        if not self.task_id:
            raise ValueError("task_id is required")
        ids = [component.component_id for component in self.components]
        if len(ids) != len(set(ids)):
            raise ValueError("component ids must be unique")

    @classmethod
    def from_components(
        cls,
        task_id: str,
        components: Iterable[ComponentSpec],
    ) -> "HealthRoster":
        return cls(task_id, tuple(components))

    @property
    def by_id(self) -> dict[str, ComponentSpec]:
        return {component.component_id: component for component in self.components}


@dataclass(frozen=True)
class ComponentHeartbeat:
    component_id: str
    health: str
    stamp_sec: float
    detail: str = ""
    sequence: int | None = None

    @property
    def is_well(self) -> bool:
        return self.health.strip().lower() in HEALTHY_LEVELS


@dataclass(frozen=True)
class StackHealth:
    state: str
    task_id: str | None
    emit_mcu_heartbeat: bool
    missing_critical: tuple[str, ...] = ()
    stale_critical: tuple[str, ...] = ()
    unhealthy_critical: tuple[str, ...] = ()
    advisory_faults: tuple[str, ...] = ()
    healthy_for_sec: float = 0.0
    source: str = "oomwoo_health_monitor"

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True)


class HealthAggregator:
    def __init__(self, *, arm_window_sec: float = 0.25):
        if arm_window_sec < 0.0:
            raise ValueError("arm_window_sec must be non-negative")
        self._arm_window_sec = arm_window_sec
        self._roster: HealthRoster | None = None
        self._heartbeats: dict[str, ComponentHeartbeat] = {}
        self._healthy_since_sec: float | None = None

    @property
    def roster(self) -> HealthRoster | None:
        return self._roster

    def update_roster(self, roster: HealthRoster):
        old_task = self._roster.task_id if self._roster else None
        old_ids = set(self._roster.by_id) if self._roster else set()
        new_ids = set(roster.by_id)
        self._roster = roster
        self._heartbeats = {
            component_id: heartbeat
            for component_id, heartbeat in self._heartbeats.items()
            if component_id in new_ids
        }
        if old_task != roster.task_id or old_ids != new_ids:
            self._healthy_since_sec = None

    def update_heartbeat(self, heartbeat: ComponentHeartbeat):
        self._heartbeats[heartbeat.component_id] = heartbeat

    def evaluate(self, now_sec: float) -> StackHealth:
        if self._roster is None:
            self._healthy_since_sec = None
            return StackHealth(
                state="no_roster",
                task_id=None,
                emit_mcu_heartbeat=False,
            )

        missing: list[str] = []
        stale: list[str] = []
        unhealthy: list[str] = []
        advisory_faults: list[str] = []

        for component_id, spec in self._roster.by_id.items():
            heartbeat = self._heartbeats.get(component_id)
            if heartbeat is None:
                if spec.critical:
                    missing.append(component_id)
                else:
                    advisory_faults.append(component_id)
                continue

            age_sec = now_sec - heartbeat.stamp_sec
            if age_sec < 0.0 or age_sec > spec.max_age_sec:
                if spec.critical:
                    stale.append(component_id)
                else:
                    advisory_faults.append(component_id)
                continue

            if not heartbeat.is_well:
                if spec.critical:
                    unhealthy.append(component_id)
                else:
                    advisory_faults.append(component_id)

        if missing or stale or unhealthy:
            self._healthy_since_sec = None
            return StackHealth(
                state="fault",
                task_id=self._roster.task_id,
                emit_mcu_heartbeat=False,
                missing_critical=tuple(sorted(missing)),
                stale_critical=tuple(sorted(stale)),
                unhealthy_critical=tuple(sorted(unhealthy)),
                advisory_faults=tuple(sorted(advisory_faults)),
            )

        if self._healthy_since_sec is None:
            self._healthy_since_sec = now_sec

        healthy_for_sec = now_sec - self._healthy_since_sec
        if healthy_for_sec < self._arm_window_sec:
            return StackHealth(
                state="arming",
                task_id=self._roster.task_id,
                emit_mcu_heartbeat=False,
                advisory_faults=tuple(sorted(advisory_faults)),
                healthy_for_sec=healthy_for_sec,
            )

        return StackHealth(
            state="healthy" if not advisory_faults else "healthy_with_advisory_faults",
            task_id=self._roster.task_id,
            emit_mcu_heartbeat=True,
            advisory_faults=tuple(sorted(advisory_faults)),
            healthy_for_sec=healthy_for_sec,
        )

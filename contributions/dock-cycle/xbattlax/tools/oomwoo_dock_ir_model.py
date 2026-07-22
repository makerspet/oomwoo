from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from math import atan2, cos, hypot, pi, sin
from typing import Iterable


def normalize_angle_rad(angle: float) -> float:
    return atan2(sin(angle), cos(angle))


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


@dataclass(frozen=True)
class Pose2D:
    x: float
    y: float
    yaw: float = 0.0

    def transform(self, local: "Pose2D") -> "Pose2D":
        c = cos(self.yaw)
        s = sin(self.yaw)
        return Pose2D(
            self.x + c * local.x - s * local.y,
            self.y + s * local.x + c * local.y,
            normalize_angle_rad(self.yaw + local.yaw),
        )


@dataclass(frozen=True)
class CircleObstacle:
    x: float
    y: float
    radius: float


@dataclass(frozen=True)
class ReceiverSpec:
    name: str
    pose: Pose2D
    fov_rad: float
    max_range_m: float
    gain: float = 1.0
    min_range_m: float = 0.08
    reference_range_m: float = 1.0
    angular_exponent: float = 2.0


@dataclass(frozen=True)
class DockSpec:
    pose: Pose2D = field(default_factory=lambda: Pose2D(0.0, 0.0, 0.0))
    beacon_offset: Pose2D = field(default_factory=lambda: Pose2D(0.0, 0.0, 0.0))

    @property
    def beacon_pose(self) -> Pose2D:
        return self.pose.transform(self.beacon_offset)


@dataclass(frozen=True)
class IrReading:
    receiver: str
    visible: bool
    strength: float
    range_m: float
    bearing_in_base_rad: float
    off_axis_rad: float


@dataclass(frozen=True)
class DockIrFrame:
    mode: str
    angular_z_hint: float
    front_error: float
    search_error: float
    readings: tuple[IrReading, ...]

    def reading(self, name: str) -> IrReading:
        for item in self.readings:
            if item.receiver == name:
                return item
        raise KeyError(name)

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True)


DEFAULT_RECEIVERS: tuple[ReceiverSpec, ...] = (
    ReceiverSpec(
        "front_left",
        Pose2D(0.16, 0.035, 0.0),
        fov_rad=0.70,
        max_range_m=2.0,
        angular_exponent=8.0,
    ),
    ReceiverSpec(
        "front_right",
        Pose2D(0.16, -0.035, 0.0),
        fov_rad=0.70,
        max_range_m=2.0,
        angular_exponent=8.0,
    ),
    ReceiverSpec(
        "search_left",
        Pose2D(0.00, 0.12, pi / 2.0),
        fov_rad=3.00,
        max_range_m=3.5,
        gain=0.7,
    ),
    ReceiverSpec(
        "search_right",
        Pose2D(0.00, -0.12, -pi / 2.0),
        fov_rad=3.00,
        max_range_m=3.5,
        gain=0.7,
    ),
)


def compute_homing_frame(
    robot_pose: Pose2D,
    dock: DockSpec | None = None,
    *,
    receivers: Iterable[ReceiverSpec] = DEFAULT_RECEIVERS,
    obstacles: Iterable[CircleObstacle] = (),
    minimum_signal: float = 0.02,
    centered_error: float = 0.04,
) -> DockIrFrame:
    dock = dock or DockSpec()
    receiver_tuple = tuple(receivers)
    obstacle_tuple = tuple(obstacles)
    readings = tuple(
        _receiver_reading(robot_pose, dock, receiver, obstacle_tuple)
        for receiver in receiver_tuple
    )

    strengths = {reading.receiver: reading.strength for reading in readings}
    front_left = strengths.get("front_left", 0.0)
    front_right = strengths.get("front_right", 0.0)
    search_left = strengths.get("search_left", 0.0)
    search_right = strengths.get("search_right", 0.0)

    front_error = _normalized_difference(front_left, front_right, minimum_signal)
    search_error = _normalized_difference(search_left, search_right, minimum_signal)
    front_total = front_left + front_right
    search_total = search_left + search_right

    if front_total >= minimum_signal:
        if abs(front_error) <= centered_error:
            mode = "final_centered"
        elif front_error > 0.0:
            mode = "final_turn_left"
        else:
            mode = "final_turn_right"
        angular_z_hint = clamp(front_error, -1.0, 1.0)
    elif search_total >= minimum_signal:
        mode = "search_turn_left" if search_error > 0.0 else "search_turn_right"
        angular_z_hint = clamp(search_error, -1.0, 1.0)
    else:
        mode = "search_pattern"
        angular_z_hint = 0.0

    return DockIrFrame(
        mode=mode,
        angular_z_hint=angular_z_hint,
        front_error=front_error,
        search_error=search_error,
        readings=readings,
    )


def _receiver_reading(
    robot_pose: Pose2D,
    dock: DockSpec,
    receiver: ReceiverSpec,
    obstacles: tuple[CircleObstacle, ...],
) -> IrReading:
    receiver_world = robot_pose.transform(receiver.pose)
    beacon_world = dock.beacon_pose
    dx = beacon_world.x - receiver_world.x
    dy = beacon_world.y - receiver_world.y
    range_m = hypot(dx, dy)
    bearing_world = atan2(dy, dx)
    off_axis = normalize_angle_rad(bearing_world - receiver_world.yaw)
    bearing_in_base = normalize_angle_rad(bearing_world - robot_pose.yaw)

    visible = (
        range_m <= receiver.max_range_m
        and abs(off_axis) <= receiver.fov_rad / 2.0
        and not _blocked(receiver_world, beacon_world, obstacles)
    )
    if not visible:
        return IrReading(
            receiver.name,
            False,
            0.0,
            range_m,
            bearing_in_base,
            off_axis,
        )

    angular_gain = max(0.0, cos(off_axis)) ** receiver.angular_exponent
    effective_range = max(range_m, receiver.min_range_m)
    range_gain = min(1.0, (receiver.reference_range_m / effective_range) ** 2)
    strength = receiver.gain * angular_gain * range_gain
    return IrReading(
        receiver.name,
        True,
        strength,
        range_m,
        bearing_in_base,
        off_axis,
    )


def _normalized_difference(left: float, right: float, minimum_signal: float) -> float:
    total = left + right
    if total < minimum_signal:
        return 0.0
    return (left - right) / total


def _blocked(start: Pose2D, end: Pose2D, obstacles: tuple[CircleObstacle, ...]) -> bool:
    return any(_segment_hits_circle(start, end, obstacle) for obstacle in obstacles)


def _segment_hits_circle(start: Pose2D, end: Pose2D, obstacle: CircleObstacle) -> bool:
    sx = start.x
    sy = start.y
    ex = end.x
    ey = end.y
    vx = ex - sx
    vy = ey - sy
    length_sq = vx * vx + vy * vy
    if length_sq == 0.0:
        return False

    t = ((obstacle.x - sx) * vx + (obstacle.y - sy) * vy) / length_sq
    if t <= 0.0 or t >= 1.0:
        return False

    closest_x = sx + t * vx
    closest_y = sy + t * vy
    return hypot(closest_x - obstacle.x, closest_y - obstacle.y) <= obstacle.radius

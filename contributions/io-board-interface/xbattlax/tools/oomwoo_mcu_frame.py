#!/usr/bin/env python3
"""Reference frame codec for the draft OOMWOO CPU/MCU serial contract."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
import struct
from typing import Iterable


MAGIC = b"OW"
VERSION = 1
HEADER_FORMAT = "<2sBBHHH"
CRC_FORMAT = "<H"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
CRC_SIZE = struct.calcsize(CRC_FORMAT)
MAX_PAYLOAD_SIZE = 512

MAX_LINEAR_MM_S = 500
MAX_ANGULAR_MRAD_S = 4000
MAX_SETPOINT_DURATION_MS = 250


class FrameDecodeError(ValueError):
    """Raised when a byte sequence is not a valid OOMWOO MCU frame."""


class MessageType(IntEnum):
    HEARTBEAT = 0x0001
    ESTOP_SET = 0x0002
    CLEAR_LATCHED_FAULT = 0x0003
    DRIVE_SETPOINT = 0x0101
    CLEANING_MOTORS_SET = 0x0102
    LIDAR_MOTOR_SET = 0x0103
    LED_SET = 0x0104
    ACK = 0x7001
    NACK = 0x7002
    MCU_HELLO = 0x8000
    FAST_TELEMETRY = 0x8001
    SAFETY_EVENT = 0x8002
    POWER_TELEMETRY = 0x8003
    MCU_DIAGNOSTIC = 0x8004


class SafetyEvent(IntEnum):
    BUMPER_LEFT = 1
    BUMPER_RIGHT = 2
    CLIFF_LEFT = 3
    CLIFF_RIGHT = 4
    WHEEL_DROP_LEFT = 5
    WHEEL_DROP_RIGHT = 6
    BRUSH_OVERCURRENT = 7
    FAN_OVERCURRENT = 8
    CPU_HEARTBEAT_TIMEOUT = 9
    ESTOP = 10


@dataclass(frozen=True)
class Frame:
    version: int
    flags: int
    sequence: int
    message_type: int
    payload: bytes


def crc16_ccitt_false(data: bytes) -> int:
    """CRC-16/CCITT-FALSE: poly 0x1021, init 0xffff, no reflection."""

    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc


def _check_uint(name: str, value: int, maximum: int) -> None:
    if not isinstance(value, int) or value < 0 or value > maximum:
        raise ValueError(f"{name} must be in range 0..{maximum}")


def _check_int(name: str, value: int, minimum: int, maximum: int) -> None:
    if not isinstance(value, int) or value < minimum or value > maximum:
        raise ValueError(f"{name} must be in range {minimum}..{maximum}")


def encode_frame(
    message_type: int | MessageType,
    payload: bytes = b"",
    *,
    sequence: int = 0,
    flags: int = 0,
    version: int = VERSION,
) -> bytes:
    """Encode a single complete frame."""

    _check_uint("version", version, 255)
    _check_uint("flags", flags, 255)
    _check_uint("sequence", sequence, 0xFFFF)
    _check_uint("message_type", int(message_type), 0xFFFF)
    if len(payload) > MAX_PAYLOAD_SIZE:
        raise ValueError(f"payload must be <= {MAX_PAYLOAD_SIZE} bytes")

    header = struct.pack(
        HEADER_FORMAT,
        MAGIC,
        version,
        flags,
        sequence,
        int(message_type),
        len(payload),
    )
    checksum = crc16_ccitt_false(header + payload)
    return header + payload + struct.pack(CRC_FORMAT, checksum)


def decode_frame(data: bytes) -> Frame:
    """Decode a single complete frame and verify its CRC."""

    if len(data) < HEADER_SIZE + CRC_SIZE:
        raise FrameDecodeError("frame too short")

    magic, version, flags, sequence, message_type, payload_len = struct.unpack(
        HEADER_FORMAT,
        data[:HEADER_SIZE],
    )
    if magic != MAGIC:
        raise FrameDecodeError("bad magic")
    if version != VERSION:
        raise FrameDecodeError(f"unsupported protocol version {version}")
    if payload_len > MAX_PAYLOAD_SIZE:
        raise FrameDecodeError("payload too large")

    expected_len = HEADER_SIZE + payload_len + CRC_SIZE
    if len(data) != expected_len:
        raise FrameDecodeError("frame length mismatch")

    payload = data[HEADER_SIZE : HEADER_SIZE + payload_len]
    expected_crc = struct.unpack(CRC_FORMAT, data[-CRC_SIZE:])[0]
    actual_crc = crc16_ccitt_false(data[:-CRC_SIZE])
    if expected_crc != actual_crc:
        raise FrameDecodeError("bad crc")

    return Frame(version, flags, sequence, message_type, payload)


class StreamDecoder:
    """Incremental decoder for UART/CDC streams."""

    def __init__(self) -> None:
        self._buffer = bytearray()

    def feed(self, chunk: bytes) -> list[Frame]:
        self._buffer.extend(chunk)
        frames: list[Frame] = []

        while True:
            magic_at = self._buffer.find(MAGIC)
            if magic_at < 0:
                self._buffer.clear()
                break
            if magic_at:
                del self._buffer[:magic_at]
            if len(self._buffer) < HEADER_SIZE:
                break

            _, _, _, _, _, payload_len = struct.unpack(
                HEADER_FORMAT,
                self._buffer[:HEADER_SIZE],
            )
            if payload_len > MAX_PAYLOAD_SIZE:
                del self._buffer[0]
                continue

            frame_len = HEADER_SIZE + payload_len + CRC_SIZE
            if len(self._buffer) < frame_len:
                break

            candidate = bytes(self._buffer[:frame_len])
            try:
                frames.append(decode_frame(candidate))
                del self._buffer[:frame_len]
            except FrameDecodeError:
                del self._buffer[0]

        return frames


def pack_heartbeat(cpu_time_ms: int, cpu_mode: int = 0) -> bytes:
    _check_uint("cpu_time_ms", cpu_time_ms, 0xFFFFFFFF)
    _check_uint("cpu_mode", cpu_mode, 0xFF)
    return struct.pack("<IB", cpu_time_ms, cpu_mode)


def pack_drive_setpoint(
    linear_mm_s: int,
    angular_mrad_s: int,
    duration_ms: int = 100,
) -> bytes:
    _check_int("linear_mm_s", linear_mm_s, -MAX_LINEAR_MM_S, MAX_LINEAR_MM_S)
    _check_int(
        "angular_mrad_s",
        angular_mrad_s,
        -MAX_ANGULAR_MRAD_S,
        MAX_ANGULAR_MRAD_S,
    )
    _check_uint("duration_ms", duration_ms, MAX_SETPOINT_DURATION_MS)
    if duration_ms == 0:
        raise ValueError("duration_ms must be non-zero")
    return struct.pack("<hhH", linear_mm_s, angular_mrad_s, duration_ms)


def unpack_drive_setpoint(payload: bytes) -> dict[str, int]:
    if len(payload) != struct.calcsize("<hhH"):
        raise ValueError("invalid DRIVE_SETPOINT payload length")
    linear_mm_s, angular_mrad_s, duration_ms = struct.unpack("<hhH", payload)
    return {
        "linear_mm_s": linear_mm_s,
        "angular_mrad_s": angular_mrad_s,
        "duration_ms": duration_ms,
    }


def pack_cleaning_motors(
    main_brush_pct: int,
    side_brush_pct: int,
    fan_pct: int,
    pump_pct: int = 0,
) -> bytes:
    for name, value in (
        ("main_brush_pct", main_brush_pct),
        ("side_brush_pct", side_brush_pct),
        ("fan_pct", fan_pct),
        ("pump_pct", pump_pct),
    ):
        _check_uint(name, value, 100)
    return struct.pack("<BBBB", main_brush_pct, side_brush_pct, fan_pct, pump_pct)


def pack_safety_event(event: int | SafetyEvent, active: bool, detail: int = 0) -> bytes:
    _check_uint("event", int(event), 0xFFFF)
    _check_uint("detail", detail, 0xFFFF)
    return struct.pack("<HBH", int(event), int(active), detail)


def pack_fast_telemetry(
    *,
    timestamp_ms: int,
    left_ticks: int,
    right_ticks: int,
    bumper_flags: int = 0,
    cliff_flags: int = 0,
    wheel_drop_flags: int = 0,
    dock_flags: int = 0,
    safety_latched_flags: int = 0,
    battery_mv: int = 0,
) -> bytes:
    _check_uint("timestamp_ms", timestamp_ms, 0xFFFFFFFF)
    _check_int("left_ticks", left_ticks, -0x80000000, 0x7FFFFFFF)
    _check_int("right_ticks", right_ticks, -0x80000000, 0x7FFFFFFF)
    for name, value in (
        ("bumper_flags", bumper_flags),
        ("cliff_flags", cliff_flags),
        ("wheel_drop_flags", wheel_drop_flags),
        ("dock_flags", dock_flags),
        ("safety_latched_flags", safety_latched_flags),
    ):
        _check_uint(name, value, 0xFF)
    _check_uint("battery_mv", battery_mv, 0xFFFF)
    return struct.pack(
        "<IiiBBBBBH",
        timestamp_ms,
        left_ticks,
        right_ticks,
        bumper_flags,
        cliff_flags,
        wheel_drop_flags,
        dock_flags,
        safety_latched_flags,
        battery_mv,
    )


def unpack_fast_telemetry(payload: bytes) -> dict[str, int]:
    if len(payload) != struct.calcsize("<IiiBBBBBH"):
        raise ValueError("invalid FAST_TELEMETRY payload length")
    fields = struct.unpack("<IiiBBBBBH", payload)
    return {
        "timestamp_ms": fields[0],
        "left_ticks": fields[1],
        "right_ticks": fields[2],
        "bumper_flags": fields[3],
        "cliff_flags": fields[4],
        "wheel_drop_flags": fields[5],
        "dock_flags": fields[6],
        "safety_latched_flags": fields[7],
        "battery_mv": fields[8],
    }


def frames_to_hex(frames: Iterable[bytes]) -> list[str]:
    return [frame.hex(" ") for frame in frames]

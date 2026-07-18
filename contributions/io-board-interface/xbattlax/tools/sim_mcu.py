#!/usr/bin/env python3
"""Generate deterministic sample MCU frames for bridge and parser tests."""

from __future__ import annotations

import argparse

from oomwoo_mcu_frame import (
    MessageType,
    SafetyEvent,
    encode_frame,
    frames_to_hex,
    pack_fast_telemetry,
    pack_safety_event,
)


def build_frames(count: int) -> list[bytes]:
    frames: list[bytes] = []
    for index in range(count):
        telemetry = pack_fast_telemetry(
            timestamp_ms=index * 20,
            left_ticks=index * 12,
            right_ticks=index * 12,
            battery_mv=15200,
        )
        frames.append(
            encode_frame(
                MessageType.FAST_TELEMETRY,
                telemetry,
                sequence=index,
            )
        )

    frames.append(
        encode_frame(
            MessageType.SAFETY_EVENT,
            pack_safety_event(SafetyEvent.BUMPER_LEFT, True, detail=0),
            sequence=count,
        )
    )
    return frames


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=5)
    args = parser.parse_args()
    if args.count < 0:
        raise SystemExit("--count must be non-negative")

    for line in frames_to_hex(build_frames(args.count)):
        print(line)


if __name__ == "__main__":
    main()

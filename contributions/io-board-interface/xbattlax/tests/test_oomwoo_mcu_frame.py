import pathlib
import sys
import unittest


TOOLS_DIR = pathlib.Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS_DIR))

from oomwoo_mcu_frame import (  # noqa: E402
    FrameDecodeError,
    MessageType,
    SafetyEvent,
    StreamDecoder,
    crc16_ccitt_false,
    decode_frame,
    encode_frame,
    pack_cleaning_motors,
    pack_drive_setpoint,
    pack_fast_telemetry,
    pack_heartbeat,
    pack_safety_event,
    unpack_drive_setpoint,
    unpack_fast_telemetry,
)


class FrameCodecTest(unittest.TestCase):
    def test_crc_known_vector(self):
        self.assertEqual(crc16_ccitt_false(b"123456789"), 0x29B1)

    def test_round_trip_heartbeat(self):
        payload = pack_heartbeat(cpu_time_ms=1234, cpu_mode=2)
        raw = encode_frame(MessageType.HEARTBEAT, payload, sequence=7)
        frame = decode_frame(raw)
        self.assertEqual(frame.sequence, 7)
        self.assertEqual(frame.message_type, MessageType.HEARTBEAT)
        self.assertEqual(frame.payload, payload)

    def test_rejects_bad_crc(self):
        raw = bytearray(
            encode_frame(
                MessageType.SAFETY_EVENT,
                pack_safety_event(SafetyEvent.ESTOP, True, detail=42),
            )
        )
        raw[-1] ^= 0x01
        with self.assertRaises(FrameDecodeError):
            decode_frame(bytes(raw))

    def test_stream_decoder_handles_noise_and_partial_frames(self):
        first = encode_frame(
            MessageType.DRIVE_SETPOINT,
            pack_drive_setpoint(100, 250, 50),
            sequence=1,
        )
        second = encode_frame(
            MessageType.CLEANING_MOTORS_SET,
            pack_cleaning_motors(20, 30, 40, 0),
            sequence=2,
        )

        decoder = StreamDecoder()
        self.assertEqual(decoder.feed(b"noise"), [])
        self.assertEqual(decoder.feed(first[:5]), [])
        frames = decoder.feed(first[5:] + b"x" + second)

        self.assertEqual([frame.sequence for frame in frames], [1, 2])
        self.assertEqual(frames[0].message_type, MessageType.DRIVE_SETPOINT)
        self.assertEqual(frames[1].message_type, MessageType.CLEANING_MOTORS_SET)

    def test_drive_setpoint_limits(self):
        payload = pack_drive_setpoint(-120, 500, 100)
        self.assertEqual(
            unpack_drive_setpoint(payload),
            {
                "linear_mm_s": -120,
                "angular_mrad_s": 500,
                "duration_ms": 100,
            },
        )
        with self.assertRaises(ValueError):
            pack_drive_setpoint(501, 0, 100)
        with self.assertRaises(ValueError):
            pack_drive_setpoint(0, 0, 251)
        with self.assertRaises(ValueError):
            pack_drive_setpoint(0, 0, 0)

    def test_percent_payload_limits(self):
        self.assertEqual(pack_cleaning_motors(0, 50, 100, 1), b"\x00\x32\x64\x01")
        with self.assertRaises(ValueError):
            pack_cleaning_motors(101, 0, 0, 0)

    def test_fast_telemetry_payload(self):
        payload = pack_fast_telemetry(
            timestamp_ms=20,
            left_ticks=-10,
            right_ticks=11,
            bumper_flags=0b01,
            cliff_flags=0b10,
            wheel_drop_flags=0,
            dock_flags=0b11,
            safety_latched_flags=0b01,
            battery_mv=15100,
        )
        self.assertEqual(
            unpack_fast_telemetry(payload),
            {
                "timestamp_ms": 20,
                "left_ticks": -10,
                "right_ticks": 11,
                "bumper_flags": 1,
                "cliff_flags": 2,
                "wheel_drop_flags": 0,
                "dock_flags": 3,
                "safety_latched_flags": 1,
                "battery_mv": 15100,
            },
        )


if __name__ == "__main__":
    unittest.main()

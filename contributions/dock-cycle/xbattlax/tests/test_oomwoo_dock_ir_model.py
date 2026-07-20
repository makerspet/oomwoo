import unittest
from math import pi

from pathlib import Path
import sys


TOOLS_DIR = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS_DIR))

from oomwoo_dock_ir_model import (  # noqa: E402
    CircleObstacle,
    DockSpec,
    Pose2D,
    compute_homing_frame,
)


class DockIrModelTest(unittest.TestCase):
    def test_centered_final_approach_has_balanced_front_receivers(self):
        frame = compute_homing_frame(Pose2D(1.0, 0.0, pi), DockSpec())

        self.assertEqual(frame.mode, "final_centered")
        self.assertAlmostEqual(frame.front_error, 0.0, delta=0.02)
        self.assertGreater(frame.reading("front_left").strength, 0.0)
        self.assertGreater(frame.reading("front_right").strength, 0.0)

    def test_offset_final_approach_requests_correct_turn(self):
        frame = compute_homing_frame(Pose2D(1.0, 0.18, pi), DockSpec())

        self.assertEqual(frame.mode, "final_turn_left")
        self.assertGreater(frame.front_error, 0.04)
        self.assertGreater(frame.angular_z_hint, 0.0)

    def test_search_receiver_detects_side_beacon_when_front_is_not_visible(self):
        frame = compute_homing_frame(Pose2D(0.35, -1.0, pi / 2.0), DockSpec())

        self.assertEqual(frame.mode, "search_turn_left")
        self.assertEqual(frame.reading("front_left").strength, 0.0)
        self.assertGreater(frame.reading("search_left").strength, 0.0)
        self.assertGreater(frame.angular_z_hint, 0.0)

    def test_blocker_occludes_beacon(self):
        frame = compute_homing_frame(
            Pose2D(1.0, 0.0, pi),
            DockSpec(),
            obstacles=(CircleObstacle(0.5, 0.0, 0.12),),
        )

        self.assertEqual(frame.mode, "search_pattern")
        for reading in frame.readings:
            self.assertFalse(reading.visible)
            self.assertEqual(reading.strength, 0.0)

    def test_signal_attenuates_with_range(self):
        near = compute_homing_frame(Pose2D(0.75, 0.0, pi), DockSpec())
        far = compute_homing_frame(Pose2D(1.65, 0.0, pi), DockSpec())

        self.assertGreater(
            near.reading("front_left").strength,
            far.reading("front_left").strength,
        )


if __name__ == "__main__":
    unittest.main()

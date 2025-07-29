import unittest
import sys
import os
from unittest.mock import patch, call
from io import StringIO

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from gear_display import (
    display_gear,
    GEAR_SEGMENTS,
    SEGMENT_POSITIONS,
    validate_gear_input,
)
from gear_animation import animate_shift, clear_screen


class TestGearDisplay(unittest.TestCase):
    """Unit tests for the 7-segment gear display functionality."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.expected_gear_3 = [
            ["#", "#", "#", "#"],  # Top horizontal (A)
            [" ", " ", " ", "#"],  # Upper right (B)
            ["#", "#", "#", "#"],  # Middle horizontal (G)
            [" ", " ", " ", "#"],  # Lower right (C)
            ["#", "#", "#", "#"],  # Bottom horizontal (D)
        ]

        self.expected_neutral = [
            [" ", " ", " ", " "],  # No top
            ["#", " ", " ", "#"],  # F and B
            [" ", " ", " ", " "],  # No middle
            ["#", " ", " ", "#"],  # E and C
            [" ", " ", " ", " "],  # No bottom
        ]

    def test_display_gear_3(self):
        """Test that gear 3 displays correctly (matches document example)."""
        result = display_gear(3)
        self.assertEqual(result, self.expected_gear_3)

    def test_display_neutral(self):
        """Test that gear 0 (Neutral) displays as 'N' with two vertical bars."""
        result = display_gear(0)
        self.assertEqual(result, self.expected_neutral)

    def test_all_gears_have_definitions(self):
        """Test that all gears 0-8 have segment definitions."""
        for gear in range(9):
            self.assertIn(gear, GEAR_SEGMENTS)
            self.assertIsInstance(GEAR_SEGMENTS[gear], set)

    def test_segment_positions_are_valid(self):
        """Test that all segment positions are within 5x4 grid bounds."""
        for segment, positions in SEGMENT_POSITIONS.items():
            for row, col in positions:
                self.assertGreaterEqual(row, 0)
                self.assertLess(row, 5)
                self.assertGreaterEqual(col, 0)
                self.assertLess(col, 4)

    def test_gear_8_all_segments(self):
        """Test that gear 8 activates all 7 segments."""
        result = display_gear(8)
        # Check that all positions are filled
        filled_positions = set()
        for row_idx, row in enumerate(result):
            for col_idx, cell in enumerate(row):
                if cell == "#":
                    filled_positions.add((row_idx, col_idx))

        # Gear 8 should have all segments active
        expected_positions = set()
        for segment in GEAR_SEGMENTS[8]:
            expected_positions.update(SEGMENT_POSITIONS[segment])

        self.assertEqual(filled_positions, expected_positions)

    def test_gear_1_minimal_segments(self):
        """Test that gear 1 only shows right vertical bars."""
        result = display_gear(1)
        expected_gear_1 = [
            [" ", " ", " ", " "],  # No top
            [" ", " ", " ", "#"],  # B only
            [" ", " ", " ", " "],  # No middle
            [" ", " ", " ", "#"],  # C only
            [" ", " ", " ", " "],  # No bottom
        ]
        self.assertEqual(result, expected_gear_1)

    def test_validate_gear_input_valid(self):
        """Test validation with valid gear inputs."""
        # Test valid gears
        for gear in range(9):
            is_valid, result = validate_gear_input(str(gear))
            self.assertTrue(is_valid)
            self.assertEqual(result, gear)

        # Test with whitespace
        is_valid, result = validate_gear_input("  3  ")
        self.assertTrue(is_valid)
        self.assertEqual(result, 3)

    def test_validate_gear_input_invalid_range(self):
        """Test validation with out-of-range gear numbers."""
        test_cases = ["-1", "9", "10", "100"]
        for invalid_input in test_cases:
            is_valid, result = validate_gear_input(invalid_input)
            self.assertFalse(is_valid)
            self.assertIn("Invalid gear", result)

    def test_validate_gear_input_invalid_format(self):
        """Test validation with non-numeric inputs."""
        test_cases = ["abc", "1.5", "", "N", "gear3"]
        for invalid_input in test_cases:
            is_valid, result = validate_gear_input(invalid_input)
            self.assertFalse(is_valid)
            self.assertIn("Invalid input", result)


class TestGearAnimation(unittest.TestCase):
    """Unit tests for the gear shift animation functionality."""

    @patch("gear_animation.time.sleep")
    @patch("gear_animation.clear_screen")
    @patch("gear_animation.gear_display.print_gear_display")
    @patch("builtins.print")
    def test_animate_shift_sequence(
        self, mock_print, mock_print_gear, mock_clear, mock_sleep
    ):
        """
        Test that animate_shift follows the correct sequence of operations.

        Verifies that the function:
        1. Prints current gear message
        2. Displays from_gear
        3. Sleeps for timing
        4. Clears screen
        5. Prints new gear message
        6. Displays to_gear
        """
        # Execute the animation
        animate_shift(3, 5)

        # Verify the sequence of calls
        expected_print_calls = [call("Current Gear: 3"), call("New Gear: 5")]
        expected_gear_calls = [call(3), call(5)]

        # Assert all expected calls were made
        mock_print.assert_has_calls(expected_print_calls)
        mock_print_gear.assert_has_calls(expected_gear_calls)
        mock_sleep.assert_called_once_with(0.5)
        mock_clear.assert_called_once()

    @patch("gear_animation.time.sleep")
    @patch("gear_animation.clear_screen")
    @patch("gear_animation.gear_display.print_gear_display")
    def test_animate_shift_valid_gear_range(
        self, mock_print_gear, mock_clear, mock_sleep
    ):
        """
        Test animate_shift with all valid gear combinations.

        Ensures the function accepts any valid gear number (0-8)
        without raising exceptions.
        """
        test_cases = [
            (0, 1),  # Neutral to first gear
            (1, 0),  # First gear to neutral
            (3, 4),  # Sequential upshift
            (5, 3),  # Downshift
            (8, 0),  # Highest gear to neutral
            (0, 8),  # Neutral to highest gear
        ]

        for from_gear, to_gear in test_cases:
            with self.subTest(from_gear=from_gear, to_gear=to_gear):
                try:
                    animate_shift(from_gear, to_gear)
                except Exception as e:
                    self.fail(
                        f"animate_shift({from_gear}, {to_gear}) raised exception: {e}"
                    )

    @patch("gear_animation.os.system")
    def test_clear_screen_windows(self, mock_system):
        """Test clear_screen function on Windows systems."""
        with patch("gear_animation.os.name", "nt"):
            clear_screen()
            mock_system.assert_called_once_with("cls")

    @patch("gear_animation.os.system")
    def test_clear_screen_unix(self, mock_system):
        """Test clear_screen function on Unix-based systems."""
        with patch("gear_animation.os.name", "posix"):
            clear_screen()
            mock_system.assert_called_once_with("clear")

    @patch("gear_animation.time.sleep")
    @patch("gear_animation.clear_screen")
    @patch("gear_animation.gear_display.print_gear_display")
    def test_animate_shift_timing(self, mock_print_gear, mock_clear, mock_sleep):
        """
        Test that animate_shift uses correct timing delay.

        Verifies the function pauses for exactly 0.5 seconds
        during the gear shift animation.
        """
        animate_shift(2, 4)

        # Verify sleep was called with correct timing
        mock_sleep.assert_called_once_with(0.5)


if __name__ == "__main__":
    unittest.main()

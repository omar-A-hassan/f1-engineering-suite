import unittest
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gear_display import display_gear, GEAR_SEGMENTS, SEGMENT_POSITIONS

class TestGearDisplay(unittest.TestCase):
    """Unit tests for the 7-segment gear display functionality."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.expected_gear_3 = [
            ['#', '#', '#', '#'],  # Top horizontal (A)
            [' ', ' ', ' ', '#'],  # Upper right (B)
            ['#', '#', '#', '#'],  # Middle horizontal (G)
            [' ', ' ', ' ', '#'],  # Lower right (C)
            ['#', '#', '#', '#']   # Bottom horizontal (D)
        ]
        
        self.expected_neutral = [
            [' ', ' ', ' ', ' '],  # No top
            ['#', ' ', ' ', '#'],  # F and B
            [' ', ' ', ' ', ' '],  # No middle
            ['#', ' ', ' ', '#'],  # E and C
            [' ', ' ', ' ', ' ']   # No bottom
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
                if cell == '#':
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
            [' ', ' ', ' ', ' '],  # No top
            [' ', ' ', ' ', '#'],  # B only
            [' ', ' ', ' ', ' '],  # No middle
            [' ', ' ', ' ', '#'],  # C only
            [' ', ' ', ' ', ' ']   # No bottom
        ]
        self.assertEqual(result, expected_gear_1)

if __name__ == '__main__':
    unittest.main()
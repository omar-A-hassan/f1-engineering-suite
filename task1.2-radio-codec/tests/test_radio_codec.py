import unittest
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from radio_codec import Codec, RadioCodecError, EncodingError, DecodingError


class TestRadioCodec(unittest.TestCase):
    """Unit tests for the radio communication codec functionality."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.codec = Codec()

    def test_round_trip_basic_commands(self):
        """Test basic round-trip encoding and decoding."""
        test_cases = [
            ["Push"],
            ["Box", "Push"],
            ["Push", "Box,box", "Push", "Overtake"],
            ["DRS", "KERS", "Pit"],
        ]

        for commands in test_cases:
            with self.subTest(commands=commands):
                encoded = self.codec.encode(commands)
                decoded = self.codec.decode(encoded)
                self.assertEqual(commands, decoded)

    def test_round_trip_f1_commands(self):
        """Test F1-specific command examples from requirements."""
        f1_commands = ["Push", "Box,box", "Push", "Overtake"]

        encoded = self.codec.encode(f1_commands)
        decoded = self.codec.decode(encoded)

        self.assertEqual(f1_commands, decoded)
        # Verify the encoded format matches expected pattern
        self.assertEqual(encoded, "4:Push7:Box,box4:Push8:Overtake")

    def test_encode_empty_list(self):
        """Test encoding an empty list."""
        result = self.codec.encode([])
        self.assertEqual(result, "")

    def test_decode_empty_string(self):
        """Test decoding an empty string."""
        result = self.codec.decode("")
        self.assertEqual(result, [])

    def test_encode_empty_strings(self):
        """Test encoding list containing empty strings."""
        commands = ["", "Push", ""]
        encoded = self.codec.encode(commands)
        decoded = self.codec.decode(encoded)

        self.assertEqual(commands, decoded)
        self.assertEqual(encoded, "0:4:Push0:")

    def test_encode_special_characters(self):
        """Test encoding strings with special characters."""
        test_cases = [
            ["Box,box"],  # Comma
            ["Push:Now"],  # Colon
            ["Test123"],  # Numbers
            ["Box-Out"],  # Hyphen
            ["Pit!"],  # Exclamation
            ["20%"],  # Percentage
            ["Temp>100"],  # Greater than
        ]

        for commands in test_cases:
            with self.subTest(commands=commands):
                encoded = self.codec.encode(commands)
                decoded = self.codec.decode(encoded)
                self.assertEqual(commands, decoded)

    def test_encode_unicode_characters(self):
        """Test encoding strings with Unicode characters."""
        test_cases = [
            ["Café"],  # Accented characters
            ["Temp°C"],  # Degree symbol
            ["±5%"],  # Plus-minus
            ["→Turn"],  # Arrow
        ]

        for commands in test_cases:
            with self.subTest(commands=commands):
                encoded = self.codec.encode(commands)
                decoded = self.codec.decode(encoded)
                self.assertEqual(commands, decoded)

    def test_encode_long_strings(self):
        """Test encoding very long strings."""
        long_command = "A" * 1000
        commands = [long_command]

        encoded = self.codec.encode(commands)
        decoded = self.codec.decode(encoded)

        self.assertEqual(commands, decoded)

    def test_encode_many_commands(self):
        """Test encoding a large number of commands."""
        commands = [f"Command{i}" for i in range(100)]

        encoded = self.codec.encode(commands)
        decoded = self.codec.decode(encoded)

        self.assertEqual(commands, decoded)

    def test_encode_invalid_input_type(self):
        """Test encoding with invalid input type."""
        invalid_inputs = [
            "not_a_list",
            123,
            None,
            {"key": "value"},
        ]

        for invalid_input in invalid_inputs:
            with self.subTest(invalid_input=invalid_input):
                with self.assertRaises(EncodingError):
                    self.codec.encode(invalid_input)

    def test_encode_invalid_element_types(self):
        """Test encoding with invalid element types in list."""
        invalid_lists = [
            [123],
            ["valid", 456],
            [None],
            ["valid", {"key": "value"}],
            [["nested", "list"]],
        ]

        for invalid_list in invalid_lists:
            with self.subTest(invalid_list=invalid_list):
                with self.assertRaises(EncodingError):
                    self.codec.encode(invalid_list)

    def test_decode_invalid_input_type(self):
        """Test decoding with invalid input type."""
        invalid_inputs = [
            123,
            None,
            ["list"],
            {"key": "value"},
        ]

        for invalid_input in invalid_inputs:
            with self.subTest(invalid_input=invalid_input):
                with self.assertRaises(DecodingError):
                    self.codec.decode(invalid_input)

    def test_decode_missing_colon(self):
        """Test decoding strings missing colon separators."""
        invalid_strings = [
            "4Push",
            "4:Push7Box",
            "nocolon",
        ]

        for invalid_string in invalid_strings:
            with self.subTest(invalid_string=invalid_string):
                with self.assertRaises(DecodingError):
                    self.codec.decode(invalid_string)

    def test_decode_invalid_length_format(self):
        """Test decoding with invalid length format."""
        invalid_strings = [
            ":Push",  # Empty length
            "abc:Push",  # Non-numeric length
            "4.5:Push",  # Float length
            "-1:Push",  # Negative length
            "04:Push",  # Leading zero (should still work)
        ]

        # Leading zero should work, others should fail
        for invalid_string in invalid_strings[:-1]:
            with self.subTest(invalid_string=invalid_string):
                with self.assertRaises(DecodingError):
                    self.codec.decode(invalid_string)

        # Leading zero case should work
        result = self.codec.decode("04:Push")
        self.assertEqual(result, ["Push"])

    def test_decode_length_mismatch(self):
        """Test decoding with length mismatch."""
        invalid_strings = [
            "5:Push",  # Length too long
            "3:Push",  # Length too short
            "10:Short",  # Much longer than actual
            "1:Toolong",  # Much shorter than actual
        ]

        for invalid_string in invalid_strings:
            with self.subTest(invalid_string=invalid_string):
                with self.assertRaises(DecodingError):
                    self.codec.decode(invalid_string)

    def test_decode_insufficient_data(self):
        """Test decoding when there's insufficient data."""
        invalid_strings = [
            "4:Pus",  # Missing one character
            "10:Short",  # Missing many characters
            "5:",  # No data after colon
        ]

        for invalid_string in invalid_strings:
            with self.subTest(invalid_string=invalid_string):
                with self.assertRaises(DecodingError):
                    self.codec.decode(invalid_string)

    def test_decode_partial_valid_data(self):
        """Test decoding partially valid data."""
        # First part valid, second part invalid
        invalid_strings = [
            "4:Push3:Go",  # Second length too short
            "4:Push10:Short",  # Second length too long
            "4:Push:",  # Second missing length
        ]

        for invalid_string in invalid_strings:
            with self.subTest(invalid_string=invalid_string):
                with self.assertRaises(DecodingError):
                    self.codec.decode(invalid_string)

    def test_encode_decode_edge_cases(self):
        """Test edge cases for encoding and decoding."""
        edge_cases = [
            ["0"],  # Single digit
            ["123456789"],  # All digits
            [":"],  # Just colon
            ["::"],  # Double colon
            ["a:b:c"],  # Multiple colons
            [" "],  # Single space
            ["  "],  # Multiple spaces
            ["\t"],  # Tab character
            ["\n"],  # Newline character
        ]

        for commands in edge_cases:
            with self.subTest(commands=commands):
                encoded = self.codec.encode(commands)
                decoded = self.codec.decode(encoded)
                self.assertEqual(commands, decoded)

    def test_encode_format_correctness(self):
        """Test that encoding produces correct format."""
        test_cases = [
            (["Push"], "4:Push"),
            (["A"], "1:A"),
            ([""], "0:"),
            (["Push", "Go"], "4:Push2:Go"),
            (["A", "BB", "CCC"], "1:A2:BB3:CCC"),
        ]

        for commands, expected in test_cases:
            with self.subTest(commands=commands, expected=expected):
                result = self.codec.encode(commands)
                self.assertEqual(result, expected)

    def test_decode_malformed_sequences(self):
        """Test decoding various malformed sequences."""
        malformed_strings = [
            "4",  # Just length, no colon
            "4:",  # Length and colon, no data
            ":4:Push",  # Leading colon
            "4:Push:",  # Trailing colon
            "4:Push5",  # Missing colon between entries
        ]

        for malformed_string in malformed_strings:
            with self.subTest(malformed_string=malformed_string):
                with self.assertRaises(DecodingError):
                    self.codec.decode(malformed_string)

    def test_unicode_length_calculation(self):
        """Test that Unicode characters are correctly handled in length calculation."""
        # Test cases with Unicode that have different byte vs character lengths
        unicode_cases = [
            "café",  # 4 chars, 5 bytes (é = 2 bytes in UTF-8)
            "温度",  # 2 chars, 6 bytes (each Chinese char = 3 bytes)
            "🏎️",  # 2 chars (car + variation selector), multiple bytes
        ]

        for unicode_string in unicode_cases:
            with self.subTest(unicode_string=unicode_string):
                commands = [unicode_string]
                encoded = self.codec.encode(commands)
                decoded = self.codec.decode(encoded)
                self.assertEqual(commands, decoded)

                # Verify the length in encoded string matches byte length
                byte_length = len(unicode_string.encode("utf-8"))
                expected_prefix = f"{byte_length}:"
                self.assertTrue(encoded.startswith(expected_prefix))


if __name__ == "__main__":
    unittest.main()

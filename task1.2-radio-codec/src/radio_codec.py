"""
Radio communication codec for F1 engineering suite.

This module implements a length-prefixed encoding scheme for transmitting
string commands over radio channels with error detection capabilities.
"""


class RadioCodecError(Exception):
    """Base exception for radio codec operations."""

    pass


class EncodingError(RadioCodecError):
    """Raised when encoding fails due to invalid input."""

    pass


class DecodingError(RadioCodecError):
    """Raised when decoding fails due to malformed data."""

    pass


class Codec:
    """
    Radio communication codec using length-prefixed encoding.

    The encoding format uses the pattern: "length:string" for each element,
    concatenated together. For example:
    ["Push", "Box,box"] becomes "4:Push7:Box,box"
    """

    def encode(self, commands):
        """
        Encode a list of strings using length-prefixed format.

        Args:
            commands (list): List of strings to encode

        Returns:
            str: Encoded string in format "length:string" concatenated

        Raises:
            EncodingError: If input is invalid or contains unsupported data
        """
        if not isinstance(commands, list):
            raise EncodingError("Input must be a list of strings")

        if not commands:
            return ""

        encoded_parts = []

        for command in commands:
            if not isinstance(command, str):
                raise EncodingError(
                    f"All elements must be strings, got {type(command).__name__}"
                )

            # Handle empty strings
            if command == "":
                encoded_parts.append("0:")
            else:
                # Calculate byte length to handle special characters correctly
                byte_length = len(command.encode("utf-8"))
                encoded_parts.append(f"{byte_length}:{command}")

        return "".join(encoded_parts)

    def decode(self, encoded_data):
        """
        Decode a length-prefixed encoded string back to list of strings.

        Args:
            encoded_data (str): Encoded string to decode

        Returns:
            list: List of decoded strings

        Raises:
            DecodingError: If encoded data is malformed or invalid
        """
        if not isinstance(encoded_data, str):
            raise DecodingError("Encoded data must be a string")

        if encoded_data == "":
            return []

        decoded_commands = []
        # Convert to bytes for proper Unicode handling
        encoded_bytes = encoded_data.encode("utf-8")
        byte_position = 0

        while byte_position < len(encoded_bytes):
            # Find the colon separator in bytes
            try:
                colon_byte_pos = encoded_bytes.index(b":", byte_position)
            except ValueError:
                raise DecodingError(
                    f"Missing colon separator at byte position {byte_position}"
                )

            # Extract and validate length
            length_bytes = encoded_bytes[byte_position:colon_byte_pos]

            if not length_bytes:
                raise DecodingError(
                    f"Empty length field at byte position {byte_position}"
                )

            try:
                length_str = length_bytes.decode("utf-8")
                expected_length = int(length_str)
            except (ValueError, UnicodeDecodeError):
                raise DecodingError(f"Invalid length at byte position {byte_position}")

            if expected_length < 0:
                raise DecodingError(
                    f"Negative length {expected_length} at byte position {byte_position}"
                )

            # Calculate data boundaries in bytes
            data_start_byte = colon_byte_pos + 1
            data_end_byte = data_start_byte + expected_length

            if data_end_byte > len(encoded_bytes):
                raise DecodingError(
                    f"Insufficient data: expected {expected_length} bytes at position {data_start_byte}, "
                    f"but only {len(encoded_bytes) - data_start_byte} bytes available"
                )

            # Extract the command bytes and decode to string
            command_bytes = encoded_bytes[data_start_byte:data_end_byte]

            try:
                command = command_bytes.decode("utf-8")
            except UnicodeDecodeError:
                raise DecodingError(
                    f"Invalid UTF-8 data at byte position {data_start_byte}"
                )

            decoded_commands.append(command)
            byte_position = data_end_byte

        return decoded_commands


def main():
    """Interactive testing function for the radio codec."""
    codec = Codec()

    print("F1 Radio Codec - Interactive Testing")
    print("=====================================")
    print("Enter commands separated by commas, or 'quit' to exit")
    print("Example: Push,Box,box,Overtake")
    print()

    while True:
        try:
            user_input = input("Enter commands: ").strip()

            if user_input.lower() == "quit":
                print("Goodbye!")
                break

            if not user_input:
                print("Please enter some commands.")
                continue

            # Parse input into list
            commands = [cmd.strip() for cmd in user_input.split(",")]

            print(f"Original: {commands}")

            # Encode
            encoded = codec.encode(commands)
            print(f"Encoded:  {encoded}")

            # Decode
            decoded = codec.decode(encoded)
            print(f"Decoded:  {decoded}")

            # Verify round trip
            if commands == decoded:
                print("✓ Round trip successful!")
            else:
                print("✗ Round trip failed!")

            print()

        except (EncodingError, DecodingError) as e:
            print(f"Error: {e}")
            print()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            print()


if __name__ == "__main__":
    main()

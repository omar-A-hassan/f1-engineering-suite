# F1 Radio Codec System

A robust radio communication codec for Formula 1 engineering applications, implementing length-prefixed encoding for reliable command transmission over radio channels.

## Overview

The F1 Radio Codec System provides a reliable method for encoding and decoding string commands transmitted over radio channels in Formula 1 environments. The system uses a length-prefixed encoding scheme that ensures data integrity and enables error detection during transmission.

## Features

- **Length-Prefixed Encoding**: Each string is prefixed with its byte length for precise parsing
- **Error Detection**: Comprehensive validation and error handling for malformed data
- **Unicode Support**: Full support for international characters and special symbols
- **Edge Case Handling**: Robust handling of empty strings, special characters, and edge cases
- **Interactive Testing**: Built-in command-line interface for testing and validation

## Usage Examples

### Basic Usage

```python
from radio_codec import Codec

# Create codec instance
codec = Codec()

# Encode F1 commands
commands = ["Push", "Box,box", "Push", "Overtake"]
encoded = codec.encode(commands)
print(f"Encoded: {encoded}")
# Output: "4:Push7:Box,box4:Push8:Overtake"

# Decode back to original commands
decoded = codec.decode(encoded)
print(f"Decoded: {decoded}")
# Output: ["Push", "Box,box", "Push", "Overtake"]
```

### Error Handling

```python
from radio_codec import Codec, EncodingError, DecodingError

codec = Codec()

try:
    # This will raise EncodingError
    codec.encode("not_a_list")
except EncodingError as e:
    print(f"Encoding error: {e}")

try:
    # This will raise DecodingError
    codec.decode("invalid_format")
except DecodingError as e:
    print(f"Decoding error: {e}")
```

### Interactive Testing

Run the interactive testing mode:

```bash
cd task1.2-radio-codec/src
python radio_codec.py
```

This will start an interactive session where you can test encoding and decoding with various inputs.

## Architecture

### Length-Prefixed Encoding Format

The encoding format follows the pattern: `length:string` for each element, concatenated together.

**Examples:**
- `["Push"]` → `"4:Push"`
- `["A", "BB"]` → `"1:A2:BB"`
- `["", "Test"]` → `"0:4:Test"`

### Key Components

1. **Codec Class**: Main interface for encoding and decoding operations
2. **Error Classes**: Specialized exception classes for different error types
3. **Validation**: Comprehensive input validation and error detection
4. **Unicode Handling**: Proper byte-length calculation for international characters

### Error Handling Strategy

The system implements a defensive approach to error handling:

- **Input Validation**: All inputs are validated before processing
- **Type Checking**: Strict type checking for all parameters
- **Length Verification**: Encoded data length is verified during decoding
- **Graceful Degradation**: Clear error messages for debugging

## Testing

Run the test suite:

```bash
cd task1.2-radio-codec
python -m pytest tests/ -v
```

Or run with unittest:

```bash
cd task1.2-radio-codec
python -m unittest tests.test_radio_codec -v
```

### Test Coverage

The test suite covers:
- Round-trip encoding/decoding validation
- F1-specific command examples
- Edge cases (empty strings, special characters)
- Unicode character support
- Error handling for malformed data
- Performance with large datasets

## Version History

### v1.0.0
- Initial implementation of length-prefixed radio codec
- Basic encode/decode functionality
- Comprehensive error handling
- Unicode character support
- Interactive testing interface
- Full test suite with edge case coverage

# F1 Engineering Suite

Complete engineering simulation suite for HMS-26 Formula 1 car systems.

## Project Structure

- `task1.1-gear-display/` - 7-segment gear indicator display & animation system
- `task1.2-radio-codec/` - Radio communication codec with length-prefixed encoding
- `.github/workflows/` - CI/CD pipeline configuration

## Quick Start

```bash
# Test the gear display and animation
cd task1.1-gear-display
python -m pytest tests/ -v

# Run the gear display
cd task1.1-gear-display/src
python gear_display.py

# Run the gear animation
cd task1.1-gear-display/src
python gear_animation.py

# Test the radio codec
cd task1.2-radio-codec
python -m pytest tests/ -v

# Run the radio codec interactive mode
cd task1.2-radio-codec/src
python radio_codec.py
```

## Development

This project uses automated testing and CI/CD for all components. Each task includes comprehensive unit tests and follows F1 engineering standards.
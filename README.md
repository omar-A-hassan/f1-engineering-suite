
# F1 Engineering Suite

Complete engineering simulation suite for HMS-26 Formula 1 car systems.

## Project Structure

- `task1.1-gear-display/` - 7-segment gear indicator display & animation system
- `task1.2-radio-codec/` - Radio communication codec with length-prefixed encoding
- `task1.3-race-simulator/` - Turn-based F1 racing simulator (Verstappen vs Mostafa)
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

# Test the race simulator
cd task1.3-race-simulator
python -m pytest tests/ -v

# Run the race simulator
cd task1.3-race-simulator/src
python race_simulator.py
```

## Development

This project uses automated testing and CI/CD for all components. Each task includes comprehensive unit tests and follows F1 engineering standards.

### Recent Updates

**Task 1.3 Hybrid Fuel System (v1.1.0)**: Implemented balanced fuel management system to eliminate turn order bias and add strategic depth:

- **Fuel Exhaustion Penalties**: Players who run out of fuel take 5 tire damage penalties and skip turns (instead of immediate elimination)
- **Resource-Based Victory**: When both players are out of fuel, winner determined by resource comparison (fuel priority, then tire health)
- **Strategic Balance**: Rewards fuel management while allowing comeback scenarios through penalty survival
- **Fair Gameplay**: Eliminates unfair advantages from turn order, making strategic resource conservation crucial

This creates realistic F1-style fuel management where running out of fuel causes mechanical penalties rather than instant disqualification.
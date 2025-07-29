# Task 1.1 & 1.2: F1 Steering Wheel Digital Gear Indicator & Animation

## Overview
Complete 7-segment display and animation system for HMS-26 F1 car digital gear indicator, featuring realistic gear shift animations with professional timing simulation.

## Features
-  7-segment display simulation using 5x4 grid
-  Support for gears 0-8 (where 0 = Neutral)
-  Realistic segment-based rendering
-  Input validation with error handling (v1.1.0)
-  Professional gear shift animation with timing simulation (v1.2.0)
-  Cross-platform screen clearing functionality
-  Comprehensive unit test coverage

## Usage

### Gear Display
```bash
cd task1.1-gear-display/src
python gear_display.py
```

### Gear Animation
```bash
cd task1.1-gear-display/src
python gear_animation.py
```

## Core Animation Function
```python
animate_shift(from_gear, to_gear)
```
Animates a gear shift by displaying the current gear, pausing for realistic timing, clearing the screen, and displaying the target gear.

## Testing
```bash
cd task1.1-gear-display
python -m pytest tests/ -v
```

## Example Output (Gear 3)
```
####
   #
####
   #
####
```

## Architecture
- **Segment-based design**: Each digit is formed by activating specific segments (A-G)
- **Modular structure**: Easy to extend with new features
- **Platform Independence**: Automatic detection for Windows/Unix screen clearing
- **Professional Timing**: 0.5 second pause for realistic gear shift simulation
- **Comprehensive Testing**: Unit tests with mocking for timing and system calls

## Version History
- **v1.2.0**: Added gear shift animation with professional timing simulation
- **v1.1.0**: Added input validation with error handling and retry loop
- **v1.0.0**: Initial 7-segment display implementation
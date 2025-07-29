# Task 1.1: F1 Steering Wheel Digital Gear Indicator

## Overview
A 7-segment display simulator F1 cars digital gear indicator.

## Features
- ✅ 7-segment display simulation using 5x4 grid
- ✅ Support for gears 0-8 (where 0 = Neutral)
- ✅ Realistic segment-based rendering
- ✅ Input validation with error handling (v1.1.0)
- 🚧 Gear shift animation (upcoming v1.2.0)

## Usage
```bash
cd task1-gear-display/src
python gear_display.py
```

## Testing
```bash
cd task1-gear-display
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
- **Independent light bars**: No pixel overlap, each grid position belongs to one segment
- **Modular structure**: Easy to extend with new features

## Version History
- **v1.1.0**: Added input validation with error handling and retry loop
- **v1.0.0**: Initial 7-segment display implementation
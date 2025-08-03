# Task 1.3: F1 Race Simulator - The Final Race

Turn-based racing simulation between Max Verstappen and Hassan Mostafa featuring maximum OOP implementation.

## Overview

This racing simulator demonstrates all four OOP principles through an engaging turn-based F1 race:

- **Abstraction**: Abstract `Driver` base class with defined interface
- **Inheritance**: `Verstappen` and `Mostafa` inherit from `Driver`
- **Polymorphism**: Different driver implementations with unique move sets
- **Encapsulation**: Protected attributes with controlled access

## Game Mechanics

- **Turn-Based Racing**: Drivers alternate taking offensive moves
- **Defensive Responses**: Opponents can defend against incoming attacks
- **Resource Management**: Fuel consumption and tire health tracking
- **Win Conditions**: 
  - **Tire Elimination**: Race ends when a driver's tire health reaches zero or below
  - **Hybrid Fuel System**: 
    - **Single player out of fuel**: Takes 5 tire damage penalty and skips turn (allows survival and comeback)
    - **Both players out of fuel**: Winner determined by resource comparison
    - **Resource comparison priority**: Fuel difference ≥10 wins, then tire health difference ≥5, otherwise draw
- **Fuel Exhaustion Penalties**: Players who run out of fuel receive 5 tire damage and must skip their turn instead of immediate elimination
- **Move Limitations**: Some moves have limited uses
- **Fuel Warnings**: Critical fuel alerts when fuel drops to 50 or below

## Driver Specifications

### Max Verstappen
**Offensive Moves:**
- DRS Boost (Fuel: 45, Damage: 12, Uses: ∞)
- Red Bull Surge (Fuel: 80, Damage: 20, Uses: ∞)
- Precision Turn (Fuel: 30, Damage: 8, Uses: ∞)

**Defensive Tactics:**
- Brake Late (Fuel: 25, Reduction: 30%, Uses: ∞)
- ERS Deployment (Fuel: 40, Reduction: 50%, Uses: 3)

### Hassan Mostafa
**Offensive Moves:**
- Turbo Start (Fuel: 50, Damage: 10, Uses: ∞)
- Mercedes Charge (Fuel: 90, Damage: 22, Uses: ∞)
- Corner Mastery (Fuel: 25, Damage: 7, Uses: ∞)

**Defensive Tactics:**
- Slipstream Cut (Fuel: 20, Reduction: 40%, Uses: ∞)
- Aggressive Block (Fuel: 35, Reduction: 100%, Uses: 2)

## Quick Start

```bash
# Run the race simulator
cd task1.3-race-simulator/src
python race_simulator.py

# Run tests
cd task1.3-race-simulator
python -m pytest tests/ -v

# Code quality checks
flake8 src/ --max-line-length=88
black --check src/
```

## Project Structure

```
task1.3-race-simulator/
├── src/
│   ├── __init__.py
│   ├── moves.py          # Move system classes
│   ├── drivers.py        # Driver classes
│   └── race_simulator.py # Main game logic
├── tests/
│   └── test_race_simulator.py # Comprehensive test suite
├── requirements.txt
└── README.md
```

## Features

- **Professional UI**: Clean menu-driven interface with fuel warnings
- **Input Validation**: Comprehensive error handling
- **Game Statistics**: Real-time fuel and health tracking
- **Move Constraints**: Fuel requirements and usage limits
- **Damage Calculation**: Realistic combat mechanics
- **Balanced Hybrid Win System**: Eliminates turn order bias with penalty system
- **Edge Case Handling**: Zero fuel/health scenarios with proper game termination

## Testing

The test suite covers:
- All OOP principles implementation
- Move validation and execution
- Damage calculations with/without defense
- Win conditions: tire failure AND hybrid fuel system
- Limited-use moves and fuel constraints
- Edge cases and boundary conditions
- Polymorphism and inheritance verification
- Fuel exhaustion scenarios and game termination

## Critical Fixes: Balanced Hybrid Fuel System

### Problem 1 Solved: Infinite Loop Prevention
**Issue**: Drivers could get stuck with 0 fuel, unable to make moves, causing infinite loops.
**Solution**: Added `can_make_any_offensive_move()` method and fuel exhaustion detection before move selection.

### Problem 2 Solved: Turn Order Bias Elimination  
**Issue**: Simple "first to run out loses" system created unfair turn order bias regardless of overall resource management.
**Solution**: Implemented hybrid penalty system with resource-based endgame:

**Hybrid Fuel System Features**:
- **Single Player Exhaustion**: 5 tire damage penalty + skip turn (allows strategic survival)
- **Dual Player Exhaustion**: Winner by resource comparison (fuel ≥10 difference, then tire health ≥5 difference)
- **Penalty Survival**: Players can survive fuel exhaustion through good tire management
- **Strategic Depth**: Fuel conservation becomes crucial tactical decision

**Game Balance Benefits**:
- Eliminates turn order bias - both players get equal opportunities
- Rewards strategic fuel management over aggressive-only tactics  
- Creates dramatic comeback scenarios through penalty survival
- Maintains tire health as ultimate elimination condition
- Adds realistic F1-style fuel management consequences

**Real F1 Logic**: Mirrors Formula 1 where fuel exhaustion causes mechanical penalties and strategic disadvantages rather than immediate race disqualification.

for more added fairness at the start of the game the order of who starts should not be fixed and can be replaced with
a randomized start, simulating flipping a coin to determine wether verstappen or mostafa who starts first
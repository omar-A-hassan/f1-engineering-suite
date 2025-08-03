"""
Driver system for F1 Racing Simulator.
Implements abstract Driver base class and concrete Verstappen and Mostafa classes.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from moves import OffensiveMove, DefensiveMove


class Driver(ABC):
    """Abstract base class for all F1 drivers."""

    def __init__(self, name: str):
        """Initialize driver with starting stats.

        Args:
            name: Name of the driver
        """
        self._name = name
        self._tire_health = 100
        self._fuel = 500

    @property
    def name(self) -> str:
        """Get driver name."""
        return self._name

    @property
    def tire_health(self) -> int:
        """Get current tire health."""
        return self._tire_health

    @property
    def fuel(self) -> int:
        """Get current fuel level."""
        return self._fuel

    def take_damage(self, damage: int) -> None:
        """Apply tire damage to the driver.

        Args:
            damage: Amount of tire health to reduce
        """
        self._tire_health = max(0, self._tire_health - damage)

    def consume_fuel(self, amount: int) -> None:
        """Consume fuel for a move.

        Args:
            amount: Amount of fuel to consume
        """
        self._fuel = max(0, self._fuel - amount)

    def is_alive(self) -> bool:
        """Check if driver can continue racing.

        Returns:
            True if tire health is above 0, False otherwise
        """
        return self._tire_health > 0

    def get_stats(self) -> Dict[str, int]:
        """Get current driver statistics.

        Returns:
            Dictionary containing tire health and fuel levels
        """
        return {"tire_health": self._tire_health, "fuel": self._fuel}

    @abstractmethod
    def get_offensive_moves(self) -> List[OffensiveMove]:
        """Get list of available offensive moves for this driver.

        Returns:
            List of OffensiveMove objects
        """
        pass

    @abstractmethod
    def get_defensive_moves(self) -> List[DefensiveMove]:
        """Get list of available defensive moves for this driver.

        Returns:
            List of DefensiveMove objects
        """
        pass

    def execute_offensive_move(self, move: OffensiveMove) -> Optional[int]:
        """Execute an offensive move if possible.

        Args:
            move: OffensiveMove to execute

        Returns:
            Damage dealt if move was executed, None if move couldn't be used
        """
        if not move.can_use(self._fuel):
            return None

        self.consume_fuel(move.fuel_cost)
        move.use_move()
        return move.tire_damage

    def execute_defensive_move(self, move: DefensiveMove) -> Optional[float]:
        """Execute a defensive move if possible.

        Args:
            move: DefensiveMove to execute

        Returns:
            Damage reduction percentage if move was executed, None if move couldn't be used
        """
        if not move.can_use(self._fuel):
            return None

        self.consume_fuel(move.fuel_cost)
        move.use_move()
        return move.damage_reduction_percent

    def can_make_any_offensive_move(self) -> bool:
        """Check if driver has fuel for at least one offensive move.

        Returns:
            True if driver can make at least one offensive move, False otherwise
        """
        for move in self.get_offensive_moves():
            if move.can_use(self._fuel):
                return True
        return False


class Verstappen(Driver):
    """Max Verstappen driver implementation."""

    def __init__(self):
        """Initialize Verstappen with his specific move set."""
        super().__init__("Max Verstappen")
        self._initialize_moves()

    def _initialize_moves(self):
        """Initialize move sets for Verstappen."""
        self._offensive_moves = [
            OffensiveMove(
                "DRS Boost",
                45,
                12,
                None,
                "Drag Reduction System, allows drivers to temporarily increase straight-line speed",
            ),
            OffensiveMove(
                "Red Bull Surge",
                80,
                20,
                None,
                "Aggressive acceleration, high tire wear",
            ),
            OffensiveMove(
                "Precision Turn",
                30,
                8,
                None,
                "Tactical turn to gain time with minimal fuel",
            ),
        ]

        self._defensive_moves = [
            DefensiveMove(
                "Brake Late",
                25,
                0.30,
                None,
                "Uses ultra-late braking to reduce attack impact. Common but risky.",
            ),
            DefensiveMove(
                "ERS Deployment",
                40,
                0.50,
                3,
                "Deploys electric recovery system defensively to absorb incoming pressure and recover next turn",
            ),
        ]

    def get_offensive_moves(self) -> List[OffensiveMove]:
        """Get Verstappen's offensive moves.

        Returns:
            List of OffensiveMove objects specific to Verstappen
        """
        return self._offensive_moves

    def get_defensive_moves(self) -> List[DefensiveMove]:
        """Get Verstappen's defensive moves.

        Returns:
            List of DefensiveMove objects specific to Verstappen
        """
        return self._defensive_moves


class Mostafa(Driver):
    """Mostafa driver implementation."""

    def __init__(self):
        """Initialize Mostafa with his specific move set."""
        super().__init__("Mostafa")
        self._initialize_moves()

    def _initialize_moves(self):
        """Initialize move sets for Mostafa."""
        self._offensive_moves = [
            OffensiveMove("Turbo Start", 50, 10, None, "Early burst of speed"),
            OffensiveMove("Mercedes Charge", 90, 22, None, "Full-throttle attack"),
            OffensiveMove(
                "Corner Mastery", 25, 7, None, "Skilled turning for efficiency"
            ),
        ]

        self._defensive_moves = [
            DefensiveMove(
                "Slipstream Cut",
                20,
                0.40,
                None,
                "Cuts into the airflow behind the leading car to reduce their advantage and limit damage",
            ),
            DefensiveMove(
                "Aggressive Block",
                35,
                1.00,
                2,
                "Swerves defensively to completely block a single incoming move. Can only be used once due to risk",
            ),
        ]

    def get_offensive_moves(self) -> List[OffensiveMove]:
        """Get Mostafa's offensive moves.

        Returns:
            List of OffensiveMove objects specific to Mostafa
        """
        return self._offensive_moves

    def get_defensive_moves(self) -> List[DefensiveMove]:
        """Get Mostafa's defensive moves.

        Returns:
            List of DefensiveMove objects specific to Mostafa
        """
        return self._defensive_moves

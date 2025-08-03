"""
Move system for F1 Racing Simulator.
Implements Move base class and specialized OffensiveMove and DefensiveMove classes.
"""

from typing import Optional


class Move:
    """Base class for all racing moves with common attributes."""

    def __init__(
        self, name: str, fuel_cost: int, uses_remaining: Optional[int], description: str
    ):
        """Initialize a move with basic attributes.

        Args:
            name: Name of the move
            fuel_cost: Fuel required to execute the move
            uses_remaining: Number of times move can be used (None for unlimited)
            description: Description of what the move does
        """
        self.name = name
        self.fuel_cost = fuel_cost
        self.uses_remaining = uses_remaining
        self.description = description

    def can_use(self, current_fuel: int) -> bool:
        """Check if move can be used based on fuel and remaining uses.

        Args:
            current_fuel: Current fuel level of the driver

        Returns:
            True if move can be used, False otherwise
        """
        has_fuel = current_fuel >= self.fuel_cost
        has_uses = self.uses_remaining is None or self.uses_remaining > 0
        return has_fuel and has_uses

    def use_move(self) -> None:
        """Consume one use of the move if it has limited uses."""
        if self.uses_remaining is not None:
            self.uses_remaining -= 1


class OffensiveMove(Move):
    """Offensive move that deals tire damage to opponent."""

    def __init__(
        self,
        name: str,
        fuel_cost: int,
        tire_damage: int,
        uses_remaining: Optional[int],
        description: str,
    ):
        """Initialize offensive move with damage capability.

        Args:
            name: Name of the move
            fuel_cost: Fuel required to execute the move
            tire_damage: Damage dealt to opponent's tire health
            uses_remaining: Number of times move can be used (None for unlimited)
            description: Description of what the move does
        """
        super().__init__(name, fuel_cost, uses_remaining, description)
        self.tire_damage = tire_damage


class DefensiveMove(Move):
    """Defensive move that reduces incoming damage."""

    def __init__(
        self,
        name: str,
        fuel_cost: int,
        damage_reduction_percent: float,
        uses_remaining: Optional[int],
        description: str,
    ):
        """Initialize defensive move with damage reduction capability.

        Args:
            name: Name of the move
            fuel_cost: Fuel required to execute the move
            damage_reduction_percent: Percentage of damage to reduce (0.0 to 1.0)
            uses_remaining: Number of times move can be used (None for unlimited)
            description: Description of what the move does
        """
        super().__init__(name, fuel_cost, uses_remaining, description)
        self.damage_reduction_percent = damage_reduction_percent

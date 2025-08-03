"""
F1 Race Simulator main game logic.
Implements the RaceSimulator class for turn-based racing between drivers.
"""

from typing import Optional
from drivers import Verstappen, Mostafa


class RaceSimulator:
    """Main game controller for F1 Racing Simulator."""

    def __init__(self):
        """Initialize the race simulator with two drivers."""
        self.verstappen = Verstappen()
        self.mostafa = Mostafa()
        self.current_driver = self.verstappen
        self.opponent = self.mostafa
        self.turn_number = 1
        self._winner = None
        self._win_reason = None

    def switch_turns(self) -> None:
        """Switch active driver and opponent for next turn."""
        if self.current_driver == self.verstappen:
            self.current_driver = self.mostafa
            self.opponent = self.verstappen
        else:
            self.current_driver = self.verstappen
            self.opponent = self.mostafa
        self.turn_number += 1

    def display_move_menu(self, moves: list, move_type: str) -> None:
        """Display numbered menu of available moves.

        Args:
            moves: List of moves to display
            move_type: Type of moves ("Offensive" or "Defensive")
        """
        print(f"\n{move_type} Moves:")
        for i, move in enumerate(moves, 1):
            uses_text = ""
            if move.uses_remaining is not None:
                uses_text = f" (Uses left: {move.uses_remaining})"

            availability = "✓" if move.can_use(self.current_driver.fuel) else "✗"
            print(
                f"{i}. {move.name} - Fuel: {move.fuel_cost}{uses_text} [{availability}]"
            )
            print(f"   {move.description}")

    def get_move_choice(self, moves: list, move_type: str) -> Optional[int]:
        """Get player's move choice with validation.

        Args:
            moves: List of available moves
            move_type: Type of moves being selected

        Returns:
            Index of chosen move or None if skipping defensive move
        """
        while True:
            if move_type == "Defensive":
                choice = input(
                    f"\nChoose defensive move (1-{len(moves)}) or press Enter to skip: "
                ).strip()
                if not choice:
                    return None
            else:
                choice = input(f"\nChoose offensive move (1-{len(moves)}): ").strip()

            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(moves):
                    selected_move = moves[choice_num - 1]
                    if selected_move.can_use(self.current_driver.fuel):
                        return choice_num - 1
                    else:
                        print(
                            "Cannot use this move - insufficient fuel or "
                            "no uses remaining!"
                        )
                else:
                    print(f"Please enter a number between 1 and {len(moves)}")
            except ValueError:
                print("Please enter a valid number")

    def execute_turn(self) -> bool:
        """Execute a complete turn (offensive move + optional defensive response).

        Returns:
            True if game should continue, False if game is over
        """
        print(f"\n{'='*50}")
        print(f"Turn {self.turn_number}: {self.current_driver.name}'s Turn")
        print(f"{'='*50}")

        # Display current stats
        print("\nCurrent Stats:")
        verstappen_stats = self.verstappen.get_stats()
        mostafa_stats = self.mostafa.get_stats()
        v_health = verstappen_stats["tire_health"]
        v_fuel = verstappen_stats["fuel"]
        m_health = mostafa_stats["tire_health"]
        m_fuel = mostafa_stats["fuel"]
        print(f"Verstappen: Tire Health={v_health}, Fuel={v_fuel}")
        print(f"Mostafa: Tire Health={m_health}, Fuel={m_fuel}")

        # Check for fuel exhaustion scenarios
        if not self.current_driver.can_make_any_offensive_move():
            if not self.opponent.can_make_any_offensive_move():
                # Both players stuck - determine winner by resources
                print("\nBoth drivers are out of fuel!")
                print("Determining winner by remaining resources...")
                return self._determine_winner_by_resources()
            else:
                # Only current player stuck - penalty and skip turn
                print(
                    f"\n{self.current_driver.name} is out of fuel and must skip turn!"
                )
                print("Applying 5 tire damage penalty for fuel exhaustion...")
                self.current_driver.take_damage(5)

                # Check if penalty caused elimination
                if not self.current_driver.is_alive():
                    print(
                        f"{self.current_driver.name} eliminated by fuel "
                        "exhaustion penalty!"
                    )
                    return False

                print(f"{self.current_driver.name} survives but skips turn.")
                return True  # Continue game with turn switch

        # Display fuel warning if critical
        if self.current_driver.fuel <= 50:
            fuel_remaining = self.current_driver.fuel
            print(
                f"\n⚠️  FUEL CRITICAL for {self.current_driver.name}! "
                f"({fuel_remaining} remaining)"
            )

        # Get offensive move from current driver
        offensive_moves = self.current_driver.get_offensive_moves()
        self.display_move_menu(offensive_moves, "Offensive")

        offensive_choice = self.get_move_choice(offensive_moves, "Offensive")
        if offensive_choice is None:
            return False

        chosen_offensive = offensive_moves[offensive_choice]
        base_damage = self.current_driver.execute_offensive_move(chosen_offensive)

        if base_damage is None:
            print("Failed to execute move!")
            return False

        print(
            f"\n{self.current_driver.name} used {chosen_offensive.name} - "
            f"{chosen_offensive.description}"
        )

        # Get defensive response from opponent
        defensive_moves = self.opponent.get_defensive_moves()
        available_defensive = [
            move for move in defensive_moves if move.can_use(self.opponent.fuel)
        ]

        final_damage = base_damage

        if available_defensive:
            print(f"\n{self.opponent.name} can respond defensively:")
            self.display_move_menu(available_defensive, "Defensive")

            defensive_choice = self.get_move_choice(available_defensive, "Defensive")
            if defensive_choice is not None:
                chosen_defensive = available_defensive[defensive_choice]
                damage_reduction = self.opponent.execute_defensive_move(
                    chosen_defensive
                )

                if damage_reduction is not None:
                    final_damage = int(base_damage * (1 - damage_reduction))
                    print(f"{self.opponent.name} defended with {chosen_defensive.name}")

        # Apply damage
        self.opponent.take_damage(final_damage)
        print(f"Damage dealt: {final_damage} tire health")

        # Display updated stats
        verstappen_stats = self.verstappen.get_stats()
        mostafa_stats = self.mostafa.get_stats()
        v_health = verstappen_stats["tire_health"]
        v_fuel = verstappen_stats["fuel"]
        m_health = mostafa_stats["tire_health"]
        m_fuel = mostafa_stats["fuel"]
        print(f"Verstappen: Tire Health={v_health}, Fuel={v_fuel}")
        print(f"Mostafa: Tire Health={m_health}, Fuel={m_fuel}")

        # Check for winner
        if not self.opponent.is_alive():
            return False

        return True

    def _determine_winner_by_resources(self) -> bool:
        """
        Determine winner when both players cannot make moves.
        Compare fuel first, then tire health if fuel is close.

        Returns:
            False to end the game
        """
        verstappen_stats = self.verstappen.get_stats()
        mostafa_stats = self.mostafa.get_stats()

        fuel_diff = abs(verstappen_stats["fuel"] - mostafa_stats["fuel"])
        tire_diff = abs(verstappen_stats["tire_health"] - mostafa_stats["tire_health"])

        print("\nResource Comparison:")
        v_fuel = verstappen_stats["fuel"]
        v_health = verstappen_stats["tire_health"]
        m_fuel = mostafa_stats["fuel"]
        m_health = mostafa_stats["tire_health"]
        print(f"Verstappen: {v_fuel} fuel, {v_health} tire health")
        print(f"Mostafa: {m_fuel} fuel, {m_health} tire health")

        # Primary comparison: fuel (if significant difference)
        if fuel_diff >= 10:
            if verstappen_stats["fuel"] > mostafa_stats["fuel"]:
                self._winner = "Max Verstappen"
                self._win_reason = "Superior fuel management"
            else:
                self._winner = "Mostafa"
                self._win_reason = "Superior fuel management"

        # Secondary comparison: tire health (if fuel is close)
        elif tire_diff >= 5:
            if verstappen_stats["tire_health"] > mostafa_stats["tire_health"]:
                self._winner = "Max Verstappen"
                self._win_reason = "Better tire condition"
            else:
                self._winner = "Mostafa"
                self._win_reason = "Better tire condition"

        # Draw if resources are very close
        else:
            self._winner = "Draw"
            self._win_reason = "Equal resource management"

        return False  # End the game

    def display_winner(self) -> None:
        """Display race results and winner."""
        print(f"\n{'='*50}")
        print("RACE FINISHED!")
        print(f"{'='*50}")

        verstappen_stats = self.verstappen.get_stats()
        mostafa_stats = self.mostafa.get_stats()

        # Check if winner was determined by resources
        if hasattr(self, "_winner") and self._winner is not None:
            winner = self._winner
            reason = self._win_reason
        else:
            # Original win condition logic (tire health)
            if self.verstappen.is_alive() and not self.mostafa.is_alive():
                winner = "Max Verstappen"
                reason = "Opponent tire failure"
            elif self.mostafa.is_alive() and not self.verstappen.is_alive():
                winner = "Mostafa"
                reason = "Opponent tire failure"
            else:
                winner = "Draw"
                reason = "Both drivers unable to continue"

        print(f"Winner: {winner}")
        print(f"Reason: {reason}")
        print("\nFinal Race Statistics:")
        v_health = verstappen_stats["tire_health"]
        v_fuel = verstappen_stats["fuel"]
        m_health = mostafa_stats["tire_health"]
        m_fuel = mostafa_stats["fuel"]
        print(f"Verstappen: Tire Health={v_health}, Fuel={v_fuel}")
        print(f"Mostafa: Tire Health={m_health}, Fuel={m_fuel}")

    def start_race(self) -> None:
        """Start the main race loop."""
        print("Welcome to F1 Racing Simulator: The Final Race - Verstappen vs Mostafa")
        print("Initial stats: Tire Health=100, Fuel=500 for both drivers")

        while True:
            if not self.execute_turn():
                break

            if not self.opponent.is_alive():
                break

            self.switch_turns()

        self.display_winner()


def main() -> None:
    """Main entry point for the race simulator."""
    simulator = RaceSimulator()
    simulator.start_race()


if __name__ == "__main__":
    main()

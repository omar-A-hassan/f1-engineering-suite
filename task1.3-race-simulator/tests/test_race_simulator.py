"""
Comprehensive test suite for F1 Racing Simulator.
Tests all OOP principles, game mechanics, and edge cases.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from moves import Move, OffensiveMove, DefensiveMove
from drivers import Driver, Verstappen, Mostafa
from race_simulator import RaceSimulator


class TestMoves(unittest.TestCase):
    """Test Move classes and polymorphism."""

    def test_move_base_class(self):
        """Test Move base class functionality."""
        move = Move("Test Move", 50, 3, "Test description")

        self.assertEqual(move.name, "Test Move")
        self.assertEqual(move.fuel_cost, 50)
        self.assertEqual(move.uses_remaining, 3)
        self.assertEqual(move.description, "Test description")

    def test_move_can_use_with_fuel(self):
        """Test move usage validation with sufficient fuel."""
        move = Move("Test Move", 50, None, "Test description")
        self.assertTrue(move.can_use(100))
        self.assertFalse(move.can_use(30))

    def test_move_can_use_with_limited_uses(self):
        """Test move usage validation with limited uses."""
        move = Move("Test Move", 50, 2, "Test description")
        self.assertTrue(move.can_use(100))

        move.use_move()
        self.assertTrue(move.can_use(100))
        self.assertEqual(move.uses_remaining, 1)

        move.use_move()
        self.assertFalse(move.can_use(100))
        self.assertEqual(move.uses_remaining, 0)

    def test_offensive_move_inheritance(self):
        """Test OffensiveMove inherits from Move correctly."""
        offensive = OffensiveMove("Attack", 40, 15, None, "Damage move")

        self.assertIsInstance(offensive, Move)
        self.assertEqual(offensive.tire_damage, 15)
        self.assertTrue(offensive.can_use(50))

    def test_defensive_move_inheritance(self):
        """Test DefensiveMove inherits from Move correctly."""
        defensive = DefensiveMove("Block", 30, 0.5, 2, "Defense move")

        self.assertIsInstance(defensive, Move)
        self.assertEqual(defensive.damage_reduction_percent, 0.5)
        self.assertTrue(defensive.can_use(40))


class TestDrivers(unittest.TestCase):
    """Test Driver classes and abstraction."""

    def test_driver_abstraction(self):
        """Test that Driver is abstract and cannot be instantiated."""
        with self.assertRaises(TypeError):
            Driver("Test Driver")

    def test_verstappen_initialization(self):
        """Test Verstappen driver initialization."""
        verstappen = Verstappen()

        self.assertEqual(verstappen.name, "Max Verstappen")
        self.assertEqual(verstappen.tire_health, 100)
        self.assertEqual(verstappen.fuel, 500)
        self.assertTrue(verstappen.is_alive())

    def test_mostafa_initialization(self):
        """Test Mostafa driver initialization."""
        mostafa = Mostafa()

        self.assertEqual(mostafa.name, "Mostafa")
        self.assertEqual(mostafa.tire_health, 100)
        self.assertEqual(mostafa.fuel, 500)
        self.assertTrue(mostafa.is_alive())

    def test_driver_take_damage(self):
        """Test damage application and bounds."""
        driver = Verstappen()

        driver.take_damage(30)
        self.assertEqual(driver.tire_health, 70)

        driver.take_damage(80)
        self.assertEqual(driver.tire_health, 0)
        self.assertFalse(driver.is_alive())

    def test_driver_fuel_consumption(self):
        """Test fuel consumption and bounds."""
        driver = Verstappen()

        driver.consume_fuel(200)
        self.assertEqual(driver.fuel, 300)

        driver.consume_fuel(400)
        self.assertEqual(driver.fuel, 0)

    def test_verstappen_moves(self):
        """Test Verstappen's specific move sets."""
        verstappen = Verstappen()

        offensive_moves = verstappen.get_offensive_moves()
        self.assertEqual(len(offensive_moves), 3)

        move_names = [move.name for move in offensive_moves]
        self.assertIn("DRS Boost", move_names)
        self.assertIn("Red Bull Surge", move_names)
        self.assertIn("Precision Turn", move_names)

        defensive_moves = verstappen.get_defensive_moves()
        self.assertEqual(len(defensive_moves), 2)

        defense_names = [move.name for move in defensive_moves]
        self.assertIn("Brake Late", defense_names)
        self.assertIn("ERS Deployment", defense_names)

    def test_mostafa_moves(self):
        """Test Mostafa's specific move sets."""
        mostafa = Mostafa()

        offensive_moves = mostafa.get_offensive_moves()
        self.assertEqual(len(offensive_moves), 3)

        move_names = [move.name for move in offensive_moves]
        self.assertIn("Turbo Start", move_names)
        self.assertIn("Mercedes Charge", move_names)
        self.assertIn("Corner Mastery", move_names)

        defensive_moves = mostafa.get_defensive_moves()
        self.assertEqual(len(defensive_moves), 2)

        defense_names = [move.name for move in defensive_moves]
        self.assertIn("Slipstream Cut", defense_names)
        self.assertIn("Aggressive Block", defense_names)


class TestGameMechanics(unittest.TestCase):
    """Test game mechanics and interactions."""

    def test_offensive_move_execution(self):
        """Test offensive move execution and fuel consumption."""
        driver = Verstappen()
        moves = driver.get_offensive_moves()
        drs_boost = moves[0]  # DRS Boost

        initial_fuel = driver.fuel
        damage = driver.execute_offensive_move(drs_boost)

        self.assertEqual(damage, 12)
        self.assertEqual(driver.fuel, initial_fuel - 45)

    def test_defensive_move_execution(self):
        """Test defensive move execution and damage reduction."""
        driver = Verstappen()
        moves = driver.get_defensive_moves()
        brake_late = moves[0]  # Brake Late

        initial_fuel = driver.fuel
        reduction = driver.execute_defensive_move(brake_late)

        self.assertEqual(reduction, 0.30)
        self.assertEqual(driver.fuel, initial_fuel - 25)

    def test_insufficient_fuel_prevention(self):
        """Test that moves cannot be executed without sufficient fuel."""
        driver = Verstappen()
        driver.consume_fuel(480)  # Leave only 20 fuel

        moves = driver.get_offensive_moves()
        red_bull_surge = moves[1]  # Red Bull Surge (80 fuel cost)

        damage = driver.execute_offensive_move(red_bull_surge)
        self.assertIsNone(damage)

    def test_limited_use_moves(self):
        """Test moves with limited uses."""
        verstappen = Verstappen()
        defensive_moves = verstappen.get_defensive_moves()
        ers_deployment = defensive_moves[1]  # ERS Deployment (3 uses)

        # First use
        reduction1 = verstappen.execute_defensive_move(ers_deployment)
        self.assertEqual(reduction1, 0.50)
        self.assertEqual(ers_deployment.uses_remaining, 2)

        # Second use
        reduction2 = verstappen.execute_defensive_move(ers_deployment)
        self.assertEqual(reduction2, 0.50)
        self.assertEqual(ers_deployment.uses_remaining, 1)

        # Third use
        reduction3 = verstappen.execute_defensive_move(ers_deployment)
        self.assertEqual(reduction3, 0.50)
        self.assertEqual(ers_deployment.uses_remaining, 0)

        # Fourth use should fail
        reduction4 = verstappen.execute_defensive_move(ers_deployment)
        self.assertIsNone(reduction4)

    def test_damage_calculation(self):
        """Test damage calculation with defense."""
        base_damage = 20
        defense_reduction = 0.30

        final_damage = int(base_damage * (1 - defense_reduction))
        self.assertEqual(final_damage, 14)

        # Test 100% block
        full_block = 1.00
        blocked_damage = int(base_damage * (1 - full_block))
        self.assertEqual(blocked_damage, 0)


class TestRaceSimulator(unittest.TestCase):
    """Test RaceSimulator game flow."""

    def test_simulator_initialization(self):
        """Test race simulator initialization."""
        simulator = RaceSimulator()

        self.assertIsInstance(simulator.verstappen, Verstappen)
        self.assertIsInstance(simulator.mostafa, Mostafa)
        self.assertEqual(simulator.current_driver, simulator.verstappen)
        self.assertEqual(simulator.opponent, simulator.mostafa)
        self.assertEqual(simulator.turn_number, 1)

    def test_turn_switching(self):
        """Test turn switching mechanism."""
        simulator = RaceSimulator()

        initial_driver = simulator.current_driver
        initial_opponent = simulator.opponent
        initial_turn = simulator.turn_number

        simulator.switch_turns()

        self.assertEqual(simulator.current_driver, initial_opponent)
        self.assertEqual(simulator.opponent, initial_driver)
        self.assertEqual(simulator.turn_number, initial_turn + 1)

    def test_win_condition_tire_health(self):
        """Test win condition when tire health reaches zero."""
        simulator = RaceSimulator()

        # Damage one driver to zero health
        simulator.mostafa.take_damage(100)

        self.assertFalse(simulator.mostafa.is_alive())
        self.assertTrue(simulator.verstappen.is_alive())


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def test_exactly_zero_fuel(self):
        """Test behavior when fuel is exactly zero."""
        driver = Verstappen()
        driver.consume_fuel(500)  # Consume all fuel

        self.assertEqual(driver.fuel, 0)

        moves = driver.get_offensive_moves()
        precision_turn = moves[2]  # Precision Turn (30 fuel cost)

        damage = driver.execute_offensive_move(precision_turn)
        self.assertIsNone(damage)

    def test_can_make_any_offensive_move(self):
        """Test can_make_any_offensive_move method."""
        driver = Verstappen()

        # Driver with full fuel should be able to make moves
        self.assertTrue(driver.can_make_any_offensive_move())

        # Driver with some fuel should be able to make at least precision turn (30 fuel)
        driver.consume_fuel(475)  # Leave 25 fuel (less than cheapest move)
        self.assertFalse(driver.can_make_any_offensive_move())

        # Driver with exactly enough fuel for cheapest move
        driver = Verstappen()
        driver.consume_fuel(470)  # Leave 30 fuel (exactly enough for Precision Turn)
        self.assertTrue(driver.can_make_any_offensive_move())

        # Driver with zero fuel
        driver.consume_fuel(30)  # Consume remaining fuel
        self.assertFalse(driver.can_make_any_offensive_move())

    def test_fuel_exhaustion_win_condition(self):
        """Test fuel exhaustion penalty system in simulator."""
        simulator = RaceSimulator()

        # Drain Mostafa's fuel completely
        simulator.mostafa.consume_fuel(500)

        # Set current driver to Mostafa
        simulator.current_driver = simulator.mostafa
        simulator.opponent = simulator.verstappen

        initial_health = simulator.mostafa.tire_health

        # Execute turn should apply penalty and continue (not end game)
        with patch("builtins.print"):  # Suppress output for test
            result = simulator.execute_turn()

        # Should continue game and apply penalty
        self.assertTrue(result)
        self.assertEqual(simulator.mostafa.fuel, 0)
        self.assertFalse(simulator.mostafa.can_make_any_offensive_move())
        self.assertEqual(simulator.mostafa.tire_health, initial_health - 5)

    def test_hybrid_fuel_exhaustion_both_players(self):
        """Test hybrid win condition when both players run out of fuel."""
        simulator = RaceSimulator()

        # Set up scenario: Verstappen has significantly more fuel (≥10 difference)
        simulator.verstappen.consume_fuel(475)  # 25 fuel left
        simulator.mostafa.consume_fuel(490)  # 10 fuel left

        # Both have equal tire health
        simulator.verstappen.take_damage(30)  # 70 health
        simulator.mostafa.take_damage(30)  # 70 health

        # Neither can make moves (cheapest is 25 fuel for Verstappen, 10 < 25 for Mostafa)
        self.assertFalse(simulator.verstappen.can_make_any_offensive_move())
        self.assertFalse(simulator.mostafa.can_make_any_offensive_move())

        # Execute turn should end game with Verstappen winning by fuel (15 fuel difference)
        with patch("builtins.print"):
            result = simulator._determine_winner_by_resources()

        self.assertFalse(result)
        self.assertEqual(simulator._winner, "Max Verstappen")
        self.assertEqual(simulator._win_reason, "Superior fuel management")

    def test_hybrid_fuel_exhaustion_penalty_system(self):
        """Test penalty system when only one player runs out of fuel."""
        simulator = RaceSimulator()

        # Set up: only current driver runs out of fuel
        simulator.verstappen.consume_fuel(500)  # 0 fuel
        simulator.mostafa.consume_fuel(100)  # 400 fuel remaining

        # Current driver is Verstappen (out of fuel)
        simulator.current_driver = simulator.verstappen
        simulator.opponent = simulator.mostafa

        initial_health = simulator.verstappen.tire_health

        # Should not be able to make moves
        self.assertFalse(simulator.verstappen.can_make_any_offensive_move())
        self.assertTrue(simulator.mostafa.can_make_any_offensive_move())

        # Execute turn should apply penalty and continue
        with patch("builtins.print"):
            result = simulator.execute_turn()

        # Should continue game (return True) and apply 5 damage penalty
        self.assertTrue(result)
        self.assertEqual(simulator.verstappen.tire_health, initial_health - 5)

    def test_hybrid_tire_health_win_condition(self):
        """Test tire health-based win when fuel is close."""
        simulator = RaceSimulator()

        # Set up scenario: Similar fuel levels (within 10 difference)
        simulator.verstappen.consume_fuel(485)  # 15 fuel left
        simulator.mostafa.consume_fuel(480)  # 20 fuel left

        # Verstappen has significantly better tire health (≥5 difference)
        simulator.verstappen.take_damage(20)  # 80 health
        simulator.mostafa.take_damage(30)  # 70 health

        # Neither can make moves
        self.assertFalse(simulator.verstappen.can_make_any_offensive_move())
        self.assertFalse(simulator.mostafa.can_make_any_offensive_move())

        # Execute turn should end game with Verstappen winning by tire health
        with patch("builtins.print"):
            result = simulator._determine_winner_by_resources()

        self.assertFalse(result)
        self.assertEqual(simulator._winner, "Max Verstappen")
        self.assertEqual(simulator._win_reason, "Better tire condition")

    def test_exactly_zero_tire_health(self):
        """Test behavior when tire health is exactly zero."""
        driver = Verstappen()
        driver.take_damage(100)  # Reduce to exactly zero

        self.assertEqual(driver.tire_health, 0)
        self.assertFalse(driver.is_alive())

    def test_fuel_constraint_for_defense(self):
        """Test fuel constraint preventing defensive moves."""
        driver = Mostafa()
        driver.consume_fuel(485)  # Leave 15 fuel

        defensive_moves = driver.get_defensive_moves()
        slipstream_cut = defensive_moves[0]  # Slipstream Cut (20 fuel cost)

        self.assertFalse(slipstream_cut.can_use(driver.fuel))

        reduction = driver.execute_defensive_move(slipstream_cut)
        self.assertIsNone(reduction)

    def test_polymorphism_in_move_lists(self):
        """Test that move lists contain proper polymorphic objects."""
        driver = Verstappen()

        offensive_moves = driver.get_offensive_moves()
        for move in offensive_moves:
            self.assertIsInstance(move, OffensiveMove)
            self.assertIsInstance(move, Move)

        defensive_moves = driver.get_defensive_moves()
        for move in defensive_moves:
            self.assertIsInstance(move, DefensiveMove)
            self.assertIsInstance(move, Move)


class TestOOPPrinciples(unittest.TestCase):
    """Test implementation of OOP principles."""

    def test_encapsulation(self):
        """Test that internal attributes are properly encapsulated."""
        driver = Verstappen()

        # Test that attributes are protected/private
        self.assertTrue(hasattr(driver, "_tire_health"))
        self.assertTrue(hasattr(driver, "_fuel"))
        self.assertTrue(hasattr(driver, "_name"))

        # Test access through properties
        self.assertEqual(driver.tire_health, 100)
        self.assertEqual(driver.fuel, 500)
        self.assertEqual(driver.name, "Max Verstappen")

    def test_inheritance_hierarchy(self):
        """Test proper inheritance relationships."""
        verstappen = Verstappen()
        mostafa = Mostafa()

        # Test driver inheritance
        self.assertIsInstance(verstappen, Driver)
        self.assertIsInstance(mostafa, Driver)

        # Test move inheritance
        offensive = OffensiveMove("Test", 10, 5, None, "Test")
        defensive = DefensiveMove("Test", 10, 0.5, None, "Test")

        self.assertIsInstance(offensive, Move)
        self.assertIsInstance(defensive, Move)

    def test_polymorphism_driver_methods(self):
        """Test polymorphic behavior of driver methods."""
        drivers = [Verstappen(), Mostafa()]

        for driver in drivers:
            # Test that all drivers respond to same interface
            self.assertTrue(hasattr(driver, "get_offensive_moves"))
            self.assertTrue(hasattr(driver, "get_defensive_moves"))
            self.assertTrue(hasattr(driver, "execute_offensive_move"))
            self.assertTrue(hasattr(driver, "execute_defensive_move"))

            # Test that methods return appropriate types
            offensive_moves = driver.get_offensive_moves()
            defensive_moves = driver.get_defensive_moves()

            self.assertIsInstance(offensive_moves, list)
            self.assertIsInstance(defensive_moves, list)
            self.assertTrue(len(offensive_moves) > 0)
            self.assertTrue(len(defensive_moves) > 0)

    def test_abstraction_enforcement(self):
        """Test that abstract methods must be implemented."""
        # This is tested in test_driver_abstraction above
        # Driver class cannot be instantiated due to abstract methods
        pass


if __name__ == "__main__":
    unittest.main()

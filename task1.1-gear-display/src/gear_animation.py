# Task 1.2: F1 Gear Shift Animation System
import time
import os

# Import the core display functions from same directory
import gear_display


def clear_screen():
    """
    Clear the terminal screen using platform-appropriate command.

    Uses 'cls' for Windows systems and 'clear' for Unix-based systems.
    """
    os.system("cls" if os.name == "nt" else "clear")


def animate_shift(from_gear, to_gear):
    """
    Animate a gear shift from one gear to another.

    This function simulates a realistic gear shift by:
    1. Displaying the current gear
    2. Pausing briefly to simulate shift timing
    3. Clearing the screen
    4. Displaying the target gear

    Args:
        from_gear (int): Starting gear number (0-8)
        to_gear (int): Target gear number (0-8)
    """
    # Display the current gear
    print(f"Current Gear: {from_gear}")
    gear_display.print_gear_display(from_gear)

    # Pause for realistic gear shift timing
    time.sleep(0.5)

    # Clear the screen to simulate the shift
    clear_screen()

    # Display the new gear
    print(f"New Gear: {to_gear}")
    gear_display.print_gear_display(to_gear)


def main():
    """
    Main function to demonstrate gear shift animation.

    Prompts user for from_gear and to_gear, validates inputs,
    and demonstrates the animation functionality.
    """
    print("F1 Gear Shift Animation System")
    print("=" * 35)

    # Get and validate from_gear input
    from_gear_input = input("Enter starting gear (0-8): ")
    from_valid, from_result = gear_display.validate_gear_input(from_gear_input)

    if not from_valid:
        print(f"Error: {from_result}")
        return

    # Get and validate to_gear input
    to_gear_input = input("Enter target gear (0-8): ")
    to_valid, to_result = gear_display.validate_gear_input(to_gear_input)

    if not to_valid:
        print(f"Error: {to_result}")
        return

    # Perform the gear shift animation
    print("\nStarting gear shift animation...")
    time.sleep(1)  # Brief pause before animation starts
    clear_screen()
    animate_shift(from_result, to_result)


if __name__ == "__main__":
    main()

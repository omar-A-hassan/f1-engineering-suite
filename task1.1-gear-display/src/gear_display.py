# Task 1.1: Seven Segment Display for F1 Gear Indicator

# Define which grid positions each segment occupies
SEGMENT_POSITIONS = {
    "A": [(0, 0), (0, 1), (0, 2), (0, 3)],  # Top horizontal
    "F": [(1, 0)],  # Upper left vertical
    "B": [(1, 3)],  # Upper right vertical
    "G": [(2, 0), (2, 1), (2, 2), (2, 3)],  # Middle horizontal
    "E": [(3, 0)],  # Lower left vertical
    "C": [(3, 3)],  # Lower right vertical
    "D": [(4, 0), (4, 1), (4, 2), (4, 3)],  # Bottom horizontal
}

# Define which segments are active for each gear (0-8)
GEAR_SEGMENTS = {
    0: {"F", "E", "B", "C"},  # Neutral (N)
    1: {"B", "C"},  # Digit 1
    2: {"A", "B", "G", "E", "D"},  # Digit 2
    3: {"A", "B", "G", "C", "D"},  # Digit 3
    4: {"F", "G", "B", "C"},  # Digit 4
    5: {"A", "F", "G", "C", "D"},  # Digit 5
    6: {"A", "F", "G", "E", "C", "D"},  # Digit 6
    7: {"A", "B", "C"},  # Digit 7
    8: {"A", "B", "C", "D", "E", "F", "G"},  # Digit 8
}


def display_gear(gear_number):
    """
    Display a gear number using a simulated 7-segment display.

    Args:
        gear_number (int): Gear number from 0-8

    Returns:
        list: 5x4 grid representing the display
    """
    # Get the active segments for this gear
    active_segments = GEAR_SEGMENTS[gear_number]

    # Create a 5x4 grid filled with spaces
    grid = [[" " for _ in range(4)] for _ in range(5)]

    # Fill in the grid positions for each active segment
    for segment in active_segments:
        positions = SEGMENT_POSITIONS[segment]
        for row, col in positions:
            grid[row][col] = "#"

    return grid


def print_gear_display(gear_number):
    """
    Print a gear number using a simulated 7-segment display.

    Args:
        gear_number (int): Gear number from 0-8
    """
    grid = display_gear(gear_number)
    for row in grid:
        print("".join(row))


def validate_gear_input(user_input):
    """
    Validate user input for gear selection.

    Args:
        user_input (str): Raw user input

    Returns:
        tuple: (is_valid, gear_number_or_error_message)
    """
    try:
        gear = int(user_input.strip())
        if 0 <= gear <= 8:
            return True, gear
        else:
            return False, f"Invalid gear: {gear}. Please enter 0-8."
    except ValueError:
        return False, f"Invalid input: '{user_input}'. Please enter a number 0-8."


def main():
    """Main function to get user input and display the gear."""
    while True:
        user_input = input("Enter Gear (0-8): ")
        is_valid, result = validate_gear_input(user_input)

        if is_valid:
            print_gear_display(result)
            break
        else:
            print(f"Error: {result}")
            print("Try again...")


if __name__ == "__main__":
    main()

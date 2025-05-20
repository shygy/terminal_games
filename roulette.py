#!/usr/bin/env python3
"""
Roulette Game Module

This module implements a feature-rich Roulette game with various betting options:
- Straight Up: Bet on a single number
- Split: Bet on two adjacent numbers
- Street: Bet on three numbers in a row
- Corner: Bet on four numbers that form a square
- Red/Black: Bet on color
- Odd/Even: Bet on odd or even numbers
- High/Low: Bet on numbers 1-18 or 19-36

The game uses a virtual currency called "Rocks" for betting and keeps track
of player's winnings over multiple rounds of play.

Quality of Life Features:
- Quick betting presets with "quick:" commands
- Color-coded text output (toggle with "color:switch")
- Win streak tracking and rewards
- Help system (type "help" at any prompt)
"""

import random
import time
import sys
try:
    # Try to import from the utils_terminal module in the current directory
    from utils_terminal import (
        colorText, 
        processCommand, 
        processQuickBet,
        getStreakData,
        saveStreakData,
        getWinStreakReward
    )
except ImportError:
    # If the terminal module is not found, try importing from the utils folder
    try:
        from terminal_games.utils_terminal import (
            colorText, 
            processCommand, 
            processQuickBet,
            getStreakData,
            saveStreakData,
            getWinStreakReward
        )
    except ImportError:
        # If both imports fail, provide fallback implementations for testing
        def colorText(text, color):
            """Fallback implementation of colorText function"""
            return text
            
        def processCommand(command, game_name):
            """Fallback implementation of processCommand function"""
            return (False, "")
            
        def processQuickBet(command):
            """Fallback implementation of processQuickBet function"""
            return (False, {})
            
        def getStreakData(game_name):
            """Fallback implementation of getStreakData function"""
            return (0, 0)
            
        def saveStreakData(game_name, win_count, max_streak):
            """Fallback implementation of saveStreakData function"""
            pass
            
        def getWinStreakReward(streak, game_name):
            """Fallback implementation of getWinStreakReward function"""
            return (0, "")

# Define roulette wheel numbers and their properties
WHEEL_NUMBERS = list(range(0, 37))  # 0-36, where 0 is green (house)
RED_NUMBERS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
BLACK_NUMBERS = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
GREEN_NUMBERS = [0]

# Define betting options and their payouts
BET_TYPES = {
    'straight': {'name': 'Straight Up', 'description': 'Bet on a single number (0-36)', 'payout': 35},
    'split': {'name': 'Split', 'description': 'Bet on two adjacent numbers', 'payout': 17},
    'street': {'name': 'Street', 'description': 'Bet on three numbers in a row', 'payout': 11},
    'corner': {'name': 'Corner', 'description': 'Bet on four numbers that form a square', 'payout': 8},
    'red': {'name': 'Red', 'description': 'Bet on any red number', 'payout': 1},
    'black': {'name': 'Black', 'description': 'Bet on any black number', 'payout': 1},
    'odd': {'name': 'Odd', 'description': 'Bet on any odd number', 'payout': 1},
    'even': {'name': 'Even', 'description': 'Bet on any even number', 'payout': 1},
    'low': {'name': 'Low (1-18)', 'description': 'Bet on numbers 1-18', 'payout': 1},
    'high': {'name': 'High (19-36)', 'description': 'Bet on numbers 19-36', 'payout': 1}
}

def get_color(number):
    """
    Determine the color of a roulette number.
    
    Args:
        number (int): A roulette number (0-36)
        
    Returns:
        str: The color of the number ("red", "black", or "green")
    """
    if number in RED_NUMBERS:
        return "red"
    elif number in BLACK_NUMBERS:
        return "black"
    else:
        return "green"  # Only 0 is green

def spin_wheel():
    """
    Simulate spinning the roulette wheel.
    
    Returns:
        int: The winning number (0-36)
    """
    print("\nThe wheel is spinning...")
    # Add suspense with a countdown
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(0.5)
    
    winning_number = random.choice(WHEEL_NUMBERS)
    color = get_color(winning_number)
    
    print(f"\nThe ball lands on: {winning_number} {color.upper()}")
    return winning_number

def check_win(bet_type, bet_value, winning_number):
    """
    Check if a bet wins based on the winning number.
    
    Args:
        bet_type (str): The type of bet (straight, red, even, etc.)
        bet_value (int or list): The value of the bet (specific number or list of numbers)
        winning_number (int): The winning number from the wheel spin
        
    Returns:
        bool: True if the bet wins, False otherwise
    """
    if bet_type == 'straight':
        return bet_value == winning_number
    
    elif bet_type == 'split':
        return winning_number in bet_value
    
    elif bet_type == 'street':
        return winning_number in bet_value
    
    elif bet_type == 'corner':
        return winning_number in bet_value
    
    elif bet_type == 'red':
        return winning_number in RED_NUMBERS
    
    elif bet_type == 'black':
        return winning_number in BLACK_NUMBERS
    
    elif bet_type == 'odd':
        return winning_number != 0 and winning_number % 2 == 1
    
    elif bet_type == 'even':
        return winning_number != 0 and winning_number % 2 == 0
    
    elif bet_type == 'low':
        return 1 <= winning_number <= 18
    
    elif bet_type == 'high':
        return 19 <= winning_number <= 36
    
    return False

def calculate_payout(bet_type, bet_amount):
    """
    Calculate the payout for a winning bet.
    
    Args:
        bet_type (str): The type of bet (straight, red, even, etc.)
        bet_amount (int): The amount bet in Rocks
        
    Returns:
        int: The payout amount in Rocks (including the original bet)
    """
    payout_multiplier = BET_TYPES[bet_type]['payout']
    return bet_amount + (bet_amount * payout_multiplier)

def display_roulette_board():
    """
    Display a visual representation of the roulette board.
    
    This function prints a formatted layout of the roulette numbers in a traditional
    order, with colors indicated for better visualization.
    
    Returns:
        None: Just prints the board layout
    """
    print("\n===== ROULETTE BOARD =====")
    
    # Display 0 separately
    print("     [0] (GREEN)")
    
    # Display the main board (1-36) in rows of three
    print("\n    1st Column    2nd Column    3rd Column")
    print("    -----------  -----------  -----------")
    
    for row in range(12):
        line = ""
        for col in range(3):
            num = 3 * row + col + 1
            color = get_color(num)
            if color == "red":
                line += f"    [{num:2d}] (RED)  "
            else:
                line += f"    [{num:2d}] (BLK)  "
        print(line)
    
    print("\n=========================")

def get_valid_bet_amount(rocks):
    """
    Get a valid bet amount from the player.
    
    This function handles input validation to ensure the bet is:
    - A valid number
    - Greater than zero
    - Not more than the player's available rocks
    
    Args:
        rocks (int): The player's current rock balance
        
    Returns:
        int: A valid bet amount or -1 if the player wants to quit
    """
    while True:
        # Show rocks balance above the input prompt
        print(colorText(f"\nYou have {rocks} Rocks available.", "cyan"))
        bet_input = input(colorText("How many Rocks do you want to bet? ", "magenta")).lower()
        
        # Process general commands
        handled, result = processCommand(bet_input, "roulette")
        if handled:
            print(result)
            continue
        
        # Check if player wants to quit
        if bet_input in ['quit', 'q', 'exit']:
            if confirm_quit():
                return -1
            else:
                continue
                
        # Handle quick bet commands - but we only use them to validate, not actually place bets here
        isQuickBet, betInfo = processQuickBet(bet_input)
        if isQuickBet:
            if betInfo["amount"] is not None:
                betAmount = betInfo["amount"]
                if betAmount <= 0:
                    print(colorText("Bet amount must be greater than zero.", "red"))
                    continue
                    
                if betAmount > rocks:
                    print(colorText(f"You only have {rocks} Rocks available.", "red"))
                    continue
                    
                return betAmount
            else:
                print("Please specify a bet amount, e.g., 'quick:red 10'")
                continue
                
        try:
            bet_amount = int(bet_input)
            
            if bet_amount <= 0:
                print(colorText("Bet amount must be greater than zero.", "red"))
                continue
                
            if bet_amount > rocks:
                print(colorText(f"You only have {rocks} Rocks available.", "red"))
                continue
                
            return bet_amount
            
        except ValueError:
            print(colorText("Please enter a valid number.", "red"))

def confirm_quit():
    """
    Asks the user to confirm if they want to quit the game.
    
    Returns:
        bool: True if the user confirms quitting, False otherwise
    """
    while True:
        confirm = input("Confirm quit? (y/n): ").lower()
        if confirm in ['y', 'yes']:
            print("\nThanks for playing Roulette! Goodbye!")
            return True
        elif confirm in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' or 'n'.")

def get_valid_number_bet():
    """
    Get a valid number or number combination for betting.
    
    This function handles input validation for various number-based bets.
    
    Returns:
        tuple: (bet_type, bet_value, description) where:
            - bet_type is the type of bet (e.g., "straight", "split")
            - bet_value is the number or list of numbers being bet on
            - description is a text description of the bet for display
    """
    while True:
        print("\n=== NUMBER BET OPTIONS ===")
        print("1. Straight Up - Bet on a single number (pays 35:1)")
        print("2. Split - Bet on two adjacent numbers (pays 17:1)")
        print("3. Street - Bet on three numbers in a row (pays 11:1)")
        print("4. Corner - Bet on four numbers that form a square (pays 8:1)")
        print("5. Return to main betting menu")
        
        choice = input("\nEnter your choice (1-5): ").lower()
        
        # Check if player wants to quit
        if choice in ['quit', 'q', 'exit']:
            if confirm_quit():
                return None, None, None
            else:
                continue
        
        if choice == '1':
            # Straight Up bet
            while True:
                try:
                    num = input("Enter a number to bet on (0-36): ").lower()
                    
                    # Check if player wants to quit
                    if num in ['quit', 'q', 'exit']:
                        if confirm_quit():
                            return None, None, None
                        else:
                            continue
                            
                    num = int(num)
                    if 0 <= num <= 36:
                        return 'straight', num, f"Straight Up bet on {num}"
                    else:
                        print("Please enter a number between 0 and 36.")
                except ValueError:
                    print("Please enter a valid number.")
                    
        elif choice == '2':
            # Split bet
            display_roulette_board()
            print("\nFor a Split bet, enter two adjacent numbers:")
            while True:
                try:
                    input1 = input("Enter first number (0-36): ").lower()
                    
                    # Check if player wants to quit
                    if input1 in ['quit', 'q', 'exit']:
                        if confirm_quit():
                            return None, None, None
                        else:
                            continue
                            
                    input2 = input("Enter second number (0-36): ").lower()
                    
                    # Check if player wants to quit
                    if input2 in ['quit', 'q', 'exit']:
                        if confirm_quit():
                            return None, None, None
                        else:
                            continue
                    
                    num1 = int(input1)
                    num2 = int(input2)
                    
                    if 0 <= num1 <= 36 and 0 <= num2 <= 36:
                        # Check if numbers are adjacent (simplified version)
                        if abs(num1 - num2) == 1 or abs(num1 - num2) == 3:
                            return 'split', [num1, num2], f"Split bet on {num1} and {num2}"
                        else:
                            print("The numbers must be adjacent on the roulette board.")
                    else:
                        print("Both numbers must be between 0 and 36.")
                except ValueError:
                    print("Please enter valid numbers.")
                    
        elif choice == '3':
            # Street bet
            display_roulette_board()
            print("\nFor a Street bet, enter the first number in a row of three.")
            print("Valid starting numbers: 1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34")
            
            while True:
                try:
                    input_num = input("Enter the starting number: ").lower()
                    
                    # Check if player wants to quit
                    if input_num in ['quit', 'q', 'exit']:
                        if confirm_quit():
                            return None, None, None
                        else:
                            continue
                            
                    num = int(input_num)
                    valid_starts = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
                    
                    if num in valid_starts:
                        street_nums = [num, num+1, num+2]
                        return 'street', street_nums, f"Street bet on {street_nums[0]}, {street_nums[1]}, and {street_nums[2]}"
                    else:
                        print("Please enter a valid starting number for a street bet.")
                except ValueError:
                    print("Please enter a valid number.")
                    
        elif choice == '4':
            # Corner bet
            display_roulette_board()
            print("\nFor a Corner bet, enter the smallest number in a square of four.")
            print("Valid starting numbers: 1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20, 22, 23, 25, 26, 28, 29, 31, 32, 34")
            
            while True:
                try:
                    input_num = input("Enter the starting number: ").lower()
                    
                    # Check if player wants to quit
                    if input_num in ['quit', 'q', 'exit']:
                        if confirm_quit():
                            return None, None, None
                        else:
                            continue
                            
                    num = int(input_num)
                    valid_starts = [1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20, 22, 23, 25, 26, 28, 29, 31, 32, 34]
                    
                    if num in valid_starts:
                        corner_nums = [num, num+1, num+3, num+4]
                        return 'corner', corner_nums, f"Corner bet on {corner_nums[0]}, {corner_nums[1]}, {corner_nums[2]}, and {corner_nums[3]}"
                    else:
                        print("Please enter a valid starting number for a corner bet.")
                except ValueError:
                    print("Please enter a valid number.")
                    
        elif choice == '5':
            # Return to main menu
            return 'return_to_main', None, None
            
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

def get_valid_outside_bet():
    """
    Get a valid outside bet.
    
    This function handles bets on properties like red/black, odd/even, etc.
    
    Returns:
        tuple: (bet_type, bet_value, description) where:
            - bet_type is the type of bet (e.g., "red", "odd", "high")
            - bet_value is None for these types (not applicable)
            - description is a text description of the bet for display
    """
    while True:
        print("\n=== OUTSIDE BET OPTIONS ===")
        print("1. Red - Bet on any red number (pays 1:1)")
        print("2. Black - Bet on any black number (pays 1:1)")
        print("3. Odd - Bet on any odd number (pays 1:1)")
        print("4. Even - Bet on any even number (pays 1:1)")
        print("5. Low (1-18) - Bet on numbers 1-18 (pays 1:1)")
        print("6. High (19-36) - Bet on numbers 19-36 (pays 1:1)")
        print("7. Return to main betting menu")
        
        choice = input("\nEnter your choice (1-7): ").lower()
        
        # Check if player wants to quit
        if choice in ['quit', 'q', 'exit']:
            if confirm_quit():
                return None, None, None
            else:
                continue
                
        if choice == '1':
            return 'red', None, "Red bet"
        elif choice == '2':
            return 'black', None, "Black bet"
        elif choice == '3':
            return 'odd', None, "Odd bet"
        elif choice == '4':
            return 'even', None, "Even bet"
        elif choice == '5':
            return 'low', None, "Low (1-18) bet"
        elif choice == '6':
            return 'high', None, "High (19-36) bet"
        elif choice == '7':
            return 'return_to_main', None, None
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

def place_bets(rocks):
    """
    Place bets on the roulette table.
    
    This function handles the betting process, allowing the player to place 
    multiple bets on different outcomes, up to their available Rocks balance.
    
    Args:
        rocks (int): The player's current rock balance
        
    Returns:
        tuple: (remaining_rocks, bets) where:
            - remaining_rocks is the player's remaining balance after placing bets
            - bets is a list of (bet_type, bet_value, bet_amount, description) tuples
    """
    bets = []
    remaining_rocks = rocks
    
    while remaining_rocks > 0:
        print(colorText("\n=== BETTING MENU ===", "yellow"))
        print("1. Place Number Bets (straight, split, street, corner)")
        print("2. Place Outside Bets (red/black, odd/even, high/low)")
        print("3. View Current Bets")
        print("4. Finish Betting and Spin the Wheel")
        print(colorText("\nQuick betting available! Examples:", "cyan"))
        print("quick:red 10   - Bet 10 Rocks on red")
        print("quick:even 20  - Bet 20 Rocks on even numbers")
        print("quick:0 5      - Bet 5 Rocks on zero")
        print(colorText("\nPercentage betting available! Examples:", "cyan"))
        print("quick:red 50%  - Bet 50% of your Rocks on red")
        print("quick:black 30% - Bet 30% of your Rocks on black")
        print("Type 'help' for more options")
        
        # Display current balance ABOVE the input prompt
        print(colorText(f"\nYou have {remaining_rocks} Rocks remaining.", "cyan"))
        
        choice = input(colorText("\nEnter your choice (1-4) or quick bet command: ", "magenta")).lower()
        
        # Process general commands
        handled, result = processCommand(choice, "roulette")
        if handled:
            print(result)
            continue
        
        # Check if player wants to quit
        if choice in ['quit', 'q', 'exit']:
            if confirm_quit():
                return -1, []
            else:
                continue
                
        # Handle quick bet commands
        is_quick_bet, bet_info = processQuickBet(choice, remaining_rocks)
        if is_quick_bet:
            if "error" in bet_info:
                print(colorText(f"Error: {bet_info['error']}", "red"))
                continue
                
            if bet_info["amount"] is None:
                # Get the amount if not specified in the command
                bet_amount = get_valid_bet_amount(remaining_rocks)
                if bet_amount == -1:  # Player chose to quit
                    return -1, []
            else:
                bet_amount = bet_info["amount"]
                if bet_amount > remaining_rocks:
                    print(colorText(f"You only have {remaining_rocks} Rocks available.", "red"))
                    continue
                    
            # Process the main bet
            bet_type = bet_info["type"]
            bet_value = bet_info.get("value", None)
            description = bet_info["description"]
            
            # Indicate if this is a percentage bet
            percentage_text = ""
            if bet_info.get("is_percentage", False):
                percentage_text = f" ({bet_amount / rocks * 100:.0f}%)"
            
            bets.append((bet_type, bet_value, bet_amount, description))
            remaining_rocks -= bet_amount
            print(colorText(f"Quick bet placed: {description} - {bet_amount}{percentage_text} Rocks", "green"))
            
            # Process any additional bets (for multiple bets separated by semicolons)
            if "additional_bets" in bet_info and remaining_rocks > 0:
                for additional_bet in bet_info["additional_bets"]:
                    add_bet_type = additional_bet["type"]
                    add_bet_value = additional_bet.get("value", None)
                    add_bet_desc = additional_bet["description"]
                    add_bet_amount = additional_bet["amount"]
                    
                    # Skip if not enough rocks remaining
                    if add_bet_amount > remaining_rocks:
                        print(colorText(f"Skipping bet on {add_bet_desc} - Not enough Rocks remaining", "red"))
                        continue
                    
                    # Add percentage text if needed
                    add_percentage_text = ""
                    if additional_bet.get("is_percentage", False):
                        add_percentage_text = f" ({add_bet_amount / rocks * 100:.0f}%)"
                    
                    bets.append((add_bet_type, add_bet_value, add_bet_amount, add_bet_desc))
                    remaining_rocks -= add_bet_amount
                    print(colorText(f"Additional bet placed: {add_bet_desc} - {add_bet_amount}{add_percentage_text} Rocks", "green"))
            continue
                
        if choice == '1':
            # Number bets
            bet_type, bet_value, description = get_valid_number_bet()
            
            if bet_type is None:  # Player chose to quit
                return -1, []
                
            if bet_type == 'return_to_main':
                continue
                
            bet_amount = get_valid_bet_amount(remaining_rocks)
            
            if bet_amount == -1:  # Player chose to quit
                return -1, []
                
            bets.append((bet_type, bet_value, bet_amount, description))
            remaining_rocks -= bet_amount
            
        elif choice == '2':
            # Outside bets
            bet_type, bet_value, description = get_valid_outside_bet()
            
            if bet_type is None:  # Player chose to quit
                return -1, []
                
            if bet_type == 'return_to_main':
                continue
                
            bet_amount = get_valid_bet_amount(remaining_rocks)
            
            if bet_amount == -1:  # Player chose to quit
                return -1, []
                
            bets.append((bet_type, bet_value, bet_amount, description))
            remaining_rocks -= bet_amount
            
        elif choice == '3':
            # View current bets
            if not bets:
                print("\nNo bets placed yet.")
            else:
                print("\n=== CURRENT BETS ===")
                total_bet = 0
                for i, (bet_type, bet_value, bet_amount, description) in enumerate(bets, 1):
                    print(f"{i}. {description} - {bet_amount} Rocks")
                    total_bet += bet_amount
                print(f"\nTotal bet: {total_bet} Rocks")
                
        elif choice == '4':
            # Finish betting
            if not bets:
                print("\nYou must place at least one bet before spinning.")
            else:
                return remaining_rocks, bets
                
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
            
        # Break if player has no more rocks to bet
        if remaining_rocks <= 0:
            print("\nYou have no more Rocks to bet.")
            if not bets:
                print("You must place at least one bet to play.")
                return rocks, []
            else:
                break
                
    return remaining_rocks, bets

def display_game_rules():
    """
    Display the rules of the Roulette game.
    
    Returns:
        None: This function just prints information
    """
    print("\n" + "=" * 70)
    print(" " * 25 + "ROULETTE RULES")
    print("=" * 70)
    
    print("\nRoulette is a game where you bet on where a ball will land on a spinning wheel.")
    print("The wheel has numbers 0-36, with 0 being green, and the rest being red or black.")
    
    print("\nBetting Options:")
    print("- Inside Bets (Higher Payout):")
    print("  • Straight Up: Bet on a single number (pays 35:1)")
    print("  • Split: Bet on two adjacent numbers (pays 17:1)")
    print("  • Street: Bet on three numbers in a row (pays 11:1)")
    print("  • Corner: Bet on four numbers that form a square (pays 8:1)")
    
    print("\n- Outside Bets (Lower Payout):")
    print("  • Red/Black: Bet on all red or all black numbers (pays 1:1)")
    print("  • Odd/Even: Bet on all odd or all even numbers (pays 1:1)")
    print("  • Low/High: Bet on numbers 1-18 or 19-36 (pays 1:1)")
    
    print("\nNote: If the ball lands on 0 (green), all outside bets lose.")
    print("You can place multiple bets in a single round.")
    
    print("\nFor example, if you bet 10 Rocks on Straight Up and win, you'd get 360 Rocks back:")
    print("  • Your original 10 Rocks + (10 Rocks × 35) = 360 Rocks")
    
    print("\nType 'quit' or 'q' at any prompt to exit the game.")
    print("-" * 70)

def process_bet_results(bets, winning_number, rocks_before_betting):
    """
    Process the results of all placed bets after the wheel spin.
    
    Args:
        bets (list): List of (bet_type, bet_value, bet_amount, description) tuples
        winning_number (int): The winning number from the wheel spin
        rocks_before_betting (int): The player's rock balance before placing any bets
        
    Returns:
        tuple: (int, bool) - (The player's new rock balance, True if player won this round)
    """
    winning_color = get_color(winning_number)
    total_winnings = 0
    new_balance = rocks_before_betting
    any_win = False
    
    # Get the winning number's display with color
    if winning_color == "red":
        number_display = colorText(f"{winning_number} {winning_color.upper()}", "red")
    elif winning_color == "black":
        number_display = colorText(f"{winning_number} {winning_color.upper()}", "white")
    else:  # green (0)
        number_display = colorText(f"{winning_number} {winning_color.upper()}", "green")
    
    for bet_type, bet_value, bet_amount, description in bets:
        win = check_win(bet_type, bet_value, winning_number)
        new_balance -= bet_amount  # Deduct the bet amount from balance
        
        if win:
            any_win = True
            payout = calculate_payout(bet_type, bet_amount)
            total_winnings += payout
            new_balance += payout
            win_text = colorText(f"\nWIN! {description} - Won {payout} Rocks (Bet: {bet_amount}, Payout: {payout-bet_amount})", "green")
            print(win_text)
        else:
            loss_text = colorText(f"\nLOSS! {description} - Lost {bet_amount} Rocks", "red")
            print(loss_text)
    
    net_profit = new_balance - rocks_before_betting
    print(f"\nResult: {number_display}")
    
    if net_profit > 0:
        result_text = colorText(f"Congratulations! You won a total of {net_profit} Rocks!", "green")
        print(result_text)
    elif net_profit < 0:
        result_text = colorText(f"Too bad! You lost a total of {abs(net_profit)} Rocks.", "red")
        print(result_text)
    else:
        print("You broke even - no Rocks gained or lost.")
    
    # Update win streak if player won overall
    if any_win and net_profit > 0:
        # Get current streak
        current_streak, max_streak = getStreakData("roulette")
        current_streak += 1
        max_streak = max(current_streak, max_streak)
        
        # Save updated streak
        saveStreakData("roulette", current_streak, max_streak)
        
        # Check for streak rewards
        reward_amount, message = getWinStreakReward(current_streak, "roulette")
        if reward_amount > 0:
            print(message)
            new_balance += reward_amount
            
        streak_info = colorText(f"Current win streak: {current_streak}", "cyan")
        print(streak_info)
    elif net_profit <= 0:
        # Reset streak on loss
        saveStreakData("roulette", 0, getStreakData("roulette")[1])
        
    print(colorText(f"New balance: {new_balance} Rocks", "cyan"))
    
    return new_balance, any_win and net_profit > 0

def play_roulette(initial_rocks=100):
    """
    Main function to run the Roulette game.
    
    This function handles the overall game flow, including:
    - Displaying rules
    - Managing the betting process
    - Spinning the wheel
    - Processing wins and losses
    - Tracking the player's rock balance
    - Managing the play again loop
    - Tracking win streaks and providing rewards
    
    Args:
        initial_rocks (int): Starting number of Rocks for the player
        
    Returns:
        int: The final number of Rocks the player has, or -1 if they quit
    """
    rocks = initial_rocks
    display_game_rules()
    
    # Welcome message with win streak info
    streak_data = getStreakData("roulette")
    current_streak, max_streak = streak_data
    if max_streak > 0:
        print(colorText(f"\nWelcome back! Your longest win streak is {max_streak}.", "cyan"))
        if current_streak > 0:
            print(colorText(f"Current win streak: {current_streak}", "green"))
            print(colorText("Keep winning to earn streak rewards!", "yellow"))
    
    while True:
        print(colorText(f"\nYou have {rocks} Rocks.", "cyan"))
        
        # Check if player has enough rocks to continue
        if rocks <= 0:
            print(colorText("\nYou're out of Rocks!", "red"))
            emergency_rocks = 50
            print(colorText(f"Here's an emergency {emergency_rocks} Rocks to keep playing.", "green"))
            rocks = emergency_rocks
            
        # Display the roulette board
        display_roulette_board()
        
        # Place bets
        rocks_before_betting = rocks
        remaining_rocks, bets = place_bets(rocks)
        
        if remaining_rocks == -1:  # Player chose to quit
            return -1
            
        if not bets:  # No bets were placed
            continue
            
        # Update rocks for betting
        rocks = remaining_rocks
        
        # Spin the wheel
        winning_number = spin_wheel()
        
        # Process bet results and track wins
        rocks, win = process_bet_results(bets, winning_number, rocks_before_betting)
        
        # Ask to play again
        print("\nDo you want to play another round?")
        while True:
            play_again = input("Enter 'y' to continue or 'n' to exit (or type 'help' for options): ").lower()
            
            # Process general commands
            handled, result = processCommand(play_again, "roulette")
            if handled:
                print(result)
                continue
                
            if play_again in ['y', 'yes']:
                break
            elif play_again in ['n', 'no', 'quit', 'q', 'exit']:
                print(colorText("\nThanks for playing Roulette! Goodbye!", "cyan"))
                
                # Show final stats
                streak_data = getStreakData("roulette")
                _, max_streak = streak_data
                if max_streak > 0:
                    print(colorText(f"Your best win streak was: {max_streak}", "yellow"))
                    
                if rocks > initial_rocks:
                    profit = rocks - initial_rocks
                    print(colorText(f"You're leaving with a profit of {profit} Rocks!", "green"))
                elif rocks < initial_rocks:
                    loss = initial_rocks - rocks
                    print(colorText(f"You're leaving with a loss of {loss} Rocks.", "red"))
                else:
                    print("You broke even!")
                    
                return rocks
            else:
                print("Please enter 'y' to continue or 'n' to exit.")
            
    return rocks

def rouletteLoop():
    """
    Entry point for the Roulette game.
    
    This function serves as the main entry point when the game is selected
    from the game selector menu or run directly. It provides a clean interface
    for external modules to start the game.
    
    Returns:
        None: This function doesn't return a value, but starts the Roulette game
    """
    try:
        play_roulette()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Exiting Roulette...")
        time.sleep(1)
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        print("Exiting Roulette...")
        time.sleep(1)
        sys.exit(1)

if __name__ == "__main__":
    rouletteLoop()
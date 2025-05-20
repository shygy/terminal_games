"""
MasterMind (Code Breaker) Game Module

This module implements a classic MasterMind code-breaking game where:
- Player tries to guess a secret code of digits (0-9)
- Player can choose the length of the code (1-10 digits)
- After each guess, player receives feedback on:
  * How many digits are correct and in the right position
  * How many digits are correct but in the wrong position
- Player can choose between two game modes:
  * Standard: Code can contain repeated digits
  * No Repeats: Code contains unique digits only

The game tracks the number of attempts and provides an option
to reveal the code if the player gives up.
"""

import random
import sys
import time

def generate_code(code_length, allow_repeats=True):
    """
    Generate a random secret code.
    
    Args:
        code_length (int): Length of the code to generate
        allow_repeats (bool): Whether repeated digits are allowed in the code
        
    Returns:
        list: A list of digits (as strings) representing the secret code
    
    Example:
        >>> generate_code(4, True)  # Might return ['1', '3', '3', '7']
        >>> generate_code(4, False)  # Might return ['2', '5', '0', '9']
    """
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    
    if allow_repeats:
        # With repeats, we simply choose random digits with replacement
        return random.choices(digits, k=code_length)
    else:
        # Without repeats, we sample unique digits
        if code_length > len(digits):
            raise ValueError("Code length cannot exceed the number of available digits when repeats are not allowed")
        return random.sample(digits, k=code_length)

def evaluate_guess(guess, secret_code):
    """
    Evaluate a guess against the secret code and provide feedback.
    
    Args:
        guess (list): The player's guess as a list of digits (strings)
        secret_code (list): The secret code as a list of digits (strings)
        
    Returns:
        tuple: (correct_position, correct_digit) where:
            - correct_position: Number of digits that are correct and in the right position
            - correct_digit: Number of digits that are correct but in the wrong position
            
    Example:
        >>> evaluate_guess(['1', '2', '3', '4'], ['1', '3', '5', '6'])
        (1, 1)  # '1' is in correct position, '3' is correct but wrong position
    """
    # Create copies to avoid modifying the original lists
    guess_copy = guess.copy()
    code_copy = secret_code.copy()
    
    # First, count exact matches (correct position)
    correct_position = 0
    for i in range(len(guess)):
        if i < len(code_copy) and guess[i] == secret_code[i]:
            correct_position += 1
            # Mark matched positions as None to avoid counting them twice
            guess_copy[i] = None
            code_copy[i] = None
    
    # Next, count digits that are correct but in wrong positions
    correct_digit = 0
    for i in range(len(guess_copy)):
        if guess_copy[i] is not None:  # Skip already matched positions
            for j in range(len(code_copy)):
                if code_copy[j] is not None and guess_copy[i] == code_copy[j]:
                    correct_digit += 1
                    code_copy[j] = None  # Mark as counted
                    break
    
    return (correct_position, correct_digit)

def display_game_rules(code_length, allow_repeats=True):
    """
    Display the rules of the MasterMind game.
    
    Args:
        code_length (int): The length of the secret code
        allow_repeats (bool): Whether the game allows repeated digits
        
    Returns:
        None: This function just prints information
    """
    print("\n=== MASTERMIND (CODE BREAKER) ===")
    print(f"I'm thinking of a {code_length}-digit code using digits 0-9.")
    
    if allow_repeats:
        print("This game mode allows repeated digits in the code.")
    else:
        print("This game mode uses only unique digits in the code (but you can still")
        print("enter repeated digits in your guesses).")
        
    print("Try to guess it in as few attempts as possible.")
    print("\nAfter each guess, you'll receive feedback:")
    print("- Digits in the correct position")
    print("- Digits that are correct but in the wrong position")
    print("\nFor example, if the secret code is 1234 and you guess 1357:")
    print("- You have 1 digit correct and in the right position (the 1)")
    print("- You have 1 digit correct but in the wrong position (the 3)")
    print("\nSpecial commands:")
    print("- Type 'h', 'his', or 'history' to review your previous guesses")
    print("- Type 'quit' or 'q' at any time to exit the game")
    print("- Type 'reveal' if you want to see the secret code")
    print("=" * 36 + "\n")

def confirm_quit():
    """
    Asks the user to confirm if they want to quit the game.
    
    Returns:
        bool: True if the user confirms quitting, False otherwise
    """
    while True:
        confirm = input("Confirm quit? (y/n): ").lower()
        if confirm in ['y', 'yes']:
            print("\nThanks for playing Mastermind! Goodbye!")
            return True
        elif confirm in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' or 'n'.")

def display_guess_history(history):
    """
    Display the guess history to the player.
    
    Args:
        history (list): List of tuples containing (guess, correct_pos, correct_digit)
        
    Returns:
        None: This function just prints the guess history
    """
    if not history:
        print("\nNo guesses made yet.")
        return
        
    print("\n=== GUESS HISTORY ===")
    for i, (guess, correct_pos, correct_digit) in enumerate(history):
        print(f"Guess #{i+1} | {''.join(guess)} | {correct_pos} Right Spot, {correct_digit} Wrong Spot")
    print("=" * 20)

def play_mastermind():
    """
    Main function to run the MasterMind game.
    
    This function handles:
    - Game setup with different modes (with/without repeats)
    - Custom code length selection (1-10 digits)
    - Processing player guesses
    - Providing feedback on guesses
    - Tracking game progress until win or quit
    - History tracking with "h" or "history" command
    - Option to play again
    
    Returns:
        None: This function doesn't return a value
    """
    while True:
        # Game setup
        print("\nWelcome to MasterMind (Code Breaker)!")
        print("Try to break the secret code.")
        
        # Let player choose code length with validation
        while True:
            try:
                length_input = input("\nChoose code length (1-9, or 0 for 10 digits): ").lower()
                
                # Check if player wants to quit
                if length_input in ['quit', 'q', 'exit']:
                    if confirm_quit():
                        return
                    else:
                        continue
                
                code_length = int(length_input)
                
                # Special handling for 0 to mean 10 digits
                if code_length == 0:
                    code_length = 10
                    print("Setting code length to 10 digits.")
                
                if 1 <= code_length <= 10:
                    break
                else:
                    print("Please enter a number between 0 and 9 (0 means 10 digits).")
            except ValueError:
                print("Please enter a valid number.")
        
        # Let player choose game mode with validation
        while True:
            mode_input = input("\nAllow repeated digits? (y/n): ").lower()
            
            # Check if player wants to quit
            if mode_input in ['quit', 'q', 'exit']:
                if confirm_quit():
                    return
                else:
                    continue
            
            if mode_input in ['y', 'yes', 'n', 'no']:
                allow_repeats = mode_input in ['y', 'yes']
                break
            else:
                print("Please enter 'y' or 'n'.")
        
        # Generate the secret code based on player's choices
        secret_code = generate_code(code_length, allow_repeats)
        
        # Display game rules
        display_game_rules(code_length, allow_repeats)
        
        # Main game loop
        attempts = 0
        max_attempts = 12  # Standard maximum for traditional Mastermind
        guess_history = []  # Track history of guesses and results
        
        while attempts < max_attempts:
            attempts += 1
            print(f"\nAttempt {attempts}/{max_attempts}")
            
            # Get player's guess with validation
            guess = None  # Initialize guess variable
            revealed = False  # Initialize revealed flag
            
            while True:
                guess_input = input(f"Enter your {code_length}-digit guess (or 'h'/'his'/'history' to view previous guesses): ").lower()
                
                # Check if player wants to see guess history
                if guess_input in ['h', 'his', 'history']:
                    display_guess_history(guess_history)
                    continue
                
                # Check if player wants to quit
                if guess_input in ['quit', 'q', 'exit']:
                    if confirm_quit():
                        return
                    else:
                        continue
                
                # Check if player wants to give up and see the answer
                if guess_input in ['reveal', 'show', 'give up']:
                    confirm = input("\nReveal the code? This will end the game (y/n): ").lower()
                    if confirm in ['y', 'yes']:
                        print(f"\nThe secret code was: {''.join(secret_code)}")
                        revealed = True
                        break
                    else:
                        print("Continue playing! Good luck!")
                        continue
                
                # Validate guess format
                if not guess_input.isdigit():
                    print("Please enter digits only (0-9).")
                    continue
                    
                if len(guess_input) != code_length:
                    print(f"Please enter exactly {code_length} digits.")
                    continue
                
                # Convert guess to list of digits for processing
                guess = list(guess_input)
                
                # No longer restricting user input in no-repeats mode
                # Users can enter repeated digits in their guesses regardless of game mode
                
                break
            
            # If player chose to reveal the code, skip to next iteration
            if revealed:
                revealed_code = True
                break
            
            # Process the guess if we have a valid one
            if guess is not None:
                # Evaluate the guess
                correct_pos, correct_digit = evaluate_guess(guess, secret_code)
                
                # Add the guess and results to history
                guess_history.append((guess, correct_pos, correct_digit))
                
                # Display feedback
                print(f"\nFeedback: {correct_pos} correct position, {correct_digit} correct digit but wrong position")
                
                # Check if player has won
                if correct_pos == code_length:
                    print(f"\nCongratulations! You've cracked the code in {attempts} attempts!")
                    break
        
        # Initialize variable for checking out of attempts
        revealed_code = False
        
        # If player runs out of attempts
        if attempts >= max_attempts:
            print(f"\nOut of attempts! The secret code was: {''.join(secret_code)}")
            revealed_code = True
        
        # Ask to play again
        while True:
            play_again = input("\nDo you want to play again? (y/n): ").lower()
            
            # Check if player wants to quit
            if play_again in ['quit', 'q', 'exit']:
                if confirm_quit():
                    return
                else:
                    continue
            
            if play_again in ['y', 'yes', 'n', 'no']:
                break
            else:
                print("Please enter 'y' or 'n'.")
        
        if play_again not in ['y', 'yes']:
            print("\nThanks for playing Mastermind! Goodbye!")
            break

def mastermindLoop():
    """
    Entry point for the MasterMind game.
    
    This function serves as the main entry point when the game is selected
    from the game selector menu or run directly. It provides a clean interface
    for external modules to start the game.
    
    Returns:
        None: This function doesn't return a value, but starts the MasterMind game
    """
    try:
        play_mastermind()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Exiting Mastermind...")
        time.sleep(1)
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        print("Exiting Mastermind...")
        time.sleep(1)
        sys.exit(1)

if __name__ == "__main__":
    mastermindLoop()
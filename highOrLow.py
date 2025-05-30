"""
Higher or Lower Game Module

This module implements a simple number guessing game where the player
tries to guess a random number between 1 and 10. After each guess,
the player receives feedback about whether the correct number is
higher or lower than their guess.
"""

import random

def confirm_quit():
    """
    Asks the user to confirm if they want to quit the game.
    
    Returns:
        bool: True if the user confirms quitting, False otherwise
    """
    while True:
        confirm = input("Confirm quit? (y/n): ").lower()
        if confirm in ['y', 'yes']:
            print("\nThanks for playing shygyGames! Goodbye!")
            return True
        elif confirm in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' or 'n'.")

def play_highOrLow():
    """
    Run the Higher or Lower game in interactive mode.
    
    This function handles the main game loop, including generating a random number,
    processing player guesses, providing feedback, tracking guesses, and allowing
    the player to play multiple rounds.
    
    Returns:
        None
    """
    print("\n=== Welcome to Higher or Lower! ===\n")
    
    while True:
        print("Let's play a round!")
        # Generate a random number between 1 and 10 (inclusive)
        compChoice = random.randint(1, 10)
        guesses = 1
        
        # Get the first player guess with input validation
        while True:
            try:
                userInput = input("I'm thinking of a number between 1 and 10 inclusive. Make a guess: ")
                
                # Check if user wants to quit
                if userInput.lower() in ['quit', 'q', 'exit']:
                    if confirm_quit():
                        return
                    else:
                        continue
                        
                userChoice = int(userInput)
                if userChoice < 1 or userChoice > 10:
                    print("Please enter a number between 1 and 10.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 10.")
        
        # Main guessing loop
        while userChoice != compChoice:
            if userChoice < compChoice:
                hint = f"Higher than {userChoice}. Guess again: "
            else:
                hint = f"Lower than {userChoice}. Guess again: "
            
            # Get subsequent guesses with input validation
            while True:
                try:
                    userInput = input(hint)
                    
                    # Check if user wants to quit
                    if userInput.lower() in ['quit', 'q', 'exit']:
                        if confirm_quit():
                            return
                        else:
                            # Show the hint again to continue the game
                            continue
                    
                    userChoice = int(userInput)
                    if userChoice < 1 or userChoice > 10:
                        print("Please enter a number between 1 and 10.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter a number between 1 and 10.")
            
            guesses += 1
        
        # Display win message based on number of guesses
        if guesses == 1:
            print(f"Wow! The number was {compChoice}. You got it first try!")
        else:
            print(f"Well done! The number was {compChoice}. You got it in {guesses} guesses.")
            
            # Provide additional feedback based on performance
            if guesses <= 3:
                print("That's excellent guessing!")
            elif guesses <= 5:
                print("Good job!")
        
        # Ask to play again with input validation
        while True:
            play_again = input("Would you like to play again? (y/n): ").lower()
            if play_again in ['y', 'n', 'yes', 'no']:
                break
            elif play_again in ['quit', 'q', 'exit']:
                if confirm_quit():
                    return
                else:
                    continue
            else:
                print("Invalid input. Please enter Y or N (case insensitive).")
        
        if play_again not in ['y', 'yes']:
            print("\nThanks for playing Higher or Lower!\n")
            break

if __name__ == "__main__":
    play_highOrLow()
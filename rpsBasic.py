"""
Rock Paper Scissors Game Module

This module implements a simple Rock Paper Scissors game where the player
competes against the computer. The game follows standard Rock Paper Scissors rules:
- Rock beats Scissors
- Scissors beats Paper
- Paper beats Rock
"""

import random

def rps(user, comp):
    """
    Determine the winner of a Rock Paper Scissors round.
    
    Args:
        user (str): The player's choice ('r', 'p', or 's')
        comp (str): The computer's choice ('r', 'p', or 's')
        
    Returns:
        str: A message indicating the result of the game (win, loss, tie, or invalid input)
    """
    user = user.lower()
    
    if user == comp:
        return "It's a tie."
    elif user == 'r':
        return "You win." if comp == 's' else "Computer wins."
    elif user == 'p':
        return "You win." if comp == 'r' else "Computer wins."
    elif user == 's':
        return "You win." if comp == 'p' else "Computer wins."
    else:
        return "Invalid input. Please enter R, P, or S (case insensitive)."

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

def play_rps():
    """
    Run the Rock Paper Scissors game in interactive mode.
    
    This function handles user input, generates the computer's choice,
    displays the results, and manages the game loop.
    
    Returns:
        None
    """
    rps_choices = ['r', 'p', 's']
    choice_full_names = {'r': 'Rock', 'p': 'Paper', 's': 'Scissors'}
    
    print("\n=== Welcome to Rock Paper Scissors! ===\n")
    
    while True:
        # Get player choice with improved error handling
        while True:
            userRPS = input("Choose: Rock (R), Paper (P), or Scissors (S): ").lower()
            
            # Check if the user wants to quit
            if userRPS in ['quit', 'q', 'exit']:
                if confirm_quit():
                    return
                else:
                    continue
                    
            if userRPS in ['r', 'p', 's'] or userRPS in ['rock', 'paper', 'scissors']:
                # Convert full word inputs to single letter
                if userRPS == 'rock': userRPS = 'r'
                elif userRPS == 'paper': userRPS = 'p'
                elif userRPS == 'scissors': userRPS = 's'
                break
            else:
                print("Invalid input. Please enter R, P, or S (case insensitive).")
        
        # Generate computer choice
        compSelection = random.choice(rps_choices)
        
        # Display choices
        print(f"You chose: {choice_full_names[userRPS]}")
        print(f"Computer chose: {choice_full_names[compSelection]}")
        
        # Determine and display result
        result = rps(userRPS, compSelection)
        print(result)
        
        # Ask to play again with improved error handling
        while True:
            play_again = input("Play again? (y/n): ").lower()
            
            # Check if the user wants to quit
            if play_again in ['quit', 'q', 'exit']:
                if confirm_quit():
                    return
                else:
                    continue
                    
            if play_again in ['y', 'n', 'yes', 'no']:
                break
            else:
                print("Invalid input. Please enter Y or N (case insensitive).")
        
        if play_again not in ['y', 'yes']:
            print("\nThanks for playing Rock Paper Scissors!\n")
            break

if __name__ == "__main__":
    play_rps()
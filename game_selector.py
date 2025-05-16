"""
Game Selector Module

This module provides a menu-driven interface for selecting and playing
various terminal games in the shygyGames collection.
"""

import os
import sys
import time
from highOrLow import play_highOrLow
from rpsBasic import play_rps
from hangman import hangmanLoop
from blackJack import mainBlackjack

def clear_screen():
    """
    Clear the terminal screen based on the operating system.
    
    Returns:
        None
    """
    # Check the operating system and use appropriate command
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix/Linux/MacOS
        os.system('clear')

def display_header():
    """
    Display a decorative header for the game menu.
    
    Returns:
        None
    """
    clear_screen()
    print("="*60)
    print("                    shygyGames Collection")
    print("="*60)
    print("       A collection of classic terminal games to enjoy!")
    print("-"*60)

def main():
    """
    Run the main game selector menu.
    
    This function displays a menu of available games, handles user input
    for game selection, and launches the selected game. It loops until the
    user chooses to exit.
    
    Returns:
        None
    """
    while True:
        display_header()
        
        # Display game menu
        print("\nAvailable Games:")
        print("  1. Higher or Lower - Guess the correct number")
        print("  2. Rock Paper Scissors - Classic hand game")
        print("  3. Hangman - Word guessing challenge")
        print("  4. Blackjack - Card game with betting")
        print("  5. Exit\n")
        
        # Get user choice with input validation
        while True:
            try:
                choice = input("Select a game (1-5) or type 'quit' to exit: ")
                
                # Check if user wants to quit
                if choice.lower() in ['quit', 'q', 'exit']:
                    print("Thanks for playing shygyGames! Goodbye!")
                    time.sleep(1)
                    sys.exit(0)
                    
                if choice in ['1', '2', '3', '4', '5']:
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 5.")
            except KeyboardInterrupt:
                print("\nGame selection interrupted. Exiting...")
                sys.exit(0)
            except Exception as e:
                print(f"An error occurred: {str(e)}. Please try again.")
        
        # Process user choice
        if choice == '1':
            try:
                play_highOrLow()
            except Exception as e:
                print(f"An error occurred while playing Higher or Lower: {str(e)}")
                input("Press Enter to return to the main menu...")
        elif choice == '2':
            try:
                play_rps()
            except Exception as e:
                print(f"An error occurred while playing Rock Paper Scissors: {str(e)}")
                input("Press Enter to return to the main menu...")
        elif choice == '3':
            try:
                hangmanLoop()
            except Exception as e:
                print(f"An error occurred while playing Hangman: {str(e)}")
                input("Press Enter to return to the main menu...")
        elif choice == '4':
            try:
                mainBlackjack()
            except Exception as e:
                print(f"An error occurred while playing Blackjack: {str(e)}")
                input("Press Enter to return to the main menu...")
        elif choice == '5':
            print("Thanks for playing shygyGames! Goodbye!")
            # Add a small delay before exiting
            time.sleep(1)
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
        sys.exit(0)
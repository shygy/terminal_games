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
from masterMind import mastermindLoop
from roulette import rouletteLoop
from blackJack import mainBlackjack

def clearScreen():
    """
    Clear the terminal screen based on the operating system.
    
    This function detects the operating system and uses the appropriate
    command to clear the terminal screen for a better user experience.
    
    Returns:
        None
    
    Examples:
        >>> clearScreen()  # Screen will be cleared
    """
    # Check the operating system and use appropriate command
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix/Linux/MacOS
        os.system('clear')

def displayHeader():
    """
    Display a decorative header for the game menu.
    
    This function prints a formatted header including the collection name,
    welcome message, and instructions for the game selector menu.
    
    Returns:
        None
    
    Examples:
        >>> displayHeader()  # Displays the header with welcome message
    """
    clearScreen()
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
        displayHeader()
        
        # Display game menu
        print("\nAvailable Games:")
        print("  1. Higher or Lower - Guess the correct number")
        print("  2. Rock Paper Scissors - Classic hand game")
        print("  3. Hangman - Word guessing challenge")
        print("  4. MasterMind - Code breaking puzzle")
        print("  5. Roulette - Wheel of fortune with betting options")
        print("  6. Blackjack - Card game with betting")
        print("  7. Exit\n")
        
        # Get user choice with input validation
        while True:
            try:
                choice = input("Select a game (1-6) or type 'quit' to exit: ")
                
                # Check if user wants to quit
                if choice.lower() in ['quit', 'q', 'exit']:
                    print("Thanks for playing shygyGames! Goodbye!")
                    time.sleep(1)
                    sys.exit(0)
                    
                if choice in ['1', '2', '3', '4', '5', '6', '7']:
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 7.")
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
                mastermindLoop()
            except Exception as e:
                print(f"An error occurred while playing Mastermind: {str(e)}")
                input("Press Enter to return to the main menu...")
        elif choice == '5':
            try:
                rouletteLoop()
            except Exception as e:
                print(f"An error occurred while playing Roulette: {str(e)}")
                input("Press Enter to return to the main menu...")
        elif choice == '6':
            try:
                mainBlackjack()
            except Exception as e:
                print(f"An error occurred while playing Blackjack: {str(e)}")
                input("Press Enter to return to the main menu...")
        elif choice == '7':
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
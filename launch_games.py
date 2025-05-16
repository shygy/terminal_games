#!/usr/bin/env python3
"""
Game Launcher - Run this script to start the shygyGames terminal collection.

This script serves as the entry point for the shygyGames terminal collection.
It sets up the Python environment, handles imports, and launches the game selector
menu where users can choose which game to play.

Usage:
    python launch_games.py
"""

import os
import sys
import time
import traceback

def clear_screen():
    """
    Clear the terminal screen based on operating system.
    
    This function detects the operating system and uses the appropriate
    command to clear the terminal screen for better user experience.
    
    Returns:
        None
    """
    try:
        # Use cls for Windows, clear for Unix/Linux/MacOS
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception:
        # If screen clearing fails, print newlines as a fallback
        print('\n' * 100)

def display_header():
    """
    Display a decorative header for the game launcher.
    
    Creates a visually appealing header with the collection name and welcome message.
    
    Returns:
        None
    """
    print("\n" + "=" * 70)
    print(" " * 23 + "SHYGYGAMES COLLECTION")
    print("=" * 70)
    print("\nWelcome to the shygyGames Terminal Collection!")
    print("A collection of classic text-based games featuring advanced gameplay options.")
    print("-" * 70)
    print("\nGames include Higher or Lower, Rock Paper Scissors, Hangman, and Blackjack")
    print("with advanced betting options (split, double down, and insurance).")
    print("-" * 70)
    # Small delay for better user experience
    time.sleep(0.5)

def check_environment():
    """
    Check if the Python environment is properly set up.
    
    Verifies Python version and required modules to ensure the games
    will run correctly.
    
    Returns:
        bool: True if environment is correctly set up, False otherwise
    """
    # Check Python version
    required_version = (3, 6)
    current_version = sys.version_info[:2]
    
    if current_version < required_version:
        print(f"Error: Python {required_version[0]}.{required_version[1]} or higher is required.")
        print(f"Current version: Python {current_version[0]}.{current_version[1]}")
        return False
    
    # Check required modules
    required_modules = ['random', 'time', 'os', 'sys']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"Error: The following required modules are missing: {', '.join(missing_modules)}")
        return False
    
    return True

def main():
    """
    Main function to run the game launcher.
    
    This function handles:
    1. Environment setup and validation
    2. Path configuration for game imports
    3. Loading the game selector
    4. Error handling for various failure scenarios
    
    Returns:
        None
    """
    # Check if environment is properly setup
    if not check_environment():
        print("Please fix the environment issues and try again.")
        input("Press Enter to exit...")
        return
    
    try:
        # Add the current directory to the Python path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, current_dir)
        
        # Import the game selector
        try:
            from game_selector import main as game_selector_main
            
            clear_screen()
            display_header()
            
            # Small delay for better user experience
            time.sleep(1)
            
            # Run the game selector
            game_selector_main()
            
        except ImportError as e:
            print(f"Error: Could not import the game_selector module. {e}")
            print(f"Make sure the file 'game_selector.py' exists in: {current_dir}")
            print("\nPossible solutions:")
            print("1. Ensure game_selector.py is in the same directory as this script")
            print("2. Check for typos in import statements")
            print("3. Verify all required game files are present")
            input("\nPress Enter to exit...")
            
    except KeyboardInterrupt:
        clear_screen()
        print("\nGame launcher was interrupted. Thanks for playing!")
        time.sleep(1)
        
    except Exception as e:
        print(f"\nError: An unexpected error occurred while launching games.\nDetails: {e}")
        print("\nDebug information:")
        traceback.print_exc()
        print("\nPlease report this issue with the above error details.")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print("\nThanks for playing shygyGames! Goodbye!")
    except Exception as e:
        print(f"\nCritical error: {e}")
        traceback.print_exc()
        input("\nPress Enter to exit...")
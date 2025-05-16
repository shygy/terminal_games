#!/usr/bin/env python3
"""
Game Launcher - Run this script to start the game collection.
"""
import os
import sys

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header():
    """Display a header for the launcher."""
    print("\n" + "=" * 60)
    print(" " * 18 + "TERMINAL GAMES COLLECTION")
    print("=" * 60)
    print("\nWelcome to the Terminal Games Collection!")
    print("Select a game to play from the menu below.")
    print("-" * 60)

def main():
    """Main function to run the game launcher."""
    # Add the games directory to the Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    games_dir = os.path.join(current_dir, "games")
    sys.path.insert(0, games_dir)
    
    # Change working directory to games dir so relative paths work
    os.chdir(games_dir)
    
    # Import the game selector
    try:
        from game_selector import main as game_selector_main
        
        clear_screen()
        display_header()
        
        # Run the game selector
        game_selector_main()
    except ImportError as e:
        print(f"Error: Could not import the game_selector module. {e}")
        print(f"Make sure the file 'game_selector.py' exists in: {games_dir}")
    except KeyboardInterrupt:
        print("\nThanks for playing! Goodbye!")
    except Exception as e:
        print(f"Error: An unexpected error occurred. {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
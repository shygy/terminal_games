#!/usr/bin/env python3
"""
Number Guessing Game - A simple terminal-based game where you guess a number.
"""
import random
import os
import time

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header():
    """Display a header for the game."""
    print("\n" + "=" * 60)
    print(" " * 20 + "NUMBER GUESSING GAME")
    print("=" * 60)
    print("\nGuess a number between 1 and 10")
    print("Try to get it in as few attempts as possible!")
    print("-" * 60)

def play_game():
    """Play one round of the number guessing game."""
    # Select a random number between 1 and 10
    target = random.randint(1, 10)
    attempts = 0
    guessed = False
    
    # Game statistics
    stats = {'total_guesses': 0, 'games_played': 0, 'best_score': float('inf')}
    
    # Try to load stats if they exist
    try:
        if os.path.exists("number_game_stats.txt"):
            with open("number_game_stats.txt", "r") as f:
                data = f.read().strip().split(",")
                stats['total_guesses'] = int(data[0])
                stats['games_played'] = int(data[1])
                stats['best_score'] = int(data[2])
    except:
        # If there's any error, just use default stats
        pass
    
    # Main game loop
    while not guessed:
        try:
            guess = input("\nEnter your guess (1-10): ")
            
            # Check if user wants to quit
            if guess.lower() in ['q', 'quit', 'exit']:
                print("\nThanks for playing!")
                return
            
            guess = int(guess)
            
            if guess < 1 or guess > 10:
                print("Please enter a number between 1 and 10.")
                continue
            
            attempts += 1
            
            if guess == target:
                guessed = True
                print(f"\n🎉 Correct! The number was {target}.")
                print(f"You got it in {attempts} {'attempt' if attempts == 1 else 'attempts'}!")
                
                # Update stats
                stats['total_guesses'] += attempts
                stats['games_played'] += 1
                stats['best_score'] = min(stats['best_score'], attempts)
                
                # Calculate and display average
                avg = stats['total_guesses'] / stats['games_played']
                print(f"\nYour stats:")
                print(f"Games played: {stats['games_played']}")
                print(f"Average attempts: {avg:.2f}")
                print(f"Best score: {stats['best_score']}")
                
                # Save stats
                try:
                    with open("number_game_stats.txt", "w") as f:
                        f.write(f"{stats['total_guesses']},{stats['games_played']},{stats['best_score']}")
                except:
                    pass
            
            elif guess < target:
                print(f"Higher than {guess}!")
            else:
                print(f"Lower than {guess}!")
                
        except ValueError:
            print("Please enter a valid number.")
            continue

def main():
    """Main function to run the game with a play again loop."""
    playing = True
    
    while playing:
        clear_screen()
        display_header()
        play_game()
        
        again = input("\nPlay again? (y/n): ").lower()
        playing = again.startswith('y')
    
    print("\nThanks for playing! Goodbye!\n")

if __name__ == "__main__":
    main()
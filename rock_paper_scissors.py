#!/usr/bin/env python3
"""
Rock Paper Scissors - A classic terminal-based game against the computer.
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
    print(" " * 20 + "ROCK PAPER SCISSORS")
    print("=" * 60)
    print("\nChoose Rock (R), Paper (P), or Scissors (S)")
    print("Rock beats Scissors, Scissors beats Paper, Paper beats Rock")
    print("-" * 60)

def get_choice_name(choice):
    """Convert the choice code to a readable name."""
    if choice == 'r':
        return "Rock"
    elif choice == 'p':
        return "Paper"
    elif choice == 's':
        return "Scissors"
    return "Unknown"

def determine_winner(player, computer):
    """Determine the winner based on player and computer choices."""
    if player == computer:
        return "tie"
    elif (player == 'r' and computer == 's') or \
         (player == 'p' and computer == 'r') or \
         (player == 's' and computer == 'p'):
        return "player"
    else:
        return "computer"

def play_game():
    """Play one round of rock paper scissors."""
    score = {'player': 0, 'computer': 0, 'ties': 0}
    
    # Try to load stats if they exist
    try:
        if os.path.exists("rps_game_stats.txt"):
            with open("rps_game_stats.txt", "r") as f:
                data = f.read().strip().split(",")
                score['player'] = int(data[0])
                score['computer'] = int(data[1])
                score['ties'] = int(data[2])
    except:
        # If there's any error, just use default stats
        pass
    
    playing = True
    
    while playing:
        # Display current score
        print(f"\nScore: You - {score['player']} | Computer - {score['computer']} | Ties - {score['ties']}")
        
        # Get player choice
        valid_choices = ['r', 'p', 's']
        player_choice = ""
        
        while player_choice not in valid_choices:
            player_choice = input("\nYour choice (R/P/S or Q to quit): ").lower()
            
            if player_choice == 'q':
                print("\nThanks for playing!")
                return
            
            if player_choice not in valid_choices:
                print("Invalid choice. Please choose R, P, S, or Q.")
        
        # Get computer choice
        computer_choice = random.choice(valid_choices)
        
        # Show choices
        print(f"\nYou chose: {get_choice_name(player_choice)}")
        print(f"Computer chose: {get_choice_name(computer_choice)}")
        
        # Determine winner
        result = determine_winner(player_choice, computer_choice)
        
        if result == "tie":
            print("It's a tie!")
            score['ties'] += 1
        elif result == "player":
            print("You win this round!")
            score['player'] += 1
        else:
            print("Computer wins this round!")
            score['computer'] += 1
        
        # Save stats
        try:
            with open("rps_game_stats.txt", "w") as f:
                f.write(f"{score['player']},{score['computer']},{score['ties']}")
        except:
            pass
        
        # Ask to play again
        again = input("\nPlay another round? (y/n): ").lower()
        if not again.startswith('y'):
            playing = False

def main():
    """Main function to run the game."""
    clear_screen()
    display_header()
    play_game()
    print("\nFinal Score:")
    
    # Try to load and display final stats if they exist
    try:
        if os.path.exists("rps_game_stats.txt"):
            with open("rps_game_stats.txt", "r") as f:
                data = f.read().strip().split(",")
                player = int(data[0])
                computer = int(data[1])
                ties = int(data[2])
                print(f"You: {player} | Computer: {computer} | Ties: {ties}")
                
                if player > computer:
                    print("Congratulations! You're ahead!")
                elif computer > player:
                    print("The computer is winning overall. Try again next time!")
                else:
                    print("It's a tie overall!")
    except:
        pass
    
    print("\nThanks for playing! Goodbye!\n")

if __name__ == "__main__":
    main()
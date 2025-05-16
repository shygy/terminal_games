from highOrLow import play_guessing_game
from rpsBasic import play_rps
from hangman import hangmanLoop
from blackJack import mainBlackjack

def main():
    while True:
        print("\nWelcome to the shygyGames!")
        print("1. Number Guessing Game")
        print("2. Rock Paper Scissors")
        print("3. Hangman")
        print("4. Blackjack")
        print("5. Exit")
        
        choice = input("Select a game (1-5): ")
        
        if choice == '1':
            play_guessing_game()
        elif choice == '2':
            play_rps()
        elif choice =='3':
            hangmanLoop()
        elif choice =='4':
            mainBlackjack()
        elif choice == '5':
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
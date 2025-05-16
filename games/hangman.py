import random

# Import the wordlist from separate file
from wordlist import wordlist

def select_difficulty():
    """Get difficulty selection from user"""
    while True:
        print("\nSelect difficulty:")
        print("1. Easy (26 guesses)")
        print("2. Medium (word length + 15 guesses)")
        print("3. Hard (word length + 5 guesses)")
        choice = input("Choose difficulty (1-3): ")

        if choice == 'D99':  # Debug mode for testing
            return 'debug'
        if choice in ['1', '2', '3']:
            return choice
        print("Invalid choice. Please try again.")

def get_max_guesses(difficulty, word_length):
    """Calculate maximum guesses based on difficulty"""
    if difficulty == 'debug':
        return 1  # Debug mode: 1 guess to quickly test out-of-guesses scenario
    elif difficulty == '1':
        return 26
    elif difficulty == '2':
        return word_length + 15
    return word_length + 5

def display_game_state(word_array, letters_not_in_word, guesses_remaining=None):
    """Display current game state"""
    print("\nCurrent Word:", ' '.join(x.upper() for x in word_array))
    if letters_not_in_word:
        print("Letters Not in Word:", ' '.join(x.upper() for x in letters_not_in_word))
    if guesses_remaining is not None:
        print(f"You have {guesses_remaining} guesses remaining.\n")

def handle_letter_guess(guess, word, word_array, letters_not_in_word):
    """Process a single letter guess"""
    if guess in letters_not_in_word or guess in word_array:
        print("You already guessed that letter.")
        return False

    found = False
    char_count = 0
    for i, letter in enumerate(word):
        if letter == guess:
            word_array[i] = guess
            found = True
            char_count += 1

    if found:
        print(f"There {'is' if char_count == 1 else 'are'} {char_count} letter{'s' if char_count > 1 else ''} '{guess.upper()}'")
    else:
        letters_not_in_word.append(guess)
        print(f"{guess.upper()} is not in the word.")

    return True

def play_infinite_guesses(word, word_array, letters_not_in_word):
    """Handle infinite guesses mode"""
    guess_count = 1
    while '_' in word_array:
        display_game_state(word_array, letters_not_in_word)
        guess = input(f"Guess {guess_count}: ").lower()

        if guess == word:
            print(f"\nYou won! The word was {word.upper()}! It took you {guess_count} guesses!")
            return True

        if len(guess) != 1:
            print("Please guess a single letter or the complete word!")
            continue

        if handle_letter_guess(guess, word, word_array, letters_not_in_word):
            guess_count += 1

        if '_' not in word_array:
            print(f"\nYou won! The word was {word.upper()}! It took you {guess_count} guesses!")
            return True

    return False

def play_hangman():
    """Main game loop"""
    while True:
        # Game setup
        difficulty = select_difficulty()
        word = random.choice(wordlist)
        max_guesses = get_max_guesses(difficulty, len(word))
        word_array = ['_' for _ in word]
        guess_count = 1
        letters_not_in_word = []

        # Main game loop
        display_game_state(word_array, letters_not_in_word, max_guesses - guess_count + 1)

        while '_' in word_array and guess_count <= max_guesses:
            guess = input(f"Guess {guess_count}: ").lower()

            if guess == word:
                print(f"\nYou won! The word was {word.upper()}. It took you {guess_count} guesses.")
                break

            if len(guess) != 1:
                print("Please guess a single letter or the complete word")
                continue
                
            if not guess.isalpha():
                print("Please enter a letter")
                continue

            if handle_letter_guess(guess, word, word_array, letters_not_in_word):
                display_game_state(word_array, letters_not_in_word, max_guesses - guess_count)
                guess_count += 1

        # Handle game end conditions
        if '_' in word_array and guess_count > max_guesses:
            if input("\nOut of guesses! Would you like to keep guessing (y) or see the word (n)? ").lower() == 'y':
                print("\nContinuing with infinite guesses...\n")
                if play_infinite_guesses(word, word_array, letters_not_in_word):
                    if input("\nPlay again? (y/n): ").lower() != 'y':
                        break
                    continue
            print(f"\nThe word was {word.upper()}!")
            break
        elif '_' not in word_array:
            print(f"\nYou won! The word was {word.upper()}! It took you {guess_count} guesses!")

        if input("\nPlay again? (y/n): ").lower() != 'y':
            break

def hangmanLoop():
    """Entry point for the game"""
    play_hangman()

if __name__ == "__main__":
    hangmanLoop()
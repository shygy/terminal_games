"""
Hangman Game Module

This module implements a classic Hangman word guessing game with multiple difficulty levels:
- Easy: 26 guesses (standard alphabet)
- Medium: word length + 15 guesses (balanced challenge)
- Hard: word length + 5 guesses (more challenging)

The game also features an infinite guesses mode that activates when the player
is down to their last guess, giving them a chance to complete the word without
the pressure of limited attempts.
"""

import random
import time  # Moved import here

# Import the wordlist from separate file
from wordlist import wordlist

def select_difficulty():
    """
    Get difficulty selection from user.

    This function presents difficulty options to the player and handles
    input validation to ensure a valid selection.

    Returns:
        str: The selected difficulty level ('1', '2', '3', or 'debug')
             '1' = Easy, '2' = Medium, '3' = Hard
             'debug' is a special mode for testing (hidden option)
    """
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
    """
    Calculate maximum guesses based on difficulty.

    Args:
        difficulty (str): The selected difficulty level ('1', '2', '3', or 'debug')
        word_length (int): The length of the word to be guessed

    Returns:
        int: The maximum number of allowed guesses based on difficulty

    Examples:
        >>> get_max_guesses('1', 8)
        26  # Easy mode is always 26 guesses
        >>> get_max_guesses('2', 8)
        23  # Medium is word length + 15
        >>> get_max_guesses('3', 8)
        13  # Hard is word length + 5
    """
    if difficulty == 'debug':
        return 1  # Debug mode: 1 guess to quickly test out-of-guesses scenario
    elif difficulty == '1':
        return 26  # Easy mode: One guess for each letter in the alphabet
    elif difficulty == '2':
        return word_length + 15  # Medium mode: Word length plus 15 extra guesses
    return word_length + 5  # Hard mode: Word length plus 5 extra guesses

def display_game_state(word_array, letters_not_in_word, guesses_remaining=None):
    """
    Display current game state including the word, guessed letters, and guesses remaining.

    Args:
        word_array (list): A list representing the current state of the word,
                            with revealed letters and underscores for hidden letters
        letters_not_in_word (list): A list of letters that have been guessed
                                    and are not in the word
        guesses_remaining (int, optional): The number of guesses remaining.
                                            If None, infinite guesses mode is active.

    Returns:
        None: This function only prints to the console
    """
    print("\nCurrent Word:", ' '.join(x.upper() for x in word_array))
    if letters_not_in_word:
        print("Letters Not in Word:", ' '.join(x.upper() for x in letters_not_in_word))
    if guesses_remaining is not None:
        print(f"You have {guesses_remaining} guesses remaining.\n")

def handle_letter_guess(guess, word, word_array, letters_not_in_word):
    """
    Process a single letter guess in the hangman game.

    This function checks if a letter has been guessed before, and if not,
    updates the game state based on whether the letter is in the word.

    Args:
        guess (str): The letter guessed by the player
        word (str): The target word to be guessed
        word_array (list): A list representing the current state of the word
        letters_not_in_word (list): A list of letters that have been guessed
                                    and are not in the word

    Returns:
        bool: True if this was a new guess, False if the letter was already guessed

    Side Effects:
        - Updates word_array in place if the guess is correct
        - Appends to letters_not_in_word if the guess is incorrect
        - Prints feedback about the guess
    """
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
    """
    Handle infinite guesses mode when player chooses to continue after running out of guesses.

    This function allows players to continue guessing until they completely reveal the word,
    without the restriction of limited attempts. It's offered as a "second chance" when
    a player is down to their last guess in normal mode.

    Args:
        word (str): The target word to be guessed
        word_array (list): Current state of the word with revealed and hidden letters
        letters_not_in_word (list): Letters that have been guessed and are not in the word

    Returns:
        None: This function runs until the word is completely guessed

    Side Effects:
        - Updates word_array in place as correct guesses are made
        - Modifies letters_not_in_word list with incorrect guesses
        - Prints game state and feedback after each guess
    """
    guess_count = 1
    while '_' in word_array:
        display_game_state(word_array, letters_not_in_word)
        guess = input(f"Guess {guess_count}: ").lower()

        if guess == word:
            print(f"\nYou won! The word was {word.upper()}! It took you {guess_count} guesses!")
            return True

        if len(guess) > 1 and guess.isalpha():  # Check if it's a word guess
            if guess != word:
                print("Incorrect word guess!")
                guess_count += 1
                display_game_state(word_array, letters_not_in_word)
                continue  # Go to the next turn
            else:
                print(f"\nYou won! The word was {word.upper()}! It took you {guess_count} guesses!")
                break

        if len(guess) != 1:
            print("Please guess a single letter or the complete word!")
            continue

        if handle_letter_guess(guess, word, word_array, letters_not_in_word):
            guess_count += 1

        if '_' not in word_array:
            print(f"\nYou won! The word was {word.upper()}! It took you {guess_count} guesses!")
            return True

    return False

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

def play_hangman():
    """
    Main game loop for Hangman.

    This function handles:
    - Setting up the game based on selected difficulty
    - Running the main guessing loop
    - Processing wins and losses
    - Handling the play again functionality
    - Offering infinite guesses mode when player is out of guesses

    Returns:
        None: This function runs the game until the player chooses to quit
    """
    while True:
        # Game setup
        difficulty = select_difficulty()
        if difficulty.lower() in ['quit', 'q', 'exit']:
            if confirm_quit():
                return
            else:
                continue
                
        word = random.choice(wordlist)
        max_guesses = get_max_guesses(difficulty, len(word))
        word_array = ['_' for _ in word]
        guess_count = 0  # Initialize guess_count to 0
        letters_not_in_word = []

        # Main game loop
        display_game_state(word_array, letters_not_in_word, max_guesses - guess_count)

        while '_' in word_array and guess_count < max_guesses:
            guess = input(f"Guess {guess_count + 1}: ").lower()
            
            if guess in ['quit', 'q', 'exit']:
                if confirm_quit():
                    return
                else:
                    # Continue the game
                    display_game_state(word_array, letters_not_in_word, max_guesses - guess_count)
                    continue

            if guess == word:
                print(f"\nYou won! The word was {word.upper()}. It took you {guess_count + 1} guesses.")
                break

            if len(guess) > 1 and guess.isalpha():  # Check if it's a word guess
                if guess != word:
                    print("Incorrect word guess!")
                    guess_count += 1
                    display_game_state(word_array, letters_not_in_word, max_guesses - guess_count)
                    continue  # Go to the next turn
                else:
                    print(f"\nYou won! The word was {word.upper()}. It took you {guess_count + 1} guesses.")
                    break

            if len(guess) != 1:
                print("Please guess a single letter or the complete word")
                continue

            if not guess.isalpha():
                print("Please enter a letter")
                continue

            if handle_letter_guess(guess, word, word_array, letters_not_in_word):
                guess_count += 1
                display_game_state(word_array, letters_not_in_word, max_guesses - guess_count)
            else:
                display_game_state(word_array, letters_not_in_word, max_guesses - guess_count) # Still display even if it was a repeat guess

        # Handle game end conditions
        if '_' in word_array and guess_count >= max_guesses:
            reveal_choice = input("\nOut of guesses! Would you like to keep guessing (y) or see the word (n)? ").lower()
            if reveal_choice == 'y':
                print("\nContinuing with infinite guesses...\n")
                if play_infinite_guesses(word, word_array, letters_not_in_word):
                    play_again = input("\nPlay again? (y/n): ").lower()
                    if play_again != 'y':
                        break
                    continue
            else:
                print(f"\nThe word was {word.upper()}!")
                while True:
                    play_again = input("\nPlay again? (y/n): ").lower()
                    
                    # Check if player wants to quit
                    if play_again in ['quit', 'q', 'exit']:
                        if confirm_quit():
                            return  # Exit the game
                        else:
                            continue  # Let the player choose again
                    elif play_again in ['y', 'yes']:
                        break
                    elif play_again in ['n', 'no']:
                        return  # Exit the game
                    else:
                        print("Invalid input. Please enter 'y' or 'n'.")
                        
                if play_again in ['y', 'yes']:
                    continue  # Start a new game
                else:
                    break
                continue

        elif '_' not in word_array:
            while True:
                play_again = input("\nPlay again? (y/n): ").lower()
                
                # Check if player wants to quit
                if play_again in ['quit', 'q', 'exit']:
                    if confirm_quit():
                        return  # Exit the game
                    else:
                        continue  # Let the player choose again
                elif play_again in ['y', 'yes']:
                    break
                elif play_again in ['n', 'no']:
                    return  # Exit the game
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
                    
            if play_again in ['y', 'yes']:
                continue  # Start a new game
            else:
                break

        else: # This condition is added to handle the case where the loop breaks due to a correct word guess
            while True:
                play_again = input("\nPlay again? (y/n): ").lower()
                
                # Check if player wants to quit
                if play_again in ['quit', 'q', 'exit']:
                    if confirm_quit():
                        return  # Exit the game
                    else:
                        continue  # Let the player choose again
                elif play_again in ['y', 'yes']:
                    break
                elif play_again in ['n', 'no']:
                    return  # Exit the game
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
                    
            if play_again in ['y', 'yes']:
                continue  # Start a new game
            else:
                break

def hangmanLoop():
    """
    Entry point for the Hangman game.

    This function serves as the main entry point when the game is selected
    from the game selector menu or run directly. It provides a clean interface
    for external modules to start the game without worrying about implementation
    details.

    Returns:
        None: This function doesn't return a value, but starts the Hangman game
    """
    try:
        print("\n" + "=" * 60)
        print(" " * 25 + "HANGMAN")
        print("=" * 60)
        print("\nWelcome to Hangman! Try to guess the hidden word one letter at a time.")
        print("Choose your difficulty level for an appropriate challenge.")
        print("\nFeatures include:")
        print("- Three difficulty levels with different guess limits")
        print("- Option to guess the entire word at once")
        print("- Infinite guesses mode when you're down to your last guess")
        print("\nGood luck!\n")

        # Small delay for better user experience
        time.sleep(1)

        # Start the main game
        play_hangman()
    except KeyboardInterrupt:
        print("\nGame interrupted. Returning to game selector...")
    except Exception as e:
        print(f"\nError occurred: {e}")
        print("Returning to game selector...")

if __name__ == "__main__":
    hangmanLoop()
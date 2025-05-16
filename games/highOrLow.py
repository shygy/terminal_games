import random

def play_guessing_game():
    while True:
        print("Let's play a guessing game.")
        compChoice = random.randint(1, 10)
        userChoice = int(input("I'm thinking of a number between 1 and 10 inclusive. Make a guess: "))
        guesses = 1

        while userChoice != compChoice:
            if userChoice < compChoice:
                userChoice = int(input("Higher than " + str(userChoice) + ". Guess again: "))
            else:
                userChoice = int(input("Lower than " + str(userChoice) + ". Guess again: "))
            guesses += 1

        if guesses == 1:
            print(f"Well done. The number was {compChoice}. You got it first try!")
        else:
            print(f"Well done. The number was {compChoice}. You got it in {guesses} guesses.")
            
        if input("Play again? (y/n): ").lower() != 'y':
            break

if __name__ == "__main__":
    play_guessing_game()
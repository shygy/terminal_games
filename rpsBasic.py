
import random

def rps(user, comp):
    user = user.lower()
    
    if user == comp:
        return "It's a tie."
    elif user == 'r':
        return "You win." if comp == 's' else "Computer wins."
    elif user == 'p':
        return "You win." if comp == 'r' else "Computer wins."
    elif user == 's':
        return "You win." if comp == 'p' else "Computer wins."
    else:
        return "Invalid input."

def play_rps():
    rps_choices = ['r', 'p', 's']
    while True:
        userRPS = input("Rock (R), Paper (P), Scissors (S): ")
        compSelection = random.choice(rps_choices)
        
        print(f"Computer chose: {compSelection.upper()}")
        result = rps(userRPS, compSelection)
        print(result)
        
        if input("Play again? (y/n): ").lower() != 'y':
            break

if __name__ == "__main__":
    play_rps()

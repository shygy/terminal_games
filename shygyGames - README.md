# shygyGames - The Terminal Collection v1.26

A collection of classic terminal-based games written in Python.

## Games Included

1. **Higher or Lower** - Guess a number between 1 and 10.
2. **Rock Paper Scissors** - Play the classic game against the computer.
3. **Hangman** - Guess the word before you run out of attempts.
4. **MasterMind** - Crack the secret code using logic and deduction.
5. **Roulette** - Bet on where the ball will land on the wheel.
6. **Blackjack** - Try to beat the dealer without going over 21.

## How to Run

1. Make sure you have Python 3 installed on your computer.
2. Open a terminal or command prompt.
3. Navigate to the terminal_games directory.
4. Run the launcher script:

```
python launch_games.py
```

Or on Unix-like systems:

```
chmod +x launch_games.py
./launch_games.py
```

## Game Controls

All games use simple keyboard input:
- Enter the number or letter shown in the prompts
- Press Enter to confirm your choices
- To quit most games, type 'q', 'quit', or 'exit'

## Game Rules

### Higher or Lower
- The computer picks a random number between 1 and 10
- Try to guess the number in as few attempts as possible
- The game will tell you if your guess is too high or too low

### Rock Paper Scissors
- Choose between Rock (R), Paper (P), or Scissors (S)
- Rock beats Scissors, Scissors beats Paper, Paper beats Rock
- Play multiple rounds and track your score against the computer

### Hangman
- Choose your difficulty level:
  - Easy: 26 guesses
  - Medium: word length + 15 guesses
  - Hard: word length + 5 guesses
- Try to guess the hidden word one letter at a time
- You can also guess the entire word if you think you know it
- When you have 1 guess remaining, you can choose to:
  - Reveal the word
  - Continue guessing with infinite tries
 
### MasterMind
- Logic game where you try to guess a secret code of digits (0-9)
- Choose your code length from 1 to 10 digits (enter 0 for 10 digits)
- Select game mode: standard (allows repeated digits) or no-repeats (unique digits in code only)
- After each guess, you'll receive feedback:
  - How many digits are in the correct position
  - How many digits are correct but in the wrong position
- Type 'h' or 'history' at any time to see a list of your previous guesses and results
- Type 'reveal' to see the secret code if you want to give up
- Try to crack the code in as few attempts as possible

### Roulette
- Classic casino game where you bet on where a ball will land on a spinning wheel
- Place bets with your Rocks on various outcomes with different payouts
- You start with 100 Rocks
- Multiple betting options available:
  - Inside Bets (higher payouts): Straight Up (35:1), Split (17:1), Street (11:1), Corner (8:1)
  - Outside Bets (1:1 payouts): Red/Black, Odd/Even, High/Low
- Place multiple bets in a single round to increase your chances

### Blackjack
- Classic card game where you aim to get as close to 21 as possible without going over
- Place bets with your Rocks (a very valuable currency)
- You start with 100 Rocks
- Blackjack (an Ace and a 10-value card) pays 3:2
- Win by beating the dealer's hand without busting

## Requirements

- Python 3.6 or higher
- No external dependencies required

## File Structure

```
terminal_games/
├── launch_games.py - Main launcher script
├── shygyGames - README.md - This file
├── start_games.bat - Windows launcher script
├── start_games.sh - Unix launcher script
├── game_selector.py - Game selection menu
├── blackJack.py - Blackjack game
├── hangman.py - Hangman game
├── wordlist.py - Word list for Hangman game
├── highOrLow.py - Number guessing game
├── masterMind.py - MasterMind code breaking game
├── roulette.py - Roulette betting game
└── rpsBasic.py - Rock Paper Scissors game
```

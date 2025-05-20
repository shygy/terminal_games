"""
Terminal Utilities for shygyGames Collection

This module provides shared utility functions for all games in the collection,
including color coding, help system, win streak tracking, and other common functionality.

Functions in this module:
- colorText: Apply color to text if color is enabled
- toggleColor: Toggle color output on or off
- getColorState: Get the current state of color output
- createDataDirectory: Create a data directory for storing game state
- saveStreakData: Save win streak data for a game
- getStreakData: Get win streak data for a game
- handleHelpCommand: Display help information for a specific game
- processCommand: Process a common command across all games
- getWinStreakReward: Calculate reward for a win streak
- processQuickBet: Process a quick bet command for Roulette
- getRockBalance: Get the current rock balance for the player
- updateRockBalance: Update the player's rock balance
- saveGameStats: Save game statistics for tracking performance
- getGameStats: Get statistics for a specific game

Classes:
    None

Constants:
    COLOR_CODES: Dictionary of ANSI color codes for terminal text coloring
    ROULETTE_QUICK_BETS: Dictionary of preset bet configurations for Roulette
    DEFAULT_ROCKS: Default starting rocks for a new player
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path

# Global variables
_colorEnabled = True  # Default state for color coding
DEFAULT_ROCKS = 100  # Default starting rocks for a new player

# Cheat codes for the games
CHEAT_CODES = {
    "millionaire": {"description": "Give 1000 Rocks to the player", "action": "rocks", "value": 1000},
    "lucky": {"description": "Give 777 Rocks to the player", "action": "rocks", "value": 777},
    "replit": {"description": "Give 100 Rocks to the player", "action": "rocks", "value": 100},
    "shygygames": {"description": "Activate rainbow text mode", "action": "rainbow", "value": True},
    "debug": {"description": "Show advanced game information", "action": "debug", "value": True},
    "tutorial": {"description": "Start tutorial mode", "action": "tutorial", "value": True}
}

# Global settings
_rainbowTextMode = False  # Rainbow text mode (cheat code reward)
_debugMode = False  # Debug mode for showing advanced game information
_tutorialMode = False  # Tutorial mode for guided gameplay

# ANSI color codes
COLOR_CODES = {
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'bold': '\033[1m',
    'underline': '\033[4m',
    'reset': '\033[0m',
    # Additional rainbow colors
    'lightred': '\033[38;5;203m',
    'orange': '\033[38;5;208m',
    'lightyellow': '\033[38;5;227m',
    'lightgreen': '\033[38;5;120m',
    'lightblue': '\033[38;5;39m',
    'purple': '\033[38;5;165m'
}

def colorText(text, color):
    """
    Apply color to text if color is enabled.
    
    Args:
        text (str): The text to colorize
        color (str): The color to use (red, green, yellow, blue, etc.)
                   or "rainbow" for rainbow text mode (requires cheat code)
        
    Returns:
        str: Colored text if enabled, original text otherwise
        
    Examples:
        >>> colorText("Success!", "green")
        '\033[92mSuccess!\033[0m'  # if color is enabled
        >>> colorText("Error!", "red")
        '\033[91mError!\033[0m'    # if color is enabled
        >>> colorText("Amazing!", "rainbow")
        # Returns text with each letter in a different color (if rainbow mode enabled)
    """
    global _rainbowTextMode
    
    if not _colorEnabled:
        return text
        
    if color == "rainbow" or _rainbowTextMode:
        if _rainbowTextMode:
            # Apply rainbow coloring (each character gets a different color)
            rainbow_colors = ['red', 'orange', 'lightyellow', 'lightgreen', 'lightblue', 'purple']
            result = ""
            for i, char in enumerate(text):
                if char.strip():  # Only color non-whitespace characters
                    color_idx = i % len(rainbow_colors)
                    result += f"{COLOR_CODES[rainbow_colors[color_idx]]}{char}{COLOR_CODES['reset']}"
                else:
                    result += char
            return result
        else:
            # Rainbow requested but not enabled via cheat code
            return text
    
    if color not in COLOR_CODES:
        return text
    
    return f"{COLOR_CODES[color]}{text}{COLOR_CODES['reset']}"

def toggleColor():
    """
    Toggle color output on or off.
    
    This function switches the color state between enabled and disabled.
    Use this when the user wants to change the color display preference.
    
    Returns:
        bool: The new state of color output (True if enabled, False if disabled)
        
    Examples:
        >>> toggleColor()  # If color was enabled, now it's disabled
        False
        >>> toggleColor()  # If color was disabled, now it's enabled
        True
    """
    global _colorEnabled
    _colorEnabled = not _colorEnabled
    return _colorEnabled

def getColorState():
    """
    Get the current state of color output.
    
    This function returns whether colored text output is currently enabled.
    
    Returns:
        bool: True if color is enabled, False otherwise
        
    Examples:
        >>> getColorState()
        True  # If color is currently enabled
    """
    return _colorEnabled

def createDataDirectory():
    """
    Create a data directory for storing game state if it doesn't exist.
    
    This function creates a hidden directory in the user's home folder
    to store persistent game data like win streaks.
    
    Returns:
        Path: Path object pointing to the data directory
        
    Examples:
        >>> dataDir = createDataDirectory()
        >>> str(dataDir)
        '/home/user/.shygygames'  # on Linux/Mac
        >>> dataDir.exists()
        True
    """
    dataDir = Path.home() / ".shygygames"
    if not dataDir.exists():
        dataDir.mkdir(exist_ok=True)
    return dataDir

def saveStreakData(gameName, winCount, maxStreak):
    """
    Save win streak data for a game.
    
    This function persistently stores the current and maximum win streaks
    for a specific game in a JSON file.
    
    Args:
        gameName (str): The name of the game (e.g., "roulette", "blackjack")
        winCount (int): The current win count/streak
        maxStreak (int): The maximum win streak achieved
        
    Returns:
        None
        
    Examples:
        >>> saveStreakData("roulette", 3, 5)  # Current streak is 3, max was 5
        >>> saveStreakData("blackjack", 0, 7)  # Reset current streak, max was 7
    """
    dataDir = createDataDirectory()
    streakFile = dataDir / "win_streaks.json"
    
    # Initialize or load existing data
    if streakFile.exists():
        with open(streakFile, 'r') as f:
            try:
                streaks = json.load(f)
            except json.JSONDecodeError:
                streaks = {}
    else:
        streaks = {}
    
    # Update streak data for this game
    if gameName not in streaks:
        streaks[gameName] = {"current_streak": winCount, "max_streak": maxStreak}
    else:
        streaks[gameName]["current_streak"] = winCount
        streaks[gameName]["max_streak"] = max(streaks[gameName]["max_streak"], maxStreak)
    
    # Save updated data
    with open(streakFile, 'w') as f:
        json.dump(streaks, f)

def getStreakData(gameName):
    """
    Get win streak data for a game.
    
    This function retrieves the current and maximum win streaks
    for a specific game from the saved JSON file.
    
    Args:
        gameName (str): The name of the game (e.g., "roulette", "blackjack")
        
    Returns:
        tuple: (current_streak, max_streak) or (0, 0) if no data exists
        
    Examples:
        >>> getStreakData("roulette")
        (3, 5)  # Current streak is 3, max is 5
        >>> getStreakData("unknown_game")
        (0, 0)  # No data for this game
    """
    dataDir = createDataDirectory()
    streakFile = dataDir / "win_streaks.json"
    
    if not streakFile.exists():
        return (0, 0)
    
    with open(streakFile, 'r') as f:
        try:
            streaks = json.load(f)
            if gameName in streaks:
                return (streaks[gameName]["current_streak"], streaks[gameName]["max_streak"])
            else:
                return (0, 0)
        except (json.JSONDecodeError, KeyError):
            return (0, 0)

def handleHelpCommand(gameName):
    """
    Display help information for a specific game.
    
    Args:
        gameName (str): The name of the game to show help for
        
    Returns:
        None: Just prints the help information
    """
    helpText = {
        "general": """
=== GENERAL COMMANDS ===
help              - Display this help message
quit, q, exit     - Exit the current game
color:switch      - Toggle colored text on/off
color             - Display the current color state
rocks, balance    - Show your current rock balance (shared across all games)
stats             - Show statistics for the current game
statistics        - Show overall statistics across all games

Special commands are available in each game. Type 'help' while playing for game-specific help.
""",
        "roulette": """
=== ROULETTE COMMANDS ===
help              - Display this help message
quit, q, exit     - Exit the game
color:switch      - Toggle colored text on/off
color             - Display the current color state
his, history      - Show history of recent spins

Betting Options:
- Inside Bets (Higher Payout):
  • Straight Up: Bet on a single number (pays 35:1)
  • Split: Bet on two adjacent numbers (pays 17:1)
  • Street: Bet on three numbers in a row (pays 11:1)
  • Corner: Bet on four numbers that form a square (pays 8:1)
  
- Outside Bets (Lower Payout):
  • Red/Black: Bet on all red or all black numbers (pays 1:1)
  • Odd/Even: Bet on all odd or all even numbers (pays 1:1)
  • Low/High: Bet on numbers 1-18 or 19-36 (pays 1:1)

Quick Bets (shortcuts):
quick:red [amount]    - Quickly bet on red
quick:black [amount]  - Quickly bet on black
quick:odd [amount]    - Quickly bet on odd numbers
quick:even [amount]   - Quickly bet on even numbers
quick:low [amount]    - Quickly bet on low numbers (1-18)
quick:high [amount]   - Quickly bet on high numbers (19-36)
quick:0 [amount]      - Quickly bet on zero
""",
        "mastermind": """
=== MASTERMIND COMMANDS ===
help              - Display this help message
quit, q, exit     - Exit the game
color:switch      - Toggle colored text on/off
color             - Display the current color state
h, history        - View your previous guesses and results
reveal            - Give up and reveal the secret code

Game Options:
- Choose code length from 1-10 digits (enter 0 for 10 digits)
- Select game mode: standard (allows repeated digits) or no-repeats (unique digits in code only)
- You can enter repeated digits in your guesses regardless of game mode
""",
        "blackjack": """
=== BLACKJACK COMMANDS ===
help              - Display this help message
quit, q, exit     - Exit the game
color:switch      - Toggle colored text on/off
color             - Display the current color state

Game Commands:
- hit             - Take another card
- stand           - End your turn and let the dealer play
- double          - Double your bet and take exactly one more card
- split           - Split a matching pair into two separate hands
- insurance       - Take insurance when dealer shows an Ace (costs half your bet)

How to Win:
- Get closer to 21 than the dealer without going over
- Dealer hits until they have 17 or more
- Blackjack (Ace + 10-value card) pays 3:2
"""
    }
    
    if gameName.lower() in helpText:
        print(colorText(helpText[gameName.lower()], "cyan"))
    else:
        print(colorText(helpText["general"], "cyan"))

def processCheatCode(code):
    """
    Process a cheat code entered by the user.
    
    This function checks if a code is a valid cheat code and applies its effect.
    Valid cheat codes are defined in the CHEAT_CODES dictionary.
    
    Args:
        code (str): The cheat code entered by the user
        
    Returns:
        tuple: (bool, str) - (True if code was valid, result message)
    """
    global _rainbowTextMode, _debugMode, _tutorialMode
    
    if code.lower() in CHEAT_CODES:
        cheat = CHEAT_CODES[code.lower()]
        action = cheat["action"]
        value = cheat["value"]
        
        if action == "rocks":
            # Add rocks to the player's balance
            current_balance = getRockBalance()
            new_balance = current_balance + value
            updateRockBalance(new_balance)
            return (True, colorText(f"Cheat code activated! Added {value} Rocks to your balance!", "green"))
            
        elif action == "rainbow":
            # Toggle rainbow text mode
            _rainbowTextMode = value
            return (True, colorText("Cheat code activated! Rainbow text mode enabled!", "rainbow"))
            
        elif action == "debug":
            # Toggle debug mode
            _debugMode = value
            return (True, colorText("Cheat code activated! Debug mode enabled!", "cyan"))
            
        elif action == "tutorial":
            # Toggle tutorial mode
            _tutorialMode = value
            return (True, colorText("Cheat code activated! Tutorial mode enabled!", "yellow"))
            
    return (False, "")


def getDebugMode():
    """
    Check if debug mode is enabled.
    
    Returns:
        bool: True if debug mode is enabled, False otherwise
    """
    return _debugMode


def getTutorialMode():
    """
    Check if tutorial mode is enabled.
    
    Returns:
        bool: True if tutorial mode is enabled, False otherwise
    """
    return _tutorialMode


def processCommand(command, gameName):
    """
    Process a common command across all games.
    
    Args:
        command (str): The command entered by the user
        gameName (str): The name of the current game
        
    Returns:
        tuple: (bool, str) - (True if command was handled, result message)
    """
    # Check if this is a cheat code
    isCheat, cheatMessage = processCheatCode(command)
    if isCheat:
        return (True, cheatMessage)
    
    if command.lower() in ["help"]:
        handleHelpCommand(gameName)
        return (True, "help displayed")
        
    if command.lower() == "color:switch":
        newState = toggleColor()
        if newState:
            return (True, colorText("Color output is now ON", "green"))
        else:
            return (True, "Color output is now OFF")
            
    if command.lower() == "color":
        state = getColorState()
        return (True, f"Color is currently: {'ON' if state else 'OFF'}")
    
    if command.lower() in ["rocks", "balance"]:
        rocks = getRockBalance()
        return (True, colorText(f"Your current rock balance: {rocks} Rocks", "cyan"))
    
    # Roulette-specific commands
    if gameName.lower() == "roulette" and command.lower() in ["his", "history"]:
        displayRouletteSpinHistory()
        return (True, "roulette history displayed")
    
    if command.lower() in ["stats", "statistics"]:
        # Show game-specific stats or general stats
        if command.lower() == "stats":
            stats = getGameStats(gameName)
            print(colorText(f"\n=== {gameName.upper()} STATISTICS ===", "cyan"))
            print(f"Total plays: {stats['plays']}")
            print(f"Wins: {stats['wins']} ({int(stats['wins']/max(1, stats['plays'])*100)}%)")
            print(f"Losses: {stats['losses']}")
            print(f"Draws: {stats['draws']}")
            print(f"Total Rocks won: {stats['rocks_won']}")
            print(f"Total Rocks lost: {stats['rocks_lost']}")
            print(f"Best win: {stats['best_win']} Rocks")
            print(f"Worst loss: {stats['worst_loss']} Rocks")
            if 'history' in stats and isinstance(stats['history'], list) and len(stats['history']) > 0:
                print(colorText("\nRecent history:", "yellow"))
                for i, entry in enumerate(reversed(stats['history'][:5])):
                    result_color = "green" if entry['result'] == "win" else "red" if entry['result'] == "loss" else "yellow"
                    result_text = colorText(entry['result'].upper(), result_color)
                    print(f"  {i+1}. {result_text} - Rocks change: {entry['rocks_change']}")
        else:
            # General stats across all games
            stats = getGameStats()
            print(colorText("\n=== OVERALL GAME STATISTICS ===", "cyan"))
            print(f"Total plays across all games: {stats['total_plays']}")
            print(f"Total wins: {stats['total_wins']} ({int(stats['total_wins']/max(1, stats['total_plays'])*100)}%)")
            print(f"Total Rocks won: {stats['total_rocks_won']}")
            print(f"Total Rocks lost: {stats['total_rocks_lost']}")
            print(f"Net Rocks: {stats['total_rocks_won'] - stats['total_rocks_lost']}")
            
            # Show per-game summary
            all_games = getGameStats(None)
            if isinstance(all_games, dict) and "games" in all_games:
                print(colorText("\nGame breakdown:", "yellow"))
                for game, game_stats in all_games["games"].items():
                    if game_stats["plays"] > 0:
                        win_rate = int(game_stats["wins"] / game_stats["plays"] * 100)
                        print(f"  {game}: {game_stats['plays']} plays, {win_rate}% win rate")
        
        return (True, "stats displayed")
    
    if command.lower() == "reset":
        # Reset all games and data
        if resetAllGames():
            return (True, "reset complete")
        return (True, "reset cancelled")
        
    if command.lower() == "cheats" and getDebugMode():
        # Display available cheat codes (only in debug mode)
        print(colorText("\n=== AVAILABLE CHEAT CODES ===", "magenta"))
        for code, info in CHEAT_CODES.items():
            print(f"  {colorText(code, 'yellow')}: {info['description']}")
        return (True, "cheat codes displayed")
        
    # Command not handled by this function
    return (False, "")

def getWinStreakReward(streak, gameName):
    """
    Calculate reward for a win streak.
    
    Args:
        streak (int): The current win streak
        gameName (str): The name of the game
        
    Returns:
        tuple: (reward_amount, message) or (0, "") if no reward
    """
    # Base rewards
    if streak == 3:
        return (10, colorText(f"Win Streak Bonus! +10 Rocks for 3 wins in a row!", "green"))
    elif streak == 5:
        return (25, colorText(f"Win Streak Bonus! +25 Rocks for 5 wins in a row!", "green"))
    elif streak == 10:
        return (100, colorText(f"AMAZING Win Streak! +100 Rocks for 10 consecutive wins!", "green"))
    elif streak > 0 and streak % 10 == 0:
        reward = streak * 10
        return (reward, colorText(f"LEGENDARY Win Streak! +{reward} Rocks for {streak} consecutive wins!", "green"))
        
    # No reward
    return (0, "")
    

def getRockBalance():
    """
    Get the current rock balance for the player.
    
    This function retrieves the shared rock balance that is used
    across all games in the collection. If no balance exists yet,
    it returns the default starting amount.
    
    Returns:
        int: The current rock balance
        
    Examples:
        >>> getRockBalance()
        100  # Default starting balance
        >>> # After winning some rocks in a game
        >>> getRockBalance()
        150  # Updated balance
    """
    dataDir = createDataDirectory()
    balanceFile = dataDir / "rocks_balance.json"
    
    if not balanceFile.exists():
        # If no balance exists yet, create one with the default amount
        updateRockBalance(DEFAULT_ROCKS)
        return DEFAULT_ROCKS
    
    try:
        with open(balanceFile, 'r') as f:
            data = json.load(f)
            return data.get("balance", DEFAULT_ROCKS)
    except (json.JSONDecodeError, IOError):
        # If there's an error reading the file, return the default
        return DEFAULT_ROCKS


def updateRockBalance(newBalance):
    """
    Update the player's rock balance.
    
    This function updates the shared rock balance that is used
    across all games in the collection.
    
    Args:
        newBalance (int): The new rock balance
        
    Returns:
        int: The updated rock balance
        
    Examples:
        >>> updateRockBalance(150)
        150  # Balance is now 150 rocks
        >>> updateRockBalance(getRockBalance() + 50)
        200  # Added 50 rocks to current balance
    """
    dataDir = createDataDirectory()
    balanceFile = dataDir / "rocks_balance.json"
    
    # Ensure balance is a positive integer
    newBalance = max(0, int(newBalance))
    
    try:
        data = {"balance": newBalance, "last_updated": datetime.now().isoformat()}
        with open(balanceFile, 'w') as f:
            json.dump(data, f)
        return newBalance
    except IOError:
        print(colorText("Warning: Could not save rock balance.", "yellow"))
        return newBalance

# Input prompt styling function
def getInput(prompt):
    """
    Display a prompt and get user input with consistent styling.
    
    This function applies the standard purple/magenta color to all input
    prompts for consistency across all games.
    
    Args:
        prompt (str): The prompt text to display to the user
        
    Returns:
        str: The user's input (lowercase)
        
    Examples:
        >>> getInput("Enter your name: ")
        # Displays the prompt in purple and returns the user's input
    """
    return input(colorText(prompt, "magenta")).lower()

# Game save/load functions
def saveGameState(gameName, state):
    """
    Save the state of a game to a file.
    
    This function saves the current state of a game to a JSON file
    for later retrieval when the player wants to resume the game.
    
    Args:
        gameName (str): The name of the game to save
        state (dict): The current state of the game
        
    Returns:
        bool: True if the state was saved successfully, False otherwise
        
    Examples:
        >>> gameState = {"score": 100, "level": 5, "items": ["sword", "shield"]}
        >>> saveGameState("adventure", gameState)
        True
    """
    dataDir = createDataDirectory()
    saveDir = dataDir / "saved_games"
    
    # Create the saved_games directory if it doesn't exist
    saveDir.mkdir(exist_ok=True)
    
    saveFile = saveDir / f"{gameName}_save.json"
    
    try:
        with open(saveFile, 'w') as f:
            json.dump(state, f)
        return True
    except IOError:
        print(colorText("Warning: Could not save game state.", "yellow"))
        return False


def loadGameState(gameName):
    """
    Load the saved state of a game from a file.
    
    This function retrieves the saved state of a game from a JSON file
    when the player wants to resume a previously saved game.
    
    Args:
        gameName (str): The name of the game to load
        
    Returns:
        dict or None: The saved state of the game, or None if no save exists
        
    Examples:
        >>> loadGameState("adventure")
        {"score": 100, "level": 5, "items": ["sword", "shield"]}
        >>> loadGameState("nonexistent_game")
        None
    """
    dataDir = createDataDirectory()
    saveDir = dataDir / "saved_games"
    saveFile = saveDir / f"{gameName}_save.json"
    
    if not saveFile.exists():
        return None
        
    try:
        with open(saveFile, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print(colorText("Warning: Could not load saved game.", "yellow"))
        return None


def hasSavedGame(gameName):
    """
    Check if a saved game exists.
    
    Args:
        gameName (str): The name of the game to check
        
    Returns:
        bool: True if a saved game exists, False otherwise
        
    Examples:
        >>> hasSavedGame("adventure")
        True
        >>> hasSavedGame("nonexistent_game")
        False
    """
    dataDir = createDataDirectory()
    saveDir = dataDir / "saved_games"
    saveFile = saveDir / f"{gameName}_save.json"
    
    return saveFile.exists()


def deleteSavedGame(gameName):
    """
    Delete a saved game.
    
    Args:
        gameName (str): The name of the game to delete
        
    Returns:
        bool: True if the saved game was deleted successfully, False otherwise
        
    Examples:
        >>> deleteSavedGame("adventure")
        True
    """
    dataDir = createDataDirectory()
    saveDir = dataDir / "saved_games"
    saveFile = saveDir / f"{gameName}_save.json"
    
    if not saveFile.exists():
        return True
        
    try:
        saveFile.unlink()
        return True
    except IOError:
        print(colorText("Warning: Could not delete saved game.", "yellow"))
        return False


def confirmQuit(gameName=None, state=None):
    """
    Confirm if the user wants to quit the game and handle saving.
    
    This function asks the user if they want to save the game before quitting
    and handles the appropriate action based on their response.
    
    Args:
        gameName (str, optional): The name of the game being played
        state (dict, optional): The current state of the game
        
    Returns:
        bool: True if the user wants to quit, False otherwise
        
    Examples:
        >>> confirmQuit("blackjack", gameState)
        # Prompts user and returns True if they confirm quit
    """
    if not gameName or not state:
        # Simple quit without save option if no game state is provided
        response = input(colorText("\nAre you sure you want to quit? (y/n): ", "yellow")).lower()
        return response.startswith('y')
    
    print(colorText("\nQuit options:", "cyan"))
    print("  (S) Save and quit")
    print("  (Q) Quit without saving")
    print("  (C) Cancel and continue playing")
    
    while True:
        choice = input(colorText("Your choice: ", "yellow")).lower()
        
        if choice in ['s', 'save']:
            # Save game state before quitting
            if saveGameState(gameName, state):
                print(colorText(f"Game saved! You can resume later by selecting {gameName}.", "green"))
            return True
            
        elif choice in ['q', 'quit']:
            # Quit without saving
            confirm = input(colorText("Are you sure you want to quit without saving? (y/n): ", "red")).lower()
            if confirm.startswith('y'):
                return True
                
        elif choice in ['c', 'cancel', 'n', 'no']:
            # Cancel quit
            return False
            
        else:
            print(colorText("Invalid choice. Please try again.", "red"))


def resetAllGames():
    """
    Reset all game data and start fresh.
    
    This function deletes all saved games, statistics, and rock balance,
    essentially giving the player a clean slate.
    
    Returns:
        bool: True if reset was successful, False otherwise
        
    Examples:
        >>> resetAllGames()
        # Deletes all saved data and returns True
    """
    confirm = input(colorText("\nWARNING: This will reset ALL games and delete ALL saved data!\nAre you sure? (y/n): ", "red")).lower()
    
    if not confirm.startswith('y'):
        print(colorText("Reset cancelled.", "yellow"))
        return False
    
    dataDir = createDataDirectory()
    
    # Delete saved games
    saveDir = dataDir / "saved_games"
    if saveDir.exists():
        try:
            for saveFile in saveDir.glob("*_save.json"):
                saveFile.unlink()
            saveDir.rmdir()
        except IOError:
            print(colorText("Warning: Could not delete all saved games.", "yellow"))
    
    # Delete rock balance
    balanceFile = dataDir / "rocks_balance.json"
    if balanceFile.exists():
        try:
            balanceFile.unlink()
        except IOError:
            print(colorText("Warning: Could not delete rock balance.", "yellow"))
    
    # Delete statistics
    statsFile = dataDir / "game_stats.json"
    if statsFile.exists():
        try:
            statsFile.unlink()
        except IOError:
            print(colorText("Warning: Could not delete game statistics.", "yellow"))
    
    # Delete streak data
    streakFile = dataDir / "win_streaks.json"
    if streakFile.exists():
        try:
            streakFile.unlink()
        except IOError:
            print(colorText("Warning: Could not delete streak data.", "yellow"))
    
    print(colorText("\nAll game data has been reset!", "green"))
    print("The program will now restart for changes to take effect...")
    time.sleep(2)  # Give the user time to read the message
    
    # Return True to indicate successful reset
    return True

# Game statistics tracking functions
def saveGameStats(gameName, result, rocksWon=0, details=None):
    """
    Save game statistics for tracking performance.
    
    This function records the outcome of a game along with any
    details for long-term statistics tracking.
    
    Args:
        gameName (str): The name of the game played
        result (str): The result of the game ('win', 'loss', 'draw', etc.)
        rocksWon (int): Number of rocks won or lost (negative for losses)
        details (dict, optional): Additional details about the game
        
    Returns:
        bool: True if statistics were saved successfully, False otherwise
        
    Examples:
        >>> saveGameStats('roulette', 'win', 25, {'bet_type': 'red'})
        True
        >>> saveGameStats('blackjack', 'loss', -10)
        True
    """
    dataDir = createDataDirectory()
    statsFile = dataDir / "game_stats.json"
    
    # Initialize or load existing stats
    if statsFile.exists():
        try:
            with open(statsFile, 'r') as f:
                stats = json.load(f)
        except json.JSONDecodeError:
            stats = {"games": {}}
    else:
        stats = {"games": {}}
    
    # Initialize game entry if it doesn't exist
    if gameName not in stats["games"]:
        stats["games"][gameName] = {
            "plays": 0,
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "rocks_won": 0,
            "rocks_lost": 0,
            "best_win": 0,
            "worst_loss": 0,
            "last_played": "",
            "history": []
        }
    
    # Update game statistics
    game_stats = stats["games"][gameName]
    game_stats["plays"] += 1
    
    if result == "win":
        game_stats["wins"] += 1
        game_stats["rocks_won"] += rocksWon
        game_stats["best_win"] = max(game_stats["best_win"], rocksWon)
    elif result == "loss":
        game_stats["losses"] += 1
        game_stats["rocks_lost"] += abs(rocksWon) if rocksWon < 0 else 0
        game_stats["worst_loss"] = max(game_stats["worst_loss"], abs(rocksWon) if rocksWon < 0 else 0)
    elif result == "draw":
        game_stats["draws"] += 1
    
    # Record timestamp
    timestamp = datetime.now().isoformat()
    game_stats["last_played"] = timestamp
    
    # Add to history (limit to last 50 games)
    history_entry = {
        "result": result,
        "rocks_change": rocksWon,
        "timestamp": timestamp
    }
    
    if details:
        history_entry["details"] = details
        
    game_stats["history"].append(history_entry)
    game_stats["history"] = game_stats["history"][-50:]  # Keep last 50 entries
    
    # Update the global stats
    if "summary" not in stats:
        stats["summary"] = {
            "total_plays": 0,
            "total_wins": 0,
            "total_rocks_won": 0,
            "total_rocks_lost": 0
        }
    
    stats["summary"]["total_plays"] += 1
    if result == "win":
        stats["summary"]["total_wins"] += 1
        stats["summary"]["total_rocks_won"] += rocksWon
    elif result == "loss" and rocksWon < 0:
        stats["summary"]["total_rocks_lost"] += abs(rocksWon)
    
    # Save updated stats
    try:
        with open(statsFile, 'w') as f:
            json.dump(stats, f, indent=2)
        return True
    except IOError:
        print(colorText("Warning: Could not save game statistics.", "yellow"))
        return False


def getGameStats(gameName=None):
    """
    Get statistics for a specific game or all games.
    
    This function retrieves the saved statistics for a game
    or a summary of all games if no game name is provided.
    
    Args:
        gameName (str, optional): The name of the game to get stats for,
                                 or None to get summary stats for all games
        
    Returns:
        dict: Game statistics or summary statistics
        
    Examples:
        >>> getGameStats('roulette')
        {'plays': 10, 'wins': 5, 'losses': 5, 'rocks_won': 100, ...}
        >>> getGameStats()
        {'total_plays': 25, 'total_wins': 12, 'total_rocks_won': 250, ...}
    """
    dataDir = createDataDirectory()
    statsFile = dataDir / "game_stats.json"
    
    if not statsFile.exists():
        # No stats saved yet
        if gameName:
            return {
                "plays": 0,
                "wins": 0,
                "losses": 0,
                "draws": 0,
                "rocks_won": 0,
                "rocks_lost": 0,
                "best_win": 0,
                "worst_loss": 0,
                "last_played": "",
                "history": []
            }
        else:
            return {
                "total_plays": 0,
                "total_wins": 0,
                "total_rocks_won": 0,
                "total_rocks_lost": 0
            }
    
    try:
        with open(statsFile, 'r') as f:
            stats = json.load(f)
            
        if gameName:
            # Return stats for specific game (or empty stats if game not found)
            return stats["games"].get(gameName, {
                "plays": 0,
                "wins": 0,
                "losses": 0,
                "draws": 0,
                "rocks_won": 0,
                "rocks_lost": 0,
                "best_win": 0,
                "worst_loss": 0,
                "last_played": "",
                "history": []
            })
        else:
            # Return summary stats for all games
            return stats.get("summary", {
                "total_plays": 0,
                "total_wins": 0,
                "total_rocks_won": 0,
                "total_rocks_lost": 0
            })
            
    except (json.JSONDecodeError, KeyError, IOError):
        # If there's an error reading the file, return empty stats
        return {
            "plays": 0,
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "rocks_won": 0,
            "rocks_lost": 0
        } if gameName else {
            "total_plays": 0,
            "total_wins": 0,
            "total_rocks_won": 0,
            "total_rocks_lost": 0
        }


# Quick betting presets for Roulette
ROULETTE_QUICK_BETS = {
    "quick:red": {"type": "red", "description": "Red bet"},
    "quick:black": {"type": "black", "description": "Black bet"},
    "quick:odd": {"type": "odd", "description": "Odd numbers bet"},
    "quick:even": {"type": "even", "description": "Even numbers bet"},
    "quick:low": {"type": "low", "description": "Low numbers (1-18) bet"},
    "quick:high": {"type": "high", "description": "High numbers (19-36) bet"},
    "quick:0": {"type": "straight", "value": 0, "description": "Straight Up bet on 0"},
}

def saveRouletteSpinHistory(spinNumber, spinType):
    """
    Save the result of a roulette spin to history.
    
    This function saves the last spins in a roulette game to a JSON file
    for displaying the history of results.
    
    Args:
        spinNumber (int): The number that was spun
        spinType (str): The type of the spin (red, black, green)
        
    Returns:
        list: The updated history list
        
    Examples:
        >>> saveRouletteSpinHistory(7, "red")
        [{'number': 7, 'type': 'red'}, ...]  # List of recent spins
    """
    dataDir = createDataDirectory()
    historyFile = dataDir / "roulette_history.json"
    
    # Initialize or load existing history
    if historyFile.exists():
        try:
            with open(historyFile, 'r') as f:
                history = json.load(f)
        except json.JSONDecodeError:
            history = []
    else:
        history = []
    
    # Add the new spin to history
    history.append({"number": spinNumber, "type": spinType, "timestamp": datetime.now().isoformat()})
    
    # Keep only last 50 spins
    history = history[-50:]
    
    # Save updated history
    try:
        with open(historyFile, 'w') as f:
            json.dump(history, f)
        return history
    except IOError:
        print(colorText("Warning: Could not save roulette history.", "yellow"))
        return history


def getRouletteSpinHistory():
    """
    Get the history of roulette spins.
    
    This function retrieves the saved history of roulette spins from a JSON file.
    
    Returns:
        list: List of recent spins, or empty list if no history exists
        
    Examples:
        >>> getRouletteSpinHistory()
        [{'number': 7, 'type': 'red'}, {'number': 0, 'type': 'green'}, ...]
    """
    dataDir = createDataDirectory()
    historyFile = dataDir / "roulette_history.json"
    
    if not historyFile.exists():
        return []
    
    try:
        with open(historyFile, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def displayRouletteSpinHistory():
    """
    Display the history of roulette spins in a formatted table.
    
    This function retrieves and displays the history of roulette spins
    in a nicely formatted table with colors.
    
    Returns:
        bool: True if history was displayed, False if no history exists
        
    Examples:
        >>> displayRouletteSpinHistory()
        === ROULETTE SPIN HISTORY ===
        1. 7 (RED)
        2. 0 (GREEN)
        3. 26 (BLACK)
        ...
    """
    history = getRouletteSpinHistory()
    
    if not history:
        print(colorText("No spin history available yet.", "yellow"))
        return False
    
    print(colorText("\n=== ROULETTE SPIN HISTORY ===", "cyan"))
    
    # Display the most recent spins first
    for i, spin in enumerate(reversed(history[:20])):
        number = spin["number"]
        spinType = spin["type"].lower()
        
        # Determine color for the number
        if spinType == "red":
            numColor = "red"
        elif spinType == "black":
            numColor = "white"  # Use white on black terminal for visibility
        else:  # green (0)
            numColor = "green"
        
        # Format and display the spin
        typeText = spinType.upper()
        numberText = colorText(str(number), numColor)
        print(f"{i+1}. {numberText} ({typeText})")
    
    # Show how many more spins are in history if there are more than 20
    if len(history) > 20:
        print(f"... and {len(history) - 20} more spins")
    
    # Display some stats
    red_count = sum(1 for spin in history if spin["type"].lower() == "red")
    black_count = sum(1 for spin in history if spin["type"].lower() == "black")
    green_count = sum(1 for spin in history if spin["type"].lower() == "green")
    
    print(colorText("\nStats from last 50 spins:", "yellow"))
    print(f"Red: {red_count} ({int(red_count/len(history)*100)}%)")
    print(f"Black: {black_count} ({int(black_count/len(history)*100)}%)")
    print(f"Green: {green_count} ({int(green_count/len(history)*100)}%)")
    
    return True


def processQuickBet(command, current_balance=None):
    """
    Process a quick bet command for Roulette.
    
    Args:
        command (str): The command entered by the user
        current_balance (int, optional): Current rock balance for percentage betting
        
    Returns:
        tuple: (bool, dict) - (True if it's a valid quick bet, bet information)
        
    Examples:
        >>> processQuickBet("quick:red 50")
        (True, {'type': 'red', 'description': 'Red bet', 'amount': 50})
        >>> processQuickBet("quick:red 50%", 200)
        (True, {'type': 'red', 'description': 'Red bet', 'amount': 100})
        >>> processQuickBet("quick:red 50%;black 30%", 200)
        (True, {'type': 'red', 'description': 'Red bet', 'amount': 100, 'additional_bets': [{'type': 'black', 'description': 'Black bet', 'amount': 60}]})
        >>> processQuickBet("invalid")
        (False, {})
    """
    # Check for multiple bets separated by semicolons (e.g., "quick:red 50%;black 30%")
    if ";" in command:
        commands = command.split(";")
        first_command = commands[0].strip()
        
        # Process first command as normal
        is_quick_bet, bet_info = processQuickBet(first_command, current_balance)
        if not is_quick_bet:
            return (False, {})
            
        # Process additional bets
        additional_bets = []
        remaining_balance = current_balance - bet_info["amount"] if current_balance is not None else None
        
        for additional_command in commands[1:]:
            additional_command = additional_command.strip()
            if not additional_command:
                continue
                
            # For additional bets, prepend "quick:" if not already present
            if not additional_command.startswith("quick:"):
                additional_command = "quick:" + additional_command
                
            is_quick_bet_additional, additional_bet_info = processQuickBet(additional_command, remaining_balance)
            if is_quick_bet_additional:
                additional_bets.append(additional_bet_info)
                if remaining_balance is not None and "amount" in additional_bet_info:
                    remaining_balance -= additional_bet_info["amount"]
        
        # Add the additional bets to the first bet info
        if additional_bets:
            bet_info["additional_bets"] = additional_bets
            
        return (True, bet_info)
    
    # Standard single bet processing
    parts = command.lower().split()
    
    if not parts:
        return (False, {})
        
    # Check if this is a quick bet command
    quickBetType = parts[0]
    if not quickBetType.startswith("quick:"):
        return (False, {})
        
    bet_type = quickBetType.split(":", 1)[1]
    if bet_type not in ROULETTE_QUICK_BETS:
        return (False, {})
        
    # Get bet amount if provided
    betAmount = None
    if len(parts) > 1:
        try:
            bet_amount_str = parts[1]
            
            # Check if it's a percentage bet
            if bet_amount_str.endswith("%"):
                if current_balance is None:
                    return (False, {"error": "Percentage betting requires current balance"})
                    
                # Convert percentage to actual amount
                percentage = float(bet_amount_str.rstrip("%"))
                if percentage <= 0 or percentage > 100:
                    return (False, {"error": "Percentage must be between 0 and 100"})
                    
                betAmount = int(current_balance * percentage / 100)
            else:
                # Regular amount bet
                betAmount = int(bet_amount_str)
                
            if betAmount <= 0:
                return (False, {})
        except ValueError:
            return (False, {})
            
    # Return the quick bet information
    bet_info = ROULETTE_QUICK_BETS[bet_type].copy()
    bet_info["amount"] = betAmount
    
    # Add flag to indicate if this was a percentage bet
    if len(parts) > 1 and betAmount is not None:
        bet_info["is_percentage"] = "%" in parts[1]
    else:
        bet_info["is_percentage"] = False
    
    return (True, bet_info)
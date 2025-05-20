"""
Web Utilities for shygyGames Collection

This module provides shared utility functions for the web version 
of the shygyGames collection, including win streak tracking,
rewards handling, and other common functionality.

Functions in this module:
- getWinStreakReward: Calculate reward for a win streak
- processQuickBet: Process a quick bet command for Roulette
- checkSuperRocksChance: Process 1% chance for super Rock rewards
"""

import random
import json
from datetime import datetime

def getWinStreakReward(streak, game_name):
    """
    Calculate reward for a win streak.
    
    Args:
        streak (int): The current win streak
        game_name (str): The name of the game
        
    Returns:
        tuple: (reward_amount, message) or (0, "") if no reward
    """
    if streak < 3:
        return (0, "")
    
    # Base reward multipliers for different games
    baseMultipliers = {
        "roulette": 2,
        "blackjack": 2,
        "hangman": 1,
        "rps": 1.5,
        "highOrLow": 1,
        "masterMind": 2
    }
    
    # Use default multiplier if game not in dictionary
    multiplier = baseMultipliers.get(game_name, 1)
    
    # Reward tiers
    if streak == 3:
        reward = 15 * multiplier
    elif streak == 4:
        reward = 25 * multiplier
    elif streak == 5:
        reward = 40 * multiplier
    elif streak >= 6 and streak <= 9:
        reward = 60 * multiplier
    elif streak >= 10:
        reward = 100 * multiplier
    else:
        return (0, "")
    
    reward = int(reward)  # Ensure reward is an integer
    message = f"Win Streak Bonus! {streak} consecutive wins: +{reward} Rocks!"
    return (reward, message)

# Dictionary of preset quick bets for Roulette
ROULETTE_QUICK_BETS = {
    "quick:corners": {
        "description": "Bet on all four corner bets",
        "bets": [
            {"type": "corner", "numbers": [1, 2, 4, 5], "amount": 1},
            {"type": "corner", "numbers": [2, 3, 5, 6], "amount": 1},
            {"type": "corner", "numbers": [4, 5, 7, 8], "amount": 1},
            {"type": "corner", "numbers": [5, 6, 8, 9], "amount": 1}
        ],
        "total_units": 4
    },
    "quick:highrisk": {
        "description": "High risk bet with 70% on a straight-up number, 30% on red",
        "bets": [
            {"type": "straight", "numbers": [17], "amount": 70},
            {"type": "red", "numbers": [], "amount": 30}
        ],
        "total_units": 100
    },
    "quick:columns": {
        "description": "Bet equally on all three columns",
        "bets": [
            {"type": "column", "numbers": [1], "amount": 10},
            {"type": "column", "numbers": [2], "amount": 10},
            {"type": "column", "numbers": [3], "amount": 10}
        ],
        "total_units": 30
    },
    "quick:dozens": {
        "description": "Bet equally on all three dozens",
        "bets": [
            {"type": "dozen", "numbers": [1], "amount": 10},
            {"type": "dozen", "numbers": [2], "amount": 10},
            {"type": "dozen", "numbers": [3], "amount": 10}
        ],
        "total_units": 30
    },
    "quick:outside": {
        "description": "Bet equally on red, even, and high",
        "bets": [
            {"type": "red", "numbers": [], "amount": 10},
            {"type": "even", "numbers": [], "amount": 10},
            {"type": "high", "numbers": [], "amount": 10}
        ],
        "total_units": 30
    },
    "quick:conservative": {
        "description": "Bet equally on two columns and a dozen",
        "bets": [
            {"type": "column", "numbers": [1], "amount": 30},
            {"type": "column", "numbers": [2], "amount": 30},
            {"type": "dozen", "numbers": [3], "amount": 30}
        ],
        "total_units": 90
    }
}

def processQuickBet(command, rocks_available):
    """
    Process a quick bet command for Roulette in the web version.
    
    Args:
        command (str): The command entered by the user
        rocks_available (int): The number of rocks the player has available
        
    Returns:
        tuple: (bool, dict) - (True if it's a valid quick bet, bet information)
        
    Examples:
        >>> processQuickBet("quick:columns", 100)
        (True, {'description': 'Bet equally on all three columns', 'bets': [...], 'total_units': 30, 'rocks_per_unit': 3})
    """
    for key, bet_info in ROULETTE_QUICK_BETS.items():
        if command.lower().startswith(key.lower()):
            # Calculate rocks per unit based on available rocks
            total_units = bet_info["total_units"]
            rocks_per_unit = min(rocks_available // total_units, 10)  # Cap at 10 rocks per unit as default
            
            # If additional amount is specified, parse it
            parts = command.lower().split()
            if len(parts) > 1:
                try:
                    specified_rocks = int(parts[1])
                    rocks_per_unit = max(1, min(specified_rocks, rocks_available // total_units))
                except ValueError:
                    pass
                
            # Create a new bet info with calculated values
            result_info = bet_info.copy()
            result_info["rocks_per_unit"] = rocks_per_unit
            return (True, result_info)
            
    return (False, {})

def checkSuperRocksChance():
    """
    Check if player won super Rocks prize (1% chance)
    
    This function provides a 1% chance to win a 1000 Rock bonus on any win event.
    It's used throughout the games to provide exciting random rewards.
    
    Returns:
        tuple: (prize_amount, won_prize) - Amount of Rocks won and boolean if prize was won
    """
    roll = random.random()
    if roll <= 0.01:  # 1% chance
        prize_amount = 1000
        return prize_amount, True
    return 0, False

def logGameStats(game_name, player_id, rocks_won, win=True):
    """
    Log game statistics for analytics
    
    Args:
        game_name (str): The name of the game played
        player_id (str): Player's unique identifier
        rocks_won (int): Number of rocks won (negative for losses)
        win (bool): Whether the player won or lost
        
    Returns:
        bool: True if logging was successful, False otherwise
    """
    try:
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "game": game_name,
            "player_id": player_id,
            "rocks_change": rocks_won,
            "result": "win" if win else "loss"
        }
        
        # In a production environment, we would store this in a database
        # For now, we'll just return success
        return True
    except Exception as e:
        print(f"Error logging game stats: {str(e)}")
        return False

"""
Blackjack Game Module

This module implements a feature-rich Blackjack card game with advanced betting options:
- Split pairs into separate hands
- Double down on initial two cards
- Insurance when dealer shows an Ace
- Proper Blackjack rules (dealer hits until 17, etc.)

The game uses a virtual currency called "Rocks" for betting and keeps track
of player's winnings over multiple rounds of play.
"""

import random

# --- Constants ---
SUITS = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
RANKS = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
NUM_DECKS = 6  # Standard casino number of decks
DEALER_HIT_STAY_VALUE = 17  # Dealer must hit until reaching this value
RESHUFFLE_THRESHOLD = 0.2  # Reshuffle when deck is below 20% capacity

# --- Card Representation and Deck Management ---

def create_deck(num_decks):
    """
    Create and shuffle a new deck of cards.
    
    Args:
        num_decks (int): Number of standard 52-card decks to include
        
    Returns:
        list: A shuffled list of card strings in the format "Rank-Suit"
             (e.g., "A-Hearts", "10-Spades", "K-Diamonds")
    """
    print("\n--- Creating and Shuffling New Deck ---")
    deck = [f'{rank}-{suit}' for rank in RANKS for suit in SUITS] * num_decks
    random.shuffle(deck)
    return deck

def deal_card(deck, reshuffle_func):
    """
    Deal a single card from the deck, reshuffling if necessary.
    
    Args:
        deck (list): The current deck of cards
        reshuffle_func (function): A function that returns a new shuffled deck
                                  when called with no arguments
    
    Returns:
        str: A card string in the format "Rank-Suit"
    
    Note:
        This function modifies the deck list in-place by removing the dealt card.
        If the deck is empty, it will be replaced with a new shuffled deck.
    """
    if not deck:
        # Deck is empty, reshuffle and replace the deck
        deck[:] = reshuffle_func() # Use slice assignment to modify the list in place
        print("Deck was empty, a new one has been created and shuffled.")

    # Now the deck is guaranteed not to be empty (unless reshuffle_func returned an empty list, which it shouldn't)
    return deck.pop()

def get_rank(card):
    """
    Extract the rank portion from a card string.
    
    Args:
        card (str): A card string in the format "Rank-Suit"
    
    Returns:
        str: The rank portion of the card (e.g., 'A', 'K', '10', '2')
    
    Example:
        >>> get_rank('K-Spades')
        'K'
        >>> get_rank('10-Hearts')
        '10'
    """
    return card.split('-')[0]

# --- Hand Calculation ---

def calculate_hand_value(hand):
    """
    Calculate the total value of a Blackjack hand, accounting for Ace flexibility.
    
    In Blackjack, number cards are worth their face value, face cards (J,Q,K) are
    worth 10, and Aces can be worth either 1 or 11, whichever is more favorable
    to the hand without exceeding 21.
    
    Args:
        hand (list): A list of card strings in the format "Rank-Suit"
    
    Returns:
        int: The optimal total value of the hand according to Blackjack rules
    
    Example:
        >>> calculate_hand_value(['A-Hearts', 'K-Spades'])
        21  # Blackjack - Ace is counted as 11
        >>> calculate_hand_value(['A-Hearts', '5-Clubs', '10-Diamonds'])
        16  # Ace is counted as 1 to avoid busting
    """
    # Extract ranks from the full card strings
    ranks = [get_rank(card) for card in hand]

    # Count Aces for special handling
    ace_count = ranks.count('A')
    total = 0
    
    # First pass: calculate the initial total
    for rank in ranks:
        if rank.isdigit():
            total += int(rank)  # Number cards worth their face value
        elif rank in ('J', 'Q', 'K'):
            total += 10  # Face cards worth 10
        elif rank == 'A':
            total += 11  # Initially count Aces as 11
    
    # Second pass: adjust Aces from 11 to 1 as needed to avoid busting
    while total > 21 and ace_count > 0:
        total -= 10  # Change an Ace from 11 to 1
        ace_count -= 1
        
    return total

def is_blackjack(hand):
    """
    Check if a hand is a natural Blackjack.
    
    A natural Blackjack is a two-card hand with a value of 21, 
    consisting of an Ace and a 10-value card (10, J, Q, or K).
    
    Args:
        hand (list): A list of card strings in the format "Rank-Suit"
    
    Returns:
        bool: True if the hand is a natural Blackjack, False otherwise
    
    Example:
        >>> is_blackjack(['A-Hearts', 'K-Spades'])
        True
        >>> is_blackjack(['10-Hearts', '9-Spades', '2-Clubs'])
        False  # Not a natural Blackjack (more than 2 cards)
    """
    return len(hand) == 2 and calculate_hand_value(hand) == 21

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

def get_valid_bet(rocks):
    """
    Get a valid bet amount from the player.
    
    This function handles input validation to ensure the bet is:
    - A valid number
    - Greater than zero
    - Not more than the player's available rocks
    
    Args:
        rocks (int): The player's current rock balance
        
    Returns:
        int: A valid bet amount or -1 if the player wants to quit
    """
    while True:
        try:
            print(f"You have {rocks} Rocks.")
            bet_input = input("How much would you like to bet? ")
            
            # Check if player wants to quit
            if bet_input.lower() in ['quit', 'q', 'exit']:
                if confirm_quit():
                    return -1  # Signal to quit the game
                else:
                    continue
                    
            bet = int(bet_input)
            if bet <= 0:
                print("Please enter a positive bet amount.")
            elif bet > rocks:
                print(f"You don't have enough Rocks. You have {rocks} Rocks.")
            else:
                return bet
        except ValueError:
            print("Please enter a valid number.")

# --- Game Logic ---

def play_blackjack_round(deck, rocks):
    """
    Play a single round of Blackjack with advanced betting options.
    
    This function handles:
    - Taking bets from the player
    - Dealing initial cards
    - Processing insurance when dealer shows an Ace
    - Allowing player to split matching pairs
    - Handling double down on initial two cards
    - Implementing standard Blackjack rules for dealer and outcome determination
    - Handling player quitting the game at any point
    
    Args:
        deck (list): The current deck of cards
        rocks (int): The player's current rock balance for betting
        
    Returns:
        int: The updated rock balance after the round is complete,
             or None if the player decides to quit
        
    Note:
        This function modifies the deck in-place. The deck will be
        reshuffled automatically if needed during card dealing.
    """
    player_hand = []
    dealer_hand = []
    
    # Track whether player doubled down
    doubled_down = False
    
    # Use the separate betting function to get a valid bet
    bet = get_valid_bet(rocks)
    
    # Check if player wants to quit
    if bet == -1:
        return None  # Signal to quit the game
    
    # Initial deal
    # deal_card now handles reshuffling if needed
    player_hand.append(deal_card(deck, lambda: create_deck(NUM_DECKS)))
    dealer_hand.append(deal_card(deck, lambda: create_deck(NUM_DECKS)))
    player_hand.append(deal_card(deck, lambda: create_deck(NUM_DECKS)))
    dealer_hand.append(deal_card(deck, lambda: create_deck(NUM_DECKS)))


    print("\n--- New Round ---")
    print(f"Your initial hand: {player_hand}, value: {calculate_hand_value(player_hand)}")
    print(f"Dealer showing: [{dealer_hand[0]}, ?]") # Only show one dealer card

    player_blackjack = is_blackjack(player_hand)
    dealer_blackjack = is_blackjack(dealer_hand)

    # Check for Insurance opportunity (dealer's first card is an Ace)
    insurance_bet = 0
    if get_rank(dealer_hand[0]) == 'A' and rocks >= bet // 2:
        print("\nDealer is showing an Ace. Insurance?")
        print(f"Insurance costs {bet // 2} Rocks (half your bet).")
        while True:
            insurance_choice = input("Take insurance? (y/n): ").lower()
            
            # Check if player wants to quit
            if insurance_choice in ['quit', 'q', 'exit']:
                if confirm_quit():
                    return None  # Signal to quit the game
                else:
                    continue
                    
            if insurance_choice == 'y':
                insurance_bet = bet // 2
                rocks -= insurance_bet
                print(f"Insurance bet placed: {insurance_bet} Rocks")
                
                # If dealer has blackjack, insurance pays 2:1
                if dealer_blackjack:
                    print("Dealer has Blackjack!")
                    print(f"Insurance pays {insurance_bet * 2} Rocks!")
                    rocks += insurance_bet * 2
                    
                    if player_blackjack:
                        print("You also have Blackjack! It's a push on your main bet.")
                        return rocks + bet  # Return the original bet
                    else:
                        print("You lose your main bet.")
                        return rocks  # Insurance gain offsets the main bet loss
                else:
                    print("Dealer doesn't have Blackjack. You lose your insurance bet.")
                break
            elif insurance_choice == 'n':
                print("No insurance taken.")
                break
            else:
                print("Invalid choice. Please enter 'y' or 'n'.")

    # Check for immediate Blackjack
    if player_blackjack and dealer_blackjack:
        print(f"Dealer's hand: {dealer_hand}, value: {calculate_hand_value(dealer_hand)}")
        print("Both player and dealer have Blackjack! It's a push.")
        return rocks # Bet is returned, no change in rocks
    elif player_blackjack:
        print("Blackjack! You win 3:2 on your bet!")
        print(f"Dealer's hand: {dealer_hand}, value: {calculate_hand_value(dealer_hand)}") # Reveal dealer's hand
        return rocks + int(bet * 1.5) # 3:2 payout for blackjack
    elif dealer_blackjack:
        print("Dealer has Blackjack! You lose your bet.")
        print(f"Dealer's hand: {dealer_hand}, value: {calculate_hand_value(dealer_hand)}") # Reveal dealer's hand
        return rocks - bet # Player loses bet

    # Check if player can split (same rank cards and enough rocks)
    can_split = (get_rank(player_hand[0]) == get_rank(player_hand[1])) and (rocks >= bet)
    # Check if player can double down (enough rocks for another bet)
    can_double_down = (rocks >= bet)
    
    # Track split hands if player decides to split
    split_hands = []
    
    # Player's turn (only if no immediate Blackjack)
    if can_split:
        player_value = calculate_hand_value(player_hand)
        print(f"\nYour hand: {player_hand}, value: {player_value}")
        print("You have a pair. Would you like to split?")
        
        while True:
            split_choice = input("Split your hand? (y/n): ").lower()
            
            # Check if player wants to quit
            if split_choice in ['quit', 'q', 'exit']:
                if confirm_quit():
                    return None  # Signal to quit the game
                else:
                    continue
                    
            if split_choice == 'y':
                # Create two hands from the pair
                second_card = player_hand.pop()
                split_hands.append([player_hand[0], deal_card(deck, lambda: create_deck(NUM_DECKS))])
                split_hands.append([second_card, deal_card(deck, lambda: create_deck(NUM_DECKS))])
                
                # Use additional bet for the second hand
                rocks -= bet
                print(f"Split your hand. Using another {bet} Rocks for the second hand.")
                
                # Play each split hand separately
                for i, hand in enumerate(split_hands):
                    player_hand = hand  # Set current hand for play
                    
                    print(f"\n--- Playing Split Hand {i+1} ---")
                    print(f"Hand: {player_hand}, value: {calculate_hand_value(player_hand)}")
                    
                    # Play this split hand
                    while True:
                        player_value = calculate_hand_value(player_hand)
                        
                        if player_value > 21:
                            print(f"Split hand {i+1} busts with {player_value}!")
                            break
                        
                        choice = input("Hit or Stand? (h/s): ").lower()
                        if choice in ['quit', 'q', 'exit']:
                            if confirm_quit():
                                return None  # Signal to quit the game
                            else:
                                # Continue playing without taking an action
                                continue
                        elif choice == 'h':
                            player_hand.append(deal_card(deck, lambda: create_deck(NUM_DECKS)))
                            print(f"Hand: {player_hand}, value: {calculate_hand_value(player_hand)}")
                        elif choice == 's':
                            break
                        else:
                            print("Invalid choice. Please enter 'h' or 's'.")
                    
                    # Update the split hand with modifications
                    split_hands[i] = player_hand
                
                # After all split hands are played, proceed to dealer's turn
                print("\n--- Dealer's Turn ---")
                print(f"Dealer's hand: {dealer_hand}, value: {calculate_hand_value(dealer_hand)}")
                
                # Dealer plays according to standard rules
                while calculate_hand_value(dealer_hand) < DEALER_HIT_STAY_VALUE:
                    print("Dealer hits.")
                    dealer_hand.append(deal_card(deck, lambda: create_deck(NUM_DECKS)))
                    print(f"Dealer's hand: {dealer_hand}, value: {calculate_hand_value(dealer_hand)}")
                
                dealer_value = calculate_hand_value(dealer_hand)
                
                # Evaluate results for each split hand
                total_winnings = 0
                for i, hand in enumerate(split_hands):
                    hand_value = calculate_hand_value(hand)
                    print(f"\n--- Result for Split Hand {i+1} ---")
                    print(f"Your hand: {hand}, value: {hand_value}")
                    print(f"Dealer's hand: {dealer_hand}, value: {dealer_value}")
                    
                    if hand_value > 21:
                        print(f"Split hand {i+1} busted. Bet lost.")
                    elif dealer_value > 21:
                        print(f"Dealer busts! Split hand {i+1} wins!")
                        total_winnings += bet * 2  # Win amount is original bet
                    elif hand_value > dealer_value:
                        print(f"Split hand {i+1} wins!")
                        total_winnings += bet * 2  # Win amount is original bet
                    elif hand_value < dealer_value:
                        print(f"Split hand {i+1} loses.")
                    else:
                        print(f"Split hand {i+1} pushes.")
                        total_winnings += bet  # Return bet for push
                
                print(f"\nTotal winnings from split hands: {total_winnings} Rocks")
                return rocks + total_winnings
                
            elif split_choice == 'n':
                print("You chose not to split.")
                break
            else:
                print("Invalid choice. Please enter 'y' or 'n'.")
    
    # Regular play (no split) or player declined split
    while True:
        player_value = calculate_hand_value(player_hand)
        print(f"\nYour hand: {player_hand}, value: {player_value}")

        if player_value > 21:
            print("Bust! You lose your bet.")
            return rocks - bet # Player loses bet

        # On first decision, offer double down if possible
        if len(player_hand) == 2 and can_double_down:
            choice = input("Hit, Stand, or Double Down? (h/s/d): ").lower()
            
            # Check if player wants to quit
            if choice in ['quit', 'q', 'exit']:
                if confirm_quit():
                    return None  # Signal to quit the game
                else:
                    continue
                    
            if choice == 'd':
                print(f"Doubling down! Additional bet: {bet} Rocks")
                rocks -= bet  # Double the bet
                bet *= 2
                doubled_down = True  # Set the flag to indicate double down
                
                # Deal one more card and then stand
                player_hand.append(deal_card(deck, lambda: create_deck(NUM_DECKS)))
                player_value = calculate_hand_value(player_hand)
                print(f"Your hand after doubling down: {player_hand}, value: {player_value}")
                
                if player_value > 21:
                    print("Bust! You lose your doubled bet.")
                    return rocks # Already deducted the bet twice
                break  # Proceed to dealer's turn
        else:
            choice = input("Hit or Stand? (h/s): ").lower()
            
            # Check if player wants to quit
            if choice in ['quit', 'q', 'exit']:
                if confirm_quit():
                    return None  # Signal to quit the game
                else:
                    continue
            
        if choice == 'h':
            player_hand.append(deal_card(deck, lambda: create_deck(NUM_DECKS)))
        elif choice == 's':
            break # Player stands
        else:
            print("Invalid choice. Please enter 'h' or 's'.")

    # Dealer's turn (only if player hasn't busted or had Blackjack)
    player_value = calculate_hand_value(player_hand) # Final player value
    if player_value <= 21:
        print(f"\nDealer's turn. Dealer's hand: {dealer_hand}, value: {calculate_hand_value(dealer_hand)}")
        while calculate_hand_value(dealer_hand) < DEALER_HIT_STAY_VALUE:
            print("Dealer hits.")
            dealer_hand.append(deal_card(deck, lambda: create_deck(NUM_DECKS)))
            print(f"Dealer's hand: {dealer_hand}, value: {calculate_hand_value(dealer_hand)}")

        dealer_value = calculate_hand_value(dealer_hand)

        # Determine the winner
        print("\n--- Final Hands ---")
        print(f"Your hand: {player_hand}, value: {player_value}")
        print(f"Dealer's hand: {dealer_hand}, value: {dealer_value}")

        # Add doubled message if player doubled down
        doubled_msg = " (doubled)" if doubled_down else ""
        
        if dealer_value > 21:
            print(f"Dealer busts! You win your bet{doubled_msg}!")
            return rocks + bet # Player wins bet
        elif dealer_value > player_value:
            print(f"Dealer wins. You lose your bet{doubled_msg}.")
            return rocks - bet # Player loses bet
        elif dealer_value < player_value:
            print(f"You win! You win your bet{doubled_msg}!")
            return rocks + bet # Player wins bet
        else:
            print(f"It's a push. Your bet{doubled_msg} is returned.")
            return rocks # Bet is returned, no change in rocks

# --- Main Game Loop ---

def mainBlackjack():
    """
    Main function to run the Blackjack game with a play again loop and Rocks betting.
    
    This function handles:
    - Initializing the game with a fresh deck and starting rocks
    - Managing the deck and reshuffling when cards run low
    - Tracking the player's Rock balance throughout multiple rounds
    - Providing emergency rocks when the player runs out
    - Controlling the overall game flow and play again loop
    
    Returns:
        None: This function doesn't return a value, but prints game state and results
    """
    print("Welcome to Blackjack!")
    print("You start with 100 Rocks.")
    
    # Initial deck creation
    current_deck = create_deck(NUM_DECKS)
    total_cards_in_deck = len(current_deck) # Store initial size for reshuffle threshold
    
    # Player starts with 100 Rocks (betting currency)
    rocks = 100

    while True:
        # Check if deck is below reshuffle threshold before starting a new round
        if len(current_deck) < (total_cards_in_deck * RESHUFFLE_THRESHOLD):
             print("\nDeck is getting low. Reshuffling...")
             current_deck = create_deck(NUM_DECKS)
             total_cards_in_deck = len(current_deck) # Update total size
             
        # Check if player is out of Rocks
        if rocks <= 0:
            print("You're out of Rocks! Here's 50 more to keep playing.")
            rocks = 50

        # Pass the current_deck to the round function
        # The round function now returns the updated rocks amount or None if player quits
        new_rocks = play_blackjack_round(current_deck, rocks)
        
        # Check if player chose to quit
        if new_rocks is None:
            print(f"\nThanks for playing! You finished with {rocks} Rocks.")
            return
            
        rocks = new_rocks

        # Ask to play again
        while True:
            play_again = input("Play again? (y/n): ").lower()
            
            # Check if player wants to quit
            if play_again in ['quit', 'q', 'exit']:
                if confirm_quit():
                    return  # Exit the game
                else:
                    continue  # Let the player choose again
                    
            if play_again in ('y', 'n'):
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

        if play_again == 'n':
            break

    print(f"Thanks for playing! You ended with {rocks} Rocks.")

# Run the main game function

def blackjackLoop():
  """
  Entry point for the Blackjack game.
  
  This function serves as the main entry point when the game is selected
  from the game selector menu or run directly. It provides a clean interface
  for external modules to start the game without worrying about implementation
  details.
  
  Returns:
      None: This function doesn't return a value, but starts the Blackjack game
  """
  try:
    print("\n" + "=" * 60)
    print(" " * 20 + "BLACKJACK")
    print("=" * 60)
    print("\nWelcome to Blackjack! Test your luck and skill against the dealer.")
    print("Try to get as close to 21 as possible without going over.")
    print("\nAdvanced features include:")
    print("- Splitting pairs into separate hands")
    print("- Doubling down on your initial two cards")
    print("- Insurance when the dealer shows an Ace")
    print("- Standard casino rules (dealer hits until 17)")
    print("\nGood luck!\n")
    
    # Small delay for better user experience
    import time
    time.sleep(1)
    
    # Start the main game
    mainBlackjack()
  except KeyboardInterrupt:
    print("\nGame interrupted. Returning to game selector...")
  except Exception as e:
    print(f"\nError occurred: {e}")
    print("Returning to game selector...")

if __name__ == "__main__":
  blackjackLoop()
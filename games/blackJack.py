import random

# --- Constants ---
SUITS = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
RANKS = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
NUM_DECKS = 6  # Standard casino number of decks
DEALER_HIT_STAY_VALUE = 17
RESHUFFLE_THRESHOLD = 0.2 # Reshuffle when deck is below 20% capacity

# --- Card Representation and Deck Management ---

# We need the deck to be mutable and accessible/modifiable by deal_card
# Making it a list that gets passed around or recreating it is key.
# Let's manage the single, current deck instance in the main loop
# and pass it to deal_card.

def create_deck(num_decks):
    """Creates a deck of cards (Rank-Suit strings) and shuffles it."""
    print("\n--- Creating and Shuffling New Deck ---")
    deck = [f'{rank}-{suit}' for rank in RANKS for suit in SUITS] * num_decks
    random.shuffle(deck)
    return deck

# deal_card will now receive and modify the deck list directly
def deal_card(deck, reshuffle_func):
    """
    Deals a single card from the deck.
    If the deck is empty, it calls the reshuffle_func to get a new deck.
    Returns the dealt card.
    """
    if not deck:
        # Deck is empty, reshuffle and replace the deck
        deck[:] = reshuffle_func() # Use slice assignment to modify the list in place
        print("Deck was empty, a new one has been created and shuffled.")

    # Now the deck is guaranteed not to be empty (unless reshuffle_func returned an empty list, which it shouldn't)
    return deck.pop()

def get_rank(card):
    """Extracts the rank from a card string (e.g., 'King-Spades' -> 'King')."""
    return card.split('-')[0]

# --- Hand Calculation ---

def calculate_hand_value(hand):
    """Calculates the value of a hand in Blackjack."""
    # Extract ranks from the full card strings
    ranks = [get_rank(card) for card in hand]

    ace_count = ranks.count('A')
    total = 0
    for rank in ranks:
        if rank.isdigit():
            total += int(rank)
        elif rank in ('J', 'Q', 'K'):
            total += 10
        elif rank == 'A':
            total += 11 # Start by assuming Ace is 11

    # Adjust for Aces if the total is over 21
    while total > 21 and ace_count > 0:
        total -= 10 # Change an Ace from 11 to 1
        ace_count -= 1
    return total

def is_blackjack(hand):
    """Checks if a hand is a natural Blackjack (Ace and a 10-value card in two cards)."""
    return len(hand) == 2 and calculate_hand_value(hand) == 21

# --- Game Logic ---

def play_blackjack_round(deck, rocks):
    """Plays a single round of Blackjack with betting."""
    player_hand = []
    dealer_hand = []
    
    # Ask for bet
    while True:
        try:
            print(f"You have {rocks} Rocks.")
            bet = int(input("How much would you like to bet? "))
            if bet <= 0:
                print("Please enter a positive bet amount.")
            elif bet > rocks:
                print(f"You don't have enough Rocks. You have {rocks} Rocks.")
            else:
                break
        except ValueError:
            print("Please enter a valid number.")
    
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

    # Player's turn (only if no immediate Blackjack)
    while True:
        player_value = calculate_hand_value(player_hand)
        print(f"\nYour hand: {player_hand}, value: {player_value}")

        if player_value > 21:
            print("Bust! You lose your bet.")
            return rocks - bet # Player loses bet

        choice = input("Hit or Stand? (h/s): ").lower()
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

        if dealer_value > 21:
            print("Dealer busts! You win your bet!")
            return rocks + bet # Player wins bet
        elif dealer_value > player_value:
            print("Dealer wins. You lose your bet.")
            return rocks - bet # Player loses bet
        elif dealer_value < player_value:
            print("You win! You win your bet!")
            return rocks + bet # Player wins bet
        else:
            print("It's a push. Your bet is returned.")
            return rocks # Bet is returned, no change in rocks

# --- Main Game Loop ---

def mainBlackjack():
    """Main function to run the Blackjack game with a play again loop and Rocks betting."""
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
        # The round function now returns the updated rocks amount
        rocks = play_blackjack_round(current_deck, rocks)

        # Ask to play again
        while True:
            play_again = input("Play again? (y/n): ").lower()
            if play_again in ('y', 'n'):
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

        if play_again == 'n':
            break

    print(f"Thanks for playing! You ended with {rocks} Rocks.")

# Run the main game function

def blackjackLoop():
  """Entry point for the game"""
  mainBlackjack()
if __name__ == "__main__":
  blackjackLoop()

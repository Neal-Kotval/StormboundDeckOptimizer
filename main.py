# Function to calculate total wasted mana (MW_t) for turn t
import itertools

# Function to calculate total wasted mana (MW_t) for turn t
# Function to calculate total wasted mana (MW_t) for each turn
def calculate_total_wasted_mana(deck, max_turn, starting_mana=3):
    total_mana = 0
    
    for i in range (starting_mana, max_turn + 1):
        # Generate all possible unique hands (combinations of 4 cards from the deck)
        possible_deck_indices = range(1, 13)
        possible_index_hands = list(itertools.combinations(deck, 4))
        possible_hands = list(itertools.combinations(deck, 4))
        
        total_wasted_mana = 0
        
        for hand in possible_hands:
            # Generate all subsets of the hand
            subsets = list(itertools.chain.from_iterable(itertools.combinations(hand, r) for r in range(1, len(hand) + 1)))
            # Find the subset that maximizes mana usage under the budget
            max_mana_used = 0
            for subset in subsets:
                mana_sum = sum(subset)
                
                if mana_sum <= i and mana_sum > max_mana_used:
                    max_mana_used = mana_sum
            
            # Calculate wasted mana for this hand
            wasted_mana = i - max_mana_used
            total_wasted_mana += wasted_mana
        
        total_mana += total_wasted_mana
    
    return total_mana

deck=[1,1,1,1,1,1,1,1,1,1,1,1]

# Calculate the total wasted mana
print(calculate_total_wasted_mana(deck, 12))

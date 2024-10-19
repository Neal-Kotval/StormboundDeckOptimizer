import itertools

# Function to calculate the average wasted mana across multiple turns
def calculate_avg_wasted_mana(deck, max_turn, starting_mana=3):
    total_mana = 0
    # Generate all possible unique hands (combinations of 4 cards from the deck)
    possible_indices = range(1, 13)
    possible_hands = list(itertools.combinations(possible_indices, 4))
    max_subsets = []
    
    for current_turn in range(starting_mana, max_turn + 1):
        if current_turn != starting_mana:
            for p in range(len(possible_hands)):  # 495 possible hands
                possible_hands[p] = tuple([x for x in possible_hands[p] if x not in max_subsets[p]])

            filled_hands = []  # Store hands completed to 4 elements
            hand_index = 0
            
            for tup in possible_hands:
                num_elements = len(tup)
                missing_elements = 4 - num_elements
                
                if missing_elements > 0:
                    available_elements = set(range(1, 13)) - set(max_subsets[hand_index]) - set(tup)
                    combinations = itertools.product(available_elements, repeat=missing_elements)
                    
                    # Add each combination to the original tuple
                    for combo in combinations:
                        completed_tuple = tup + combo
                        filled_hands.append(completed_tuple)
                else:
                    # If the tuple already has 4 elements, just add it as is
                    filled_hands.append(tup)
                
                hand_index += 1
            
            possible_hands = filled_hands

        max_subsets = []
        counts = [0] * 12  # Track the number of times each card is used
        total_wasted_mana = 0
        
        for hand in possible_hands:
            # Generate all subsets of the hand
            subsets = list(itertools.chain.from_iterable(itertools.combinations(hand, r) for r in range(1, len(hand) + 1)))
            # Find the subset that maximizes mana usage under the budget
            max_mana_used = 0
            max_subset = []

            for subset in subsets:
                mana_sum = sum([deck[l-1] for l in subset])
                
                if mana_sum <= current_turn and mana_sum > max_mana_used:
                    max_mana_used = mana_sum
                    max_subset = subset
                elif mana_sum <= current_turn and mana_sum > max_mana_used and len(subset) > len(max_subset):
                    max_subset = subset

            # Calculate wasted mana for this hand
            wasted_mana = current_turn - max_mana_used
            total_wasted_mana += wasted_mana
            max_subsets.append(max_subset)

        # Calculate average wasted mana per hand
        avg_wasted_mana_per_hand = total_wasted_mana / len(max_subsets)
        total_mana += avg_wasted_mana_per_hand
    
    return total_mana / (max_turn - starting_mana)

# Example deck with mana values
deck = [1, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 6]

# Calculate the total wasted mana
print("TOTAL MANA", calculate_avg_wasted_mana(deck, 8))

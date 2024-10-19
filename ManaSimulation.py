import itertools

class ManaSimulation:
    def __init__(self, deck, max_turn, starting_mana=3):
        """
        Initialize the simulation with a deck, maximum turns, and starting mana.
        """
        self.deck = deck  # The deck of cards
        self.max_turn = max_turn  # The maximum number of turns
        self.starting_mana = starting_mana  # Starting mana for the simulation
        self.possible_indices = range(1, 13)  # Card indices (1 to 12)
        self.possible_hands = list(itertools.combinations(self.possible_indices, 4))  # All combinations of hands (4 cards each)]
        self.max_subset_identifiers = []
        self.max_subsets_history = []

    def fill_hands(self, max_subsets):
        """
        Fill hands with combinations to reach 4 elements.
        """
        filled_hands = []
        for hand_index, hand in enumerate(self.possible_hands):
            num_elements = len(hand)
            missing_elements = 4 - num_elements

            if missing_elements > 0:
                available_elements = set(self.possible_indices) - set(max_subsets[hand_index]) - set(hand)
                combinations = itertools.product(available_elements, repeat=missing_elements)
                
                for combo in combinations:
                    completed_tuple = hand + combo
                    filled_hands.append(completed_tuple)
            else:
                filled_hands.append(hand)

        return filled_hands

    def calculate_avg_wasted_mana(self):
        """
        Calculate the average wasted mana across multiple turns.
        """
        total_mana = 0
        max_subsets = []

        for current_turn in range(self.starting_mana, self.max_turn + 1):
            if current_turn != self.starting_mana:
                for p in range(len(self.possible_hands)):
                    self.possible_hands[p] = tuple([x for x in self.possible_hands[p] if x not in max_subsets[p]])

                # Fill hands for the next turn
                self.possible_hands = self.fill_hands(max_subsets)

            max_subsets = []
            total_wasted_mana = 0

            for hand in self.possible_hands:
                # Generate all subsets of the hand
                subsets = list(itertools.chain.from_iterable(itertools.combinations(hand, r) for r in range(1, len(hand) + 1)))
                # Find the subset that maximizes mana usage under the budget
                max_mana_used = 0
                max_subset = []

                for subset in subsets:
                    mana_sum = sum([self.deck[l-1] for l in subset])

                    if mana_sum <= current_turn and mana_sum > max_mana_used:
                        max_mana_used = mana_sum
                        max_subset = subset
                    elif mana_sum <= current_turn and mana_sum > max_mana_used and len(subset) > len(max_subset):
                        max_subset = subset

                # Calculate wasted mana for this hand
                wasted_mana = current_turn - max_mana_used
                total_wasted_mana += wasted_mana

                #add optimal subset to list of optimal subsets, add empty history array to track past data
                max_subsets.append(max_subset)

            # Calculate average wasted mana per hand
            avg_wasted_mana_per_hand = total_wasted_mana / len(max_subsets)
            total_mana += avg_wasted_mana_per_hand

        return total_mana / (self.max_turn - self.starting_mana)



# Example usage
deck = [1, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 6]
simulation = ManaSimulation(deck, max_turn=8)
print("TOTAL MANA:", simulation.calculate_avg_wasted_mana())

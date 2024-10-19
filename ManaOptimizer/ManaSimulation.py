import itertools
import numpy as np
from tqdm import tqdm

class ManaSimulation:
    def __init__(self, deck, max_turn, starting_mana=3):
        """
        Initialize the simulation with a deck, maximum turns, and starting mana.
        """
        self.deck = np.array(deck)  # The deck of cards
        self.max_turn = max_turn  # The maximum number of turns
        self.starting_mana = starting_mana  # Starting mana for the simulation
        self.possible_indices = range(1, 13)  # Card indices (1 to 12)
        self.possible_hands = [tuple(sorted(hand)) for hand in itertools.combinations(self.possible_indices, 4)]  # Pre-sort hands  # All combinations of hands (4 cards each)]
        self.base_hands = [tuple(sorted(hand)) for hand in itertools.combinations(self.possible_indices, 4)]
        self.max_subsets_history = []
        self.optimal_subsets = self.precompute_max_subsets()
        self.future_hand_counts = np.zeros(495, dtype=int)

    def precompute_max_subsets(self):
        """
        Precompute the maximal subsets for each possible hand based on each turn's mana budget.
        Returns a list where each item is a dictionary mapping hands to their maximal subsets.
        """
        turns = []
        for current_turn in range(self.starting_mana, self.max_turn + 1):
            turn_dict = {}  # Dictionary for this turn

            for hand in self.possible_hands:
                subsets = itertools.chain.from_iterable(itertools.combinations(hand, r) for r in range(1, len(hand) + 1))
                max_mana_used, max_subset = 0, []

                # Find the maximal subset for the current turn's mana budget
                for subset in subsets:
                    mana_sum = sum([self.deck[l-1] for l in subset])
                    
                    if mana_sum <= current_turn and mana_sum > max_mana_used:
                        max_mana_used = mana_sum
                        max_subset = subset

                # Store the maximal subset for this hand and turn
                turn_dict[tuple(sorted(hand))] = max_subset

            # Append this turn's dictionary to the list
            turns.append(turn_dict)

        return turns

    def fill_hands(self, max_subsets):
        """
        Fill hands with combinations to reach 4 elements.
        """
        filled_hands = []
        new_history = []
        for hand_index, hand in enumerate(self.possible_hands):
            num_elements = len(hand)
            missing_elements = 4 - num_elements

            if missing_elements > 0:
                available_elements = set(self.possible_indices) - set(self.max_subsets_history[hand_index]) - set(hand)
                # if hand_index==0:
                #     print(available_elements)
                combinations = itertools.combinations(available_elements, 4 - len(hand))
                # if hand_index==0:
                #     print([hand+x for x in combinations])
                for combo in combinations:
                    completed_tuple = tuple(sorted(hand + combo))
                    filled_hands.append(completed_tuple)
                    new_history.append(self.max_subsets_history[hand_index])
                    self.future_hand_counts[self.base_hands.index(completed_tuple)]+=1
            else:
                filled_hands.append(tuple(sorted(hand)))
                new_history.append(self.max_subsets_history[hand_index])
                self.future_hand_counts[self.base_hands.index(hand)]+=1
        filled_hands.sort()
        new_history = [x for _, x in sorted(zip(filled_hands, new_history), key=lambda pair: pair[0])]
        # print(filled_hands[0:10])
        return filled_hands, new_history

    def calculate_avg_wasted_mana(self):
        """
        Calculate the average wasted mana across multiple turns.
        """
        total_mana = 0
        max_subsets = []

        for current_turn in range(self.starting_mana, self.max_turn + 1):
            if current_turn != self.starting_mana:
                for p in range(len(self.possible_hands)):
                    self.possible_hands[p] = tuple([x for x in self.possible_hands[p] if x not in self.max_subsets_history[p][-8:]])
                # Fill hands for the next turn
                self.possible_hands, self.max_subsets_history = self.fill_hands(max_subsets)
            max_subsets = []
            total_wasted_mana = 0
            h=0
            for hand in tqdm(self.base_hands, desc="Processing Mana {0}".format(current_turn)):
                max_subset = self.optimal_subsets[current_turn-3][hand]
                if max_subset:
                    max_mana_used = np.sum(self.deck[np.array(max_subset) - 1])
                else:
                    max_mana_used=0

                # Calculate wasted mana for this hand
                if current_turn != self.starting_mana:
                    wasted_mana = (current_turn - max_mana_used)*self.future_hand_counts[h]
                else:
                    wasted_mana = (current_turn - max_mana_used)
                total_wasted_mana += wasted_mana

                #add optimal subset to list of optimal subsets
                if current_turn == self.starting_mana:
                    max_subsets.append(max_subset)
                else:
                    for i in range(self.future_hand_counts[h]):
                        max_subsets.append(max_subset)

                if current_turn == self.starting_mana:
                    self.max_subsets_history=max_subsets.copy()
                else:
                    # print("doing???")
                    for index, maximal in enumerate(max_subsets):
                        self.max_subsets_history[index] = tuple(self.max_subsets_history[index])+tuple(maximal)
                    # print("done???")

                h+=1
            print(len(self.max_subsets_history))


            # Calculate average wasted mana per hand
            self.future_hand_counts.fill(0)
            avg_wasted_mana_per_hand = total_wasted_mana / len(max_subsets)
            total_mana += avg_wasted_mana_per_hand
        return total_mana / (self.max_turn - self.starting_mana)



# Example usage
deck = [1, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 6]
simulation = ManaSimulation(deck, max_turn=4)
print("AVG MANA WASTE:", simulation.calculate_avg_wasted_mana())

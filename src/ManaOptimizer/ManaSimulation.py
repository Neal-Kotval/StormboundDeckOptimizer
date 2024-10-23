import itertools
import numpy as np
from tqdm import tqdm
import math

class ManaSimulation:
    def __init__(self, deck, max_turn, starting_mana=3, debug=False):
        """
        Initialize the simulation with a deck, maximum turns, and starting mana.
        """
        self.cards_in_hand = 5
        self.deck = np.array(deck)  # The deck of cards
        self.max_turn = max_turn  # The maximum number of turns
        self.starting_mana = starting_mana  # Starting mana for the simulation
        self.possible_indices = range(1, 13)  # Card indices (1 to 12)
        self.possible_hands = [tuple(sorted(hand)) for hand in itertools.combinations(self.possible_indices, self.cards_in_hand)]  # Pre-sort hands  # All combinations of hands (4 cards each)]
        self.base_hands = [tuple(sorted(hand)) for hand in itertools.combinations(self.possible_indices, self.cards_in_hand)]
        self.max_subsets_history = []
        self.optimal_subsets = self.precompute_max_subsets()
        self.future_hand_counts = np.zeros(math.comb(12, self.cards_in_hand), dtype=int)
        self.debug = debug
        deck_copy = deck.copy()
        deck_copy.sort()
        print(deck_copy)

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
                    
                    if mana_sum <= current_turn and mana_sum > max_mana_used and len(max_subset)<5:
                        max_mana_used = mana_sum
                        max_subset = subset

                # Store the maximal subset for this hand and turn
                turn_dict[tuple(sorted(hand))] = max_subset

            # Append this turn's dictionary to the list
            turns.append(turn_dict)

        return turns

    def fill_hands(self):
        """
        Fill hands with combinations to reach 4 elements.
        """
        filled_hands = []
        new_history = []
        
        base_hands_dict = {hand: idx for idx, hand in enumerate(self.base_hands)}
        available_indices_np = np.array(self.possible_indices)  # Convert indices to Numpy array for faster operations
        
        for hand_index, hand in enumerate(self.possible_hands):
            hand_np = np.array(hand)  # Convert hand to Numpy array for faster operations
            num_elements = len(hand)
            missing_elements = self.cards_in_hand - num_elements
            
            if missing_elements > 0:
                # Use Numpy's set difference for faster element exclusion
                available_elements = np.setdiff1d(available_indices_np, np.union1d(hand_np, np.array(self.max_subsets_history[hand_index])))

                # Generate all combinations of available elements to fill the hand
                combinations = itertools.combinations(available_elements, missing_elements)
                
                for combo in combinations:
                    completed_tuple = tuple(sorted(np.concatenate((hand_np, combo))))
                    filled_hands.append(completed_tuple)
                    new_history.append(self.max_subsets_history[hand_index])
                    self.future_hand_counts[base_hands_dict[completed_tuple]] += 1
            else:
                filled_hands.append(hand)
                new_history.append(self.max_subsets_history[hand_index])
                self.future_hand_counts[base_hands_dict[hand]] += 1

        # There's no need to sort again here, just return the results
        return filled_hands, new_history

    def calculate_avg_wasted_mana(self):
        """
        Calculate the average wasted mana across multiple turns.
        """
        total_mana = 0
        max_subsets = []

        for current_turn in range(self.starting_mana, self.max_turn+1):
            if current_turn != self.starting_mana:
                for p in range(len(self.possible_hands)):
                    self.possible_hands[p] = tuple([x for x in self.possible_hands[p] if x not in self.max_subsets_history[p][-8:]])
                # Fill hands for the next turn
                self.possible_hands, self.max_subsets_history = self.fill_hands()
            max_subsets = []
            total_wasted_mana = 0
            h=0
            if self.debug:
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
                    h+=1
            else:
                for hand in self.base_hands:
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
                    h+=1

            if current_turn == self.starting_mana:
                self.max_subsets_history=max_subsets.copy()
            else:
                for index, maximal in enumerate(max_subsets):
                    self.max_subsets_history[index] = tuple(self.max_subsets_history[index])+tuple(maximal)

            # Calculate average wasted mana per hand
            self.future_hand_counts.fill(0)
            avg_wasted_mana_per_hand = total_wasted_mana / len(max_subsets)
            total_mana += avg_wasted_mana_per_hand
        print("AMW", total_mana / (self.max_turn - self.starting_mana))
        return total_mana / (self.max_turn - self.starting_mana)
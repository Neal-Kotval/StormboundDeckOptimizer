import itertools
import random

# Function to calculate total wasted mana (MW_t) for each turn
def calculate_total_wasted_mana(deck, max_turn, starting_mana=3):
    total_mana = 0
    # Generate all possible unique hands (combinations of 4 cards from the deck)
    possible_indices = range(1, 13)
    possible_hands = list(itertools.combinations(possible_indices, 4))
    weights = [0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range (starting_mana, max_turn + 1):
        counts = [0,0,0,0,0,0,0,0,0,0,0,0]
        total_wasted_mana = 0
        for hand in possible_hands:
            # Generate all subsets of the hand
            subsets = list(itertools.chain.from_iterable(itertools.combinations(hand, r) for r in range(1, len(hand) + 1)))
            # Find the subset that maximizes mana usage under the budget
            max_mana_used = 0
            max_subset = []

            for subset in subsets:
                mana_sum = sum([deck[l-1] for l in subset])
                
                if mana_sum <= i and mana_sum > max_mana_used:
                    max_mana_used = mana_sum
                    max_subset = subset
                elif mana_sum <= i and mana_sum > max_mana_used and len(subset)>len(max_subset):
                    max_subset = subset
        
        # Calculate wasted mana for this hand
            wasted_mana = i - max_mana_used
            total_wasted_mana += wasted_mana
            # for card in max_subset:
            #     counts[card-1]+=1
            # for g in range(12):
            #     weights[g] = counts[g]/sum(counts)
        avg_hand_mana_waste = total_wasted_mana/459
        total_mana += avg_hand_mana_waste
    
    return total_mana/(max_turn-starting_mana)

# Genetic Algorithm Functions

def create_random_deck(deck_size=12, max_mana=9):
    """Create a random deck with `deck_size` cards, where each card has a mana value between 1 and `max_mana`."""
    return [random.randint(1, max_mana) for _ in range(deck_size)]

def mutate_deck(deck, max_mana=9, mutation_rate=0.1):
    """Mutate the deck by randomly changing a card's mana value with a certain probability (mutation_rate)."""
    for i in range(len(deck)):
        if random.random() < mutation_rate:
            deck[i] = random.randint(1, max_mana)
    return deck

def crossover_decks(deck1, deck2):
    """Crossover between two decks to create a new deck (combining parts of both decks)."""
    crossover_point = random.randint(1, len(deck1) - 2)
    return deck1[:crossover_point] + deck2[crossover_point:]

def genetic_algorithm(population_size=100, generations=50, mutation_rate=0.1, max_turn=12):
    # Create an initial population of random decks
    population = [create_random_deck() for _ in range(population_size)]
    
    for generation in range(generations):
        # Evaluate fitness of each deck (lower mana wastage is better)
        population = sorted(population, key=lambda deck: calculate_total_wasted_mana(deck, max_turn))
        
        # Keep the top 10% of the population as "elite"
        elite_size = int(0.1 * population_size)
        new_population = population[:elite_size]
        
        # Create the rest of the population through crossover and mutation
        while len(new_population) < population_size:
            # Select two random parents from the elite population
            parent1 = random.choice(population[:elite_size])
            parent2 = random.choice(population[:elite_size])
            
            # Crossover to create a new deck
            child = crossover_decks(parent1, parent2)
            
            # Mutate the new deck
            child = mutate_deck(child, mutation_rate=mutation_rate)
            
            new_population.append(child)
        
        population = new_population
        
        # Print the best deck and its fitness (total wasted mana) for the current generation
        best_deck = population[0]
        best_fitness = calculate_total_wasted_mana(best_deck, max_turn)
        print(f"Generation {generation + 1}: Best Deck = {best_deck}, Wasted Mana = {best_fitness}")
    
    return population[0]  # Return the best deck found

# Run the genetic algorithm to find the best deck with minimal mana wastage over 12 turns
best_deck = genetic_algorithm()
best_deck.sort()
print("Best deck found:", best_deck)
print("Wasted Mana:", calculate_total_wasted_mana(best_deck, 12))
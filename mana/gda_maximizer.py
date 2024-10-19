import itertools
import pygad

# Modified fitness function to accept the required 3 parameters
def fitness_function(ga_instance, solution, solution_idx):
    max_turn = 12
    starting_mana = 3
    total_mana = 0
    
    # Iterate through turns
    for i in range(starting_mana, max_turn + 1):
        possible_hands = list(itertools.combinations(solution, 5))
        total_wasted_mana = 0
        
        # Loop through each possible hand
        for hand in possible_hands:
            subsets = list(itertools.chain.from_iterable(itertools.combinations(hand, r) for r in range(1, len(hand) + 1)))
            max_mana_used = 0
            # Find the best subset of cards for maximizing mana used
            for subset in subsets:
                mana_sum = sum(subset)
                if mana_sum <= i and mana_sum > max_mana_used:
                    max_mana_used = mana_sum
            
            wasted_mana = i - max_mana_used
            total_wasted_mana += wasted_mana
        total_mana += total_wasted_mana
    
    # Return the negative of the total wasted mana (since PyGAD maximizes the fitness function)
    return -total_mana

# Set up the genetic algorithm with integer genes only
ga = pygad.GA(
    num_generations=50,               # Number of generations
    num_parents_mating=50,             # Number of parents for mating
    fitness_func=fitness_function,     # Fitness function defined above
    sol_per_pop=100,                   # Number of solutions per population
    num_genes=12,                      # Each deck has 12 cards
    gene_type=int,                     # Ensure genes are integers
    gene_space=range(1, 10),           # Mana values range from 1 to 9 (integers)
    mutation_percent_genes=10,         # Mutation rate (can be tuned)
    allow_duplicate_genes=True,         # Allows duplicate values in the deck (same mana values in different cards)

    parent_selection_type = "sss",
    keep_parents = 1,

    crossover_type = "single_point",

    mutation_type = "random",
)

# Run the genetic algorithm
ga.run()

# Retrieve the best solution and its corresponding fitness value
solution, solution_fitness, solution_idx = ga.best_solution()
solution.sort()
print(f"Best Deck: {solution}")
print(f"Lowest Wasted Mana: {-solution_fitness}")

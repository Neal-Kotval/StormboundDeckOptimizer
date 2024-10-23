import pygad
from ManaSimulation import ManaSimulation

# Modified fitness function to accept the required 3 parameters
def fitness_function(ga_instance, solution, solution_idx):
    generation = ga_instance.generations_completed
    print(f"Generation {generation+1}, Solution {solution_idx+1}: ", end="")
    deck = ManaSimulation(solution, max_turn=12, debug=True)
    return -deck.calculate_avg_wasted_mana()*1000  # Multiplying by 1000 for scaling

# Set up the genetic algorithm
ga = pygad.GA(
    num_generations=50,              # Number of generations
    num_parents_mating=2,           # Number of parents for mating
    fitness_func=fitness_function,    # Fitness function defined above
    sol_per_pop=10,                  # Increased number of solutions per population
    num_genes=12,                     # Each deck has 12 cards
    gene_type=int,                    # Ensure genes are integers
    gene_space=range(1, 10),          # Mana values range from 1 to 9 (integers)
    mutation_percent_genes=1,         # Lower mutation rate to preserve good solutions
    allow_duplicate_genes=True,       # Allows duplicate values in the deck (same mana values in different cards)

    # Genetic algorithm configurations
    parent_selection_type="tournament",  # Tournament selection
    crossover_type="two_points",         # Two-point crossover for more diversity
    keep_elitism=5,                      # Preserve top 5 solutions each generation
    # stop_criteria=["saturate_50"],       # Stop if no improvement for 50 generations
)

# Run the genetic algorithm
ga.run()

# Retrieve the best solution and its corresponding fitness value
solution, solution_fitness, solution_idx = ga.best_solution()
solution.sort()
print(f"Best Deck: {solution}")
print(f"Lowest Wasted Mana: {-solution_fitness}")

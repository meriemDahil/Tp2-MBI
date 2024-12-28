import random
import time
import matplotlib.pyplot as plt

# Fonction de calcul de fitness
def fitness_function(x):
    return -x**2 + 4*x

# Convertir un chromosome binaire en entier
def binary_to_decimal(binary):
    return int("".join(map(str, binary)), 2)

# Générer une population initiale
def initialize_population(pop_size, chromosome_length):
    return [random.choices([0, 1], k=chromosome_length) for _ in range(pop_size)]

# Sélection par roulette
def roulette_selection(population, fitness_values):
    total_fitness = sum(fitness_values)
    probabilities = [f / total_fitness for f in fitness_values]
    selected = random.choices(population, weights=probabilities, k=2)
    return selected

# Croisement uniforme
def uniform_crossover(parent1, parent2, crossover_prob):
    if random.random() < crossover_prob:
        child1, child2 = [], []
        for i in range(len(parent1)):
            if random.random() < 0.5:
                child1.append(parent1[i])
                child2.append(parent2[i])
            else:
                child1.append(parent2[i])
                child2.append(parent1[i])
        return child1, child2
    return parent1, parent2

# Mutation
def mutation(chromosome, mutation_prob):
    return [gene if random.random() > mutation_prob else 1 - gene for gene in chromosome]

# Algorithme génétique
def genetic_algorithm(scenario):
    # Paramètres du scénario
    pop_size = 4
    chromosome_length = 5
    crossover_prob = scenario['Pc']
    mutation_prob = scenario['Pm']
    max_generation = scenario['max_gen']

    # Initialisation
    population = initialize_population(pop_size, chromosome_length)
    execution_time_start = time.time()

    fitness_per_iteration = []
    crossover_count = 0
    mutation_count = 0

    for generation in range(max_generation):
        # Calculer la fitness pour chaque individu
        fitness_values = [fitness_function(binary_to_decimal(ind)) for ind in population]
        fitness_per_iteration.append(fitness_values)

        # Sélection et reproduction
        new_population = []
        while len(new_population) < pop_size:
            parent1, parent2 = roulette_selection(population, fitness_values)
            child1, child2 = uniform_crossover(parent1, parent2, crossover_prob)
            if child1 != parent1 or child2 != parent2:
                crossover_count += 1

            child1 = mutation(child1, mutation_prob)
            child2 = mutation(child2, mutation_prob)
            mutation_count += sum(1 for i in range(chromosome_length) if child1[i] != parent1[i])
            mutation_count += sum(1 for i in range(chromosome_length) if child2[i] != parent2[i])

            new_population.extend([child1, child2])

        population = new_population[:pop_size]

    # Statistiques finales
    execution_time_end = time.time()
    final_fitness = [fitness_function(binary_to_decimal(ind)) for ind in population]
    best_fitness = max(final_fitness)
    avg_fitness = sum(final_fitness) / len(final_fitness)

    return {
        'execution_time': execution_time_end - execution_time_start,
        'fitness_per_iteration': fitness_per_iteration,
        'average_fitness': avg_fitness,
        'max_fitness': best_fitness,
        'crossover_count': crossover_count,
        'mutation_count': mutation_count
    }


# Scénarios
scenarios = [
    {'Pc': 0.75, 'Pm': 0.005, 'max_gen': 30},
    {'Pc': 0.75, 'Pm': 0.005, 'max_gen': 50},
    {'Pc': 0.90, 'Pm': 0.01, 'max_gen': 30},
    {'Pc': 0.90, 'Pm': 0.01, 'max_gen': 50}
]

# Exécution des scénarios
results = []
for i, scenario in enumerate(scenarios):
    print(f"Exécution du scénario {i+1}...")
    result = genetic_algorithm(scenario)
    results.append(result)
    print(f"Scénario {i+1} terminé. Résultats : {result}\n")



# Plot graphs

color = ['lightblue', 'blue', 'purple', 'red', 'black']
for metric in ['average_fitness', 'max_fitness', 'execution_time', 'crossover_count', 'mutation_count']:
    plt.figure()
    plt.title(f"Comparaison des scénarios - {metric}")
    plt.bar([f"Scénario {i+1}" for i in range(len(scenarios))], [res[metric] for res in results],color=color)
    plt.ylabel(metric)
    plt.show()



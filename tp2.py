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
def initialize_population():
    # Population initiale définie dans l'exercice
    initial_population = [
        [1, 0, 0, 1, 0],  # 18
        [0, 0, 1, 1, 0],  # 6
        [0, 1, 0, 1, 1],  # 11
        [1, 1, 0, 1, 1]   # 27
    ]
    return initial_population

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

def plot_roulette_wheel(population, fitness_values, generation, scenario_id):
    min_fitness = min(fitness_values)
    if min_fitness < 0:
        fitness_values = [f - min_fitness + 1 for f in fitness_values]

    total_fitness = sum(fitness_values)
    if total_fitness > 0:
        probabilities = [f / total_fitness for f in fitness_values]
    else:
        probabilities = [1 / len(fitness_values) for _ in fitness_values]
    
    labels = [f"Ind {i}\n({fitness_function(binary_to_decimal(population[i])):.2f})" for i in range(len(population))]
    colors = plt.cm.tab10.colors[:len(population)]
    
    plt.figure(figsize=(6, 6))
    plt.pie(probabilities, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    plt.title(f"Scenario {scenario_id} - Generation {generation}")
    plt.show()

def genetic_algorithm(scenario, scenario_id):
    # Paramètres du scénario
    chromosome_length = 5
    crossover_prob = scenario['Pc']
    mutation_prob = scenario['Pm']
    max_generation = scenario['max_gen']

    # Initialisation avec la population donnée
    population = initialize_population()
    execution_time_start = time.time()

    fitness_per_iteration = []
    crossover_count = 0
    mutation_count = 0

    for generation in range(max_generation):
        # Calcul de la fitness pour chaque individu
        fitness_values = [fitness_function(binary_to_decimal(ind)) for ind in population]
        fitness_per_iteration.append(fitness_values)

        # Visualisation de la roulette
        if generation % 29 == 0:  
            plot_roulette_wheel(population, fitness_values, generation, scenario_id)

        # Sélection et reproduction
        new_population = []
        while len(new_population) < len(population):
            parent1, parent2 = roulette_selection(population, fitness_values)
            child1, child2 = uniform_crossover(parent1, parent2, crossover_prob)
            if child1 != parent1 or child2 != parent2:
                crossover_count += 1

            child1 = mutation(child1, mutation_prob)
            child2 = mutation(child2, mutation_prob)
            mutation_count += sum(1 for i in range(chromosome_length) if child1[i] != parent1[i])
            mutation_count += sum(1 for i in range(chromosome_length) if child2[i] != parent2[i])

            new_population.extend([child1, child2])

        population = new_population[:len(population)]

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
    result = genetic_algorithm(scenario,scenario_id=i + 1)
    
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



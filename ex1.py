import random
import numpy as np


# this is just to ensure repeatable results when running this code
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
# create individual


def individual_creator(n_bits):
    return [random.randint(0, 1) for _ in range(n_bits)]

# create population


def population_creator(n_bits, n_pop):
    return [individual_creator(n_bits) for _ in range(n_pop)]

# fitness function


def onemax(x):
    return sum(x)

# tournament selection


def selection(population, k=3):
    # obtain scores of individuals
    scores = [onemax(ind) for ind in population]
    # first random selection
    selection_idx = random.randint(0, len(population)-1)
    for idx in random.sample(range(len(population)-1), k-1):
        # perform tournament of 3
        if scores[idx] > scores[selection_idx]:
            selection_idx = idx
    return population[selection_idx]

# crossover two parents to create two children


def crossover(parent1, parent2, p_crossover):
    child1, child2 = parent1.copy(), parent2.copy()
    if random.random() < p_crossover:
        # select crossover point that is not on the end of the string
        point = random.randint(1, len(parent1)-1)
        # perform crossover
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
    return [child1, child2]

# mutation operator


def mutation(bitstring, p_mutation):
    for i in range(len(bitstring)):
        if random.random() < p_mutation:
            # flip the bit
            bitstring[i] = 1-bitstring[i]

# genetic algorithm


def genetic_algorithm(fitness_func, n_bits, n_pop, n_gen, p_cross, p_mut, t_size):
    population = population_creator(n_bits, n_pop)
    # initialize the best individual and its score
    best_ind, best_score = 0, fitness_func(population[0])
    # enumerate generations
    for generation in range(n_gen):
        # evaluate all individuals in the population
        scores = [fitness_func(ind) for ind in population]
        # check for new best solution
        for i in range(n_pop):
            if scores[i] > best_score:
                best_ind, best_score = population[i], scores[i]
                print(
                    f'>{generation}, new best {population[i]}, with score of {scores[i]} \n')

        # select parents -- same number of individuals in all generation
        selected = [selection(population, t_size) for _ in range(n_pop)]
        # create next generation
        children = list()
        for i in range(0, n_pop, 2):
            # get selected parents in pairs
            parent1, parent2 = selected[i], selected[i+1]
            # crossover and mutation
            for child in crossover(parent1, parent2, p_cross):
                # mutation
                mutation(child, p_mut)
                # store the next generation
                children.append(child)

        # replace population
        population = children
    return [best_ind, best_score]


# problem constants:
ONE_MAX_LENGTH = 100    # length of bit string to be optimized

# Genetic Algorithm constants:
POPULATION_SIZE = 200    # number of individuals in population
P_CROSSOVER = 0.9        # probability of crossover
# probability of flipping a bit in an individual
indpb = 1.0/float(ONE_MAX_LENGTH)
MAX_GENERATIONS = 80     # max num of generations for stopping condition

# set the parameters
best_ind, best_score = genetic_algorithm(
    onemax,
    ONE_MAX_LENGTH,
    POPULATION_SIZE,
    MAX_GENERATIONS,
    P_CROSSOVER,
    indpb,
    t_size=3
)
print('Done!')
print(f'best individual: {best_ind}, score = {best_score}')




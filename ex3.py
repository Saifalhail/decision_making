import random
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms
import numpy as np

# problem constants:
ONE_MAX_LENGTH = 100    # length of bit string to be optimized

# Genetic Algorithm constants:
POPULATION_SIZE = 200    # number of individuals in population
P_CROSSOVER = 0.9        # probability of crossover
P_MUTATION = 0.1         # probability of an individual selected for mutation
MAX_GENERATIONS = 80     # max num of generations for stopping condition


# create a maximizing fitness - maximize a single objective fitness
creator.create(
    'FitnessMax',
    base.Fitness,
    weights=(1.0,)
)
# create an Individual class that inherits properties of list
# has a fitness attribute of type FitnessMax
creator.create(
    'Individual',
    list,
    fitness=creator.FitnessMax
)

# to create zeroOrOne operator
toolbox = base.Toolbox()
toolbox.register(
    'zeroOrOne',
    random.randint,
    0, 1
)

# type in your answer :^)
# to register the individualCreator
toolbox.register(
    'individualCreator',
    tools.initRepeat,
    creator.Individual,
    toolbox.zeroOrOne,
    ONE_MAX_LENGTH
    # container (1st argument for initRepeat)
    # function to run (2nd argument for initRepeat)
    # number of times (3rd argument for initRepeat)
)

# to register the populationCreator
toolbox.register(
    'populationCreator',
    tools.initRepeat,
    list,
    toolbox.individualCreator,

    # container (1st argument for initRepeat)
    # function to run (2nd argument for initRepeat)
)
# number of times (3rd argument for initRepeat) is not given
# hence user input is expected for population size


def oneMaxFitness(individual):
    # <-- type your answer here, hint: must return a tuple
    return sum(individual),


# define evalute operator as an alias of oneMaxFitness
toolbox.register(
    'evaluate',
    oneMaxFitness)

# type in your answer :^)
toolbox.register('select', tools.selTournament, tournsize=3)
toolbox.register('mate', tools.cxOnePoint)
toolbox.register('mutate', tools.mutFlipBit, indpb=1.0/ONE_MAX_LENGTH)

# creating the initial population
population = toolbox.populationCreator(n=POPULATION_SIZE)

# keep track of generation
generationCounter = 0

# calculate fitness of each individual in the initial population by map()
fitnessValues = list(map(toolbox.evaluate, population))

# assign matching fitness tuple to each individual
for individual, fitnessValue in zip(population, fitnessValues):
    individual.fitness.values = fitnessValue

# single objective fitness, extract the first value of tuple
fitnessValues = [individual.fitness.values[0] for individual in population]

maxFitnessValues = []
meanFitnessValues = []

while max(fitnessValues) < ONE_MAX_LENGTH and generationCounter < MAX_GENERATIONS:
    generationCounter += 1
    offspring = toolbox.select(population, len(population))
    # the selected individuals, residing in a list called offspring
    # they are cloned prior applying the genetic operators
    # so not affecting original population
    # clones of individual from previous generation
    offspring = list(map(toolbox.clone, offspring))

    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < P_CROSSOVER:  # flip coin to decide if crossover happens
            toolbox.mate(child1, child2)
            # fitness value deleted as they have been modified
            # existing one no longer valid
            del child1.fitness.values
            del child2.fitness.values

        # the mate function takes 2 individuals as arguments and modifies them in place
        # don't need to be reassigned

    for mutant in offspring:
        if random.random() < P_MUTATION:
            toolbox.mutate(mutant)
            del mutant.fitness.values

    # individuals that went through crossover and mutation have empty (invalid) firness values
    # need to recalculate

    freshIndividuals = [ind for ind in offspring if not ind.fitness.valid]
    freshFitnessValues = list(map(toolbox.evaluate, freshIndividuals))
    for individual, fitnessValue in zip(freshIndividuals, freshFitnessValues):
        individual.fitness.values = fitnessValue

    # replace old population with new one
    population[:] = offspring

    # before continue, current fitness values are collected for statistics
    # fitness value is a single element tuple
    fitnessValues = [ind.fitness.values[0] for ind in population]

    # calculate and append the max and mean fitness value for statistics
    maxFitness = max(fitnessValues)
    meanFitness = sum(fitnessValues) / len(population)
    maxFitnessValues.append(maxFitness)
    meanFitnessValues.append(meanFitness)
    print(
        f"- Generation {generationCounter}: Max Fitness = {maxFitness}, Avg Fitness = {meanFitness}")

    best_index = fitnessValues.index(max(fitnessValues))
    print("Best Individual = ", *population[best_index], "\n")

# plot out the graph after stopping condition met
plt.plot(maxFitnessValues, color='red', label='max')
plt.plot(meanFitnessValues, color='green', label='mean')
plt.xlabel('Generation')
plt.ylabel('Max / Average Fitness')
plt.title('Max and average fitness over generations')
plt.legend()
plt.show()


# population = toolbox.populationCreator(n=POPULATION_SIZE)

# # set the key function to extract the data we interest in for each generation
# # i.e. the fitness value(s)
# stats = tools.Statistics(lambda ind: ind.fitness.values)

# # then register various functions to apply to these values
# stats.register('max', np.max)
# stats.register('avg', np.mean)

# # the collected statistics will be returned in an object called the logbook
# # simply call the algorithms.eaSimple
# population, logbook = algorithms.eaSimple(
#     population,
#     toolbox,
#     cxpb=P_CROSSOVER,
#     mutpb=P_MUTATION,
#     ngen=MAX_GENERATIONS,    # stopping condition
#     stats=stats,
#     verbose=True
# )

# # GA is done - extract statistics:
# maxFitnessValues, meanFitnessValues = logbook.select('max', 'avg')

# # plot out the graph after stopping condition met
# plt.plot(maxFitnessValues, color='red', label='max')
# plt.plot(meanFitnessValues, color='green', label='mean')
# plt.xlabel('Generation')
# plt.ylabel('Max / Average Fitness')
# plt.title('Max and average fitness over generations')
# plt.legend()
# plt.show()

import random
from deap import creator, base, tools

creator.create(
    'FitnessMax',
    base.Fitness,     # extending the base.Fitness class (inherit from this)
    weights=(1.0,)    # class attribute initialized to value of (1.0,), a tuple
)

creator.create(
    'FitnessMin',
    base.Fitness,     # extending the base.Fitness class
    weights=(-1.0,)   # negative 1 for minimization
)
creator.create(
    'FitnessCompund',
    base.Fitness,     # extending the base.Fitness class
    weights=(1.0, 0.2, -0.5)   # negative 1 for minimization
)
creator.create(
    'Individual',    # name
    list,            # inherit and extends the Python list class, the chromosome used is of list type
    fitness=creator.FitnessMax    # fitness attribute previously created
)


def sum_two(a, b):
    return a+b


toolbox = base.Toolbox()
toolbox.register('increment_five', sum_two, b=5)

print(toolbox.increment_five(10))


# toolbox.select operator that performs tournament selection, size of 3
toolbox.register('select', tools.selTournament, tournsize=3)

# toolbox.mate operator that performs two-point crossover
toolbox.register('mate', tools.cxTwoPoint)

# toolbox.mutate operator that performs flip bit mutation, with probability of 0.02 for each attribute to be flipped
toolbox.register('mutate', tools.mutFlipBit, indpb=0.02)


randomList = tools.initRepeat(
    list,           # container
    random.random,  # function
    30              # number of times
)
print(randomList)

toolbox.register('zeroOrOne', random.randint, 0, 1)
randomList_one_zero = tools.initRepeat(list, toolbox.zeroOrOne, 30)
print(randomList_one_zero)


def someFitnessCalculationFunction(individual):
    return _some_calculation_of_the_fitness


toolbox.register('evaluate', someFitnessCalculationFunction)

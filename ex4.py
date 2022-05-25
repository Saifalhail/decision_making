import operator
import math
import random

import numpy
import matplotlib.pyplot as plt

from deap import algorithms, base, creator, tools, gp


def protectedDiv(left, right):
    # try:
    #     ____ans_here____
    # except ZeroDivisionError:
    #     ____ans_here____
    pass  # comment this out after you have key in your answer

# the primitives and terminals that will populate the trees are regrouped in a primitive set
# the following primitive set instantiation with basic operators
# arity means the number of entries it takes (number of arguments)


pset = gp.PrimitiveSet("MAIN", 1)
pset.addPrimitive(operator.add, 2)
# ______add_operator_subtraction______
# ______add_operator_multiplication______
pset.addPrimitive(protectedDiv, 2)
pset.addPrimitive(operator.neg, 1)    # negation
pset.addPrimitive(math.cos, 1)        # cosine
# ______add_math_operator_sine()______
pset.addEphemeralConstant("rand101", lambda: random.randint(-1, 1))

pset.renameArguments(ARG0='x')    # one dimension regression problem

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# three ways to generate trees: full, grow, half-and-half
# full: generate an expression where each leaf has the same depth between min and max
# grow: generate an expression where each leaf might have a different depth between min and max
# half-and-half: half of each style
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate,
                 creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# to transform the individual into its executable form – that is, a program
toolbox.register("compile", gp.compile, pset=pset)


def evalSymbReg(individual, points):
    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)
    # Evaluate the mean squared error between the expression
    # and the real function : x**4 + x**3 + x**2 + x
    sqerrors = ((func(x) - x**4 - x**3 - x**2 - x)**2 for x in points)
    return math.fsum(sqerrors) / len(points),


toolbox.register("evaluate", evalSymbReg, points=[
                 x/10. for x in range(-10, 10)])
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(
    key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(
    key=operator.attrgetter("height"), max_value=17))

stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
stats_size = tools.Statistics(len)
mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
mstats.register("avg", numpy.mean)
mstats.register("std", numpy.std)
# _____register_stats_for_min_value_____
# _____register_stats_for_max_value_____

pop = toolbox.population(n=300)
hof = tools.HallOfFame(1)
pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, 50, stats=mstats,
                               halloffame=hof, verbose=True)
print("Best Ever Individual = ", hof.items[0])
best_indv = hof.items[0]

gen = log.select('gen')
ft = log.chapters['fitness'].select('min')

plt.plot(gen, ft, "b-")
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.legend()
plt.show()

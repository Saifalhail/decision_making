from deap import base, creator
import random
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from deap import tools
from deap import algorithms
import datetime
import json
# penalty factors - if capability is incorrect/ if effectiveness is incorrect/ if number of units doesn't match the
# requirements
SOFT_CONSTRAINT_PENALTY = 0.5
HARD_CONSTRAINT_PENALTY = 10

erStationA = {'fireEngineA': 5, 'fireEngineB': 2, 'fireFastResponse': 5,
              'ambulance': 2, 'medicalFastResponse': 2, 'policePatrolCar': 3, 'trafficPoliceBike': 2}
erStationB = {'fireEngineA': 2, 'fireEngineB': 1, 'fireFastResponse': 3,
              'ambulance': 2, 'medicalFastResponse': 2, 'policePatrolCar': 3, 'trafficPoliceBike': 2}

capabilities = ['oil', 'chemical', 'electrical', 'injury',
                 'robbery', 'breakin', 'traffic accident', 'traffic control']
effects = ['supress', 'control', 'evacuate', 'investigate', 'arrest']

sizes = ['small', 'medium', 'large', 'light', 'serious', 'simple']


class Assets:
    def __init__(self, asset, speed, capability, prep_time, effectiveness):
        self.asset = asset
        self.speed = speed
        self.capability = capability
        self.prep_time = prep_time
        self.effectiveness = effectiveness


fireEngineA = Assets(asset='fireEngineA', speed=80, capability=['oil', 'chemical', 'electrical'],
                     prep_time=5, effectiveness=['supress','control'])
fireEngineB = Assets(asset='fireEngineB', speed=90, capability=['chemical', 'electrical'],
                     prep_time=3, effectiveness=['supress','control'])
fireFastResponse = Assets(asset='fireFastResponse', speed=100, capability=['electrical'],
                          prep_time=2, effectiveness=['control'])
ambulance = Assets(asset='ambulance', speed=80, capability=['injury'],
                   prep_time=5, effectiveness=['control', 'evacuate'])
medicalFastResponse = Assets(asset='medicalFastResponse', speed=100, capability=['injury'],
                             prep_time=2, effectiveness=['investigate', 'arrest', 'control'])
policePatrolCar = Assets(asset='policePatrolCar', speed=100,
                         capability=['robbery', 'breakin', 'traffic accident', 'traffic control'],
                         prep_time=3, effectiveness=['investigate', 'arrest', 'control'])
trafficPoliceBike = Assets(asset='trafficPoliceBike', speed=120,
                           capability=['traffic accident', 'traffic control'],
                           prep_time=2, effectiveness=['investigate', 'control'])


# function to convert the individual to a dictionary having different units for both the stations
def getallocation(stations, listofavailableunits , individual):
    allocation = {}
    last_index = 0
    for unit in listofavailableunits:
        allocation[unit.asset] = {}
        for i,station in enumerate(stations):
            #Going through each vehicle in each station and giving it a random deployment [0,0] or [1,1]
             allocation[unit.asset][i] = individual[last_index : (last_index + station[unit.asset])]
             last_index = (last_index + station[unit.asset])
    return allocation


class Situation:
    def __init__(self, distFromA, distFromB, situation, solution, numUnits, timeTaken): #Can add timetaken
        self.dist = {'a': distFromA, 'b': distFromB}
        self.situation = situation
        self.solution = solution
        self.numUnits = numUnits
        self.timeTaken = timeTaken

    def print(self, number, sType):
        print('\nSituation ' + str(number) + ': ' + sType)
        print(self.dist)
        print(self.situation)
        print(self.solution)

# calculate the cost for any individual
# individual is a list of binary values indicating whether the asset is assigned or not
def getCost(situationlist, situationqueue, individual):
    cost = 0
    # convert the individual list to a dictionary
    
    alloc = getallocation(stations, listofavailableunits, individual) #Takes in All units and all stations and randomized individual list
    """
    Run getallocation to provide a deployment list from the station EG:
    {'fireEngineA': {0: [0, 0, 1, 1, 0], 1: [1, 1]}, 'fireEngineB': {0: [1, 1], 1: [0]}, 
    'fireFastResponse': {0: [1, 1, 1, 1, 0], 1: [1, 1, 1]}, 'ambulance': {0: [0, 0], 1: [0, 1]}, 
    'medicalFastResponse': {0: [1, 0], 1: [0, 1]}, 'policePatrolCar': {0: [0, 1, 0], 1: [1, 1, 0]},
     'trafficPoliceBike': {0: [1, 1], 1: [1, 1]}}
     Each Vehicle contains a random deployment scenario and can only use the vehicles available within the station
    """
    # total units which have been assigned to address the sitation
    total_units = 0
    # total requirement for different situations
    total_req = 0
    allVehiclesTime = []
    for k in alloc.keys(): # Loop through the vehicles dict
        total_units += sum(alloc[k][0]) + sum(alloc[k][1]) #Update total units to be deployed

    # for all the situations in the queue
    for key in situationqueue.keys():
        # elements in small/ medium/ large sizes
        for elem in situationqueue[key]:
            # retrieve the element from situation list
            elem = situationList[elem]

            # penalty is calculated such the if capability is addressed along with effectiveness and time penalty is 0
            num_capable_units = 0 # How many units in total
            num_effective_units = 0 # How many units that cover the solution
            num_ontime_units = 0 # Units that would reach on time
            num_timing = 0 # Units compared to each other based on their time
            
            total_req += elem.numUnits
            # for all the assets in the list
            for unit in listofavailableunits:
                allVehiclesTime.append(unit.prep_time)
                # if situation is there in the asset capability
                if elem.situation in unit.capability: # Checks if vehicle fits the scenario required
                    # check the number of such assets assigned in the allocation by the individual
                    num_capable_units += sum(alloc[unit.asset][0]) + sum(alloc[unit.asset][1]) # Count how many units assigned
                    # if effectiveness is also addressed
                    if elem.solution in unit.effectiveness:
                        num_effective_units += sum(alloc[unit.asset][0]) + sum(alloc[unit.asset][1])
                        # if the asset would be able to reach in time
                        if int(HARD_CONSTRAINT_PENALTY * int(unit.speed/ 60 *
                            (elem.timeTaken - unit.prep_time) * sum(alloc[unit.asset][0]) > elem.dist['a'])):
                            num_ontime_units += sum(alloc[unit.asset][0])
                            
                        elif int(HARD_CONSTRAINT_PENALTY * int(unit.speed/ 60 *
                            (elem.timeTaken - unit.prep_time) * sum(alloc[unit.asset][1]) > elem.dist['b'])):
                            num_ontime_units += sum(alloc[unit.asset][1])

                        for vehicleTime in allVehiclesTime:
                            if elem.timeTaken < vehicleTime:
                                num_timing += sum(alloc[unit.asset][0])
            # calculate the cost basis the numbers calculated above
            """
            Constrains violations: 
            num_capable_units is how many violations for the situation, EG: Oil or electrical
            num_effective_units is how many violations for the solutions, EG: Supress, Control
            num_ontime_units is how many violations for the time, EG: which vehicle is faster with prep time
            """
            # units available - units with solution + units that meet time criteria - units with solution + units required - units available
            cost += HARD_CONSTRAINT_PENALTY * abs(num_capable_units - num_effective_units) + \
                    HARD_CONSTRAINT_PENALTY * abs(num_ontime_units - num_effective_units) + \
                    HARD_CONSTRAINT_PENALTY * abs(elem.numUnits - num_capable_units) + \
                    SOFT_CONSTRAINT_PENALTY * abs(num_timing)
# WRONG_NUM_UNITS * abs(num_ontime_units - num_effective_units) + \
    # difference in total number of assets required and assigned is added
    cost += abs(total_units - total_req) * HARD_CONSTRAINT_PENALTY
    return cost

def eaSimpleWithElitism(
    population,
    toolbox,
    cxpb,
    mutpb,
    ngen,
    stats=None,
    halloffame=None,
    verbose=__debug__,
):
    """This algorithm is similar to DEAP eaSimple() algorithm, with the modification that
    halloffame is used to implement an elitism mechanism. The individuals contained in the
    halloffame are directly injected into the next generation and are not subject to the
    genetic operators of selection, crossover and mutation.
    """
    logbook = tools.Logbook()
    logbook.header = ["gen", "nevals"] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if halloffame is None:
        raise ValueError("halloffame parameter must not be empty!")

    halloffame.update(population)
    hof_size = len(halloffame.items) if halloffame.items else 0

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print(logbook.stream)

    # Begin the generational process
    for gen in range(1, ngen + 1):

        # Select the next generation individuals
        offspring = toolbox.select(population, len(population) - hof_size)

        # Vary the pool of individuals
        offspring = algorithms.varAnd(offspring, toolbox, cxpb, mutpb)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # add the best back to population:
        offspring.extend(halloffame.items)

        # Update the hall of fame with the generated individuals
        halloffame.update(offspring)

        # Replace the current population by the offspring
        population[:] = offspring

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print(logbook.stream)

    return population, logbook


def main():
    """
    Multiple Inputs
    """
    n = int(input('How many situations are there:'))

    situationList = []
    situationPriorityQueue = {
        'small': [],
        'medium': [],
        'large': [],
        'light': [],
        'serious': [],
        'simple': []
    }

    for i in range(n):
        while True:
            dist_a = int(input('What is the distance from station A:'))
            dist_b = int(input('What is the distance from station B:'))
            situation = input('What is the Situation?\n')
            solution = input('What solution is needed?\n')
            sType = input('What is the size of situation? small, medium, large, simple, light or serious?\n')
            timeTaken = int(input('What is the maximum time which can be taken:'))

            situations = {'small': 1, 'medium': 2, 'large': 3, 'light': 1, 'serious': 2, 'simple': 1}
            numUnits = situations[sType.lower()]

            # Validity Checks - if input is in stored list
            if situation not in capabilities:
                print('Invalid situation, try again\n')
                continue
            if solution not in effects:
                print('Invalid solution, try again\n')
                continue
            if sType not in sizes:
                print('Invalid size, try again\n')
                continue
            newSituation = Situation(dist_a, dist_b, situation, solution, numUnits, timeTaken) #Can add timetaken
            situationList.append(newSituation)
            newSituation.print(i, sType)
            situationPriorityQueue[sType].append(i)
            break
    return situationList, situationPriorityQueue

if __name__ == '__main__':
    situationList, situationPriorityQueue = main()


    listofavailableunits = [fireEngineA, fireEngineB, fireFastResponse, ambulance, medicalFastResponse, policePatrolCar,
                            trafficPoliceBike]
    individual_length = 0

    stations = [erStationA, erStationB]

    for  unit in listofavailableunits: # Go through the list of available units
        for station in stations: # Go through the list of stations
            if unit.asset in station: # Check whether the unit required is within the station or not
                individual_length += station[unit.asset] # Records all vehicles within each station (total)

    individual = [0] * individual_length # Starts Base with all 0's

    RANDOM_SEED = 33 # Choose randomness factor
    random.seed(RANDOM_SEED)

    # define a single objective, maximizing fitness strategy:
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

    # create the Individual class based on list:
    creator.create("Individual", list, fitness=creator.FitnessMin)

    #Base toolbox created and saved
    toolbox = base.Toolbox()

    nsp_length = individual_length

    # create an operator that randomly returns 0 or 1:
    toolbox.register("zeroOrOne", random.randint, 0, 1)
    # create the individual operator to fill up an Individual instance:
    toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.zeroOrOne, nsp_length)
    # create the population operator to generate a list of individuals:
    toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)

    # fitness calculation
    def fitness_func(individual):
        return getCost(situationList , situationPriorityQueue, individual),  # return a tuple

    toolbox.register("evaluate", fitness_func)

    # genetic operators:
    toolbox.register("select", tools.selTournament, tournsize=2)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=1.0/nsp_length)

    # Genetic Algorithm constants:
    POPULATION_SIZE = 300
    P_CROSSOVER = 0.9  # probability for crossover
    P_MUTATION = 0.1   # probability for mutating an individual
    MAX_GENERATIONS = 200
    HALL_OF_FAME_SIZE = 30

    population = toolbox.populationCreator(n=POPULATION_SIZE) # Creates population

    # prepare the statistics object:
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min)
    stats.register("avg", np.mean)

    # define the hall-of-fame object:
    hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

    population, logbook = eaSimpleWithElitism(population, toolbox, cxpb=P_CROSSOVER, mutpb=P_MUTATION,
                                                  ngen=MAX_GENERATIONS, stats=stats, halloffame=hof, verbose=True)

    # print best solution found:
    best = hof.items[0]
    print(len(best))
    print("-- Best Individual = ", best)
    print("-- Best Fitness = ", best.fitness.values[0])
    print()
    print("-- Schedule = ")
    print(getallocation(stations, listofavailableunits, best))

    # extract statistics:
    minFitnessValues, meanFitnessValues = logbook.select("min", "avg")
    # with open('results.txt', 'a') as outfile:
    #     json.dump(best, outfile)
    #     outfile.write('\n')
    #     json.dump(best.fitness.values[0], outfile)
    #     outfile.write('\n')
    #     json.dump(getallocation(stations, listofavailableunits, best), outfile)
    #     outfile.write('\n')
    # plot statistics:
    sns.set_style("whitegrid")
    plt.plot(minFitnessValues, color='red', label='min')
    plt.plot(meanFitnessValues, color='green', label='mean')
    plt.xlabel('Generation')
    plt.ylabel('Min / Average Fitness')
    plt.title('Min and Average fitness over Generations')
    plt.legend()
    plt.show()
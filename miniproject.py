import datetime
from random import randint
from random import seed
from deap import base, creator, tools, algorithms
import random
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


erStationA = {'fireEngineA': 5, 'fireEngineB': 2, 'fireFastResponse': 5,
              'ambulance': 2, 'medicalFastResponse': 2, 'policePatrolCar': 3, 'trafficPoliceBike': 2}
erStationB = {'fireEngineA': 2, 'fireEngineB': 1, 'fireFastResponse': 3,
              'ambulance': 2, 'medicalFastResponse': 2, 'policePatrolCar': 3, 'trafficPoliceBike': 2}

capabilities = ['oil', 'chemical', 'electrical', 'injury-serious',
                'injury-light', 'robbery', 'breakin', 'traffic accident', 'traffic control']
effects = ['supress', 'control', 'evacuate', 'investigate', 'arrest']

sizes = ['small', 'medium', 'large']

locationPreference = [
    [0, 1],
    [1, 0]
]



class Assets:
    def __init__(self, asset, speed, quantity, capability, prep_time, effectiveness):
        self.asset = asset
        self.speed = speed
        self.quantity = quantity
        self.capability = capability
        self.prep_time = prep_time
        self.effectiveness = effectiveness

    def deployFromStationA(self, situation, solution):
        if erStationA[self.asset] > 0:
            if situation in self.capability and solution in self.effectiveness:
                erStationA[self.asset] = erStationA[self.asset] - 1
                print("Proper Vehicle to Deploy: ", self.asset)
                print("From: Station A")
                return True
        return False

    def deployFromStationB(self, situation, solution):
        if erStationB[self.asset] > 0:
            if situation in self.capability and solution in self.effectiveness:
                erStationB[self.asset] = erStationB[self.asset] - 1
                print("Proper Vehicle to Deploy: ", self.asset)
                print("From: Station B")
                return True
        return False

    def checker(self, situation):
        a = situation.dist['a']
        b = situation.dist['b']
        pref = locationPreference[0]
        if b < a:
            pref = locationPreference[1]
        # [1, 0]

        for loc in pref:
            if loc == 0 and self.deployFromStationA(situation.situation, situation.solution):
                print('The unit will reach in ' + str(datetime.timedelta(hours=b/self.speed)))
                return True
            if loc == 1 and self.deployFromStationB(situation.situation, situation.solution):
                print('The unit will reach in ' + str(datetime.timedelta(hours=b/self.speed)))
                return True
        return False


fireEngineA = Assets(asset='fireEngineA', speed=80, quantity=5, capability=['oil', 'chemical', 'electrical'],
                     prep_time=5, effectiveness=['supress'])
fireEngineB = Assets(asset='fireEngineB', speed=90, quantity=2, capability=['chemical', 'electrical'],
                     prep_time=3, effectiveness=['supress'])
fireFastResponse = Assets(asset='fireFastResponse', speed=100, quantity=5, capability=['electrical'],
                          prep_time=2, effectiveness=['control'])
ambulance = Assets(asset='ambulance', speed=80, quantity=2, capability=['injury-serious', 'injury-light'],
                   prep_time=5, effectiveness=['control', 'evacuate'])
medicalFastResponse = Assets(asset='medicalFastResponse', speed=100, quantity=2, capability=['injury-light'],
                             prep_time=2, effectiveness=['investigate', 'arrest', 'control'])
policePatrolCar = Assets(asset='policePatrolCar', speed=100, quantity=3,
                         capability=['robbery', 'breakin', 'traffic accident', 'traffic control'],
                         prep_time=3, effectiveness=['investigate', 'arrest', 'control'])
trafficPoliceBike = Assets(asset='trafficPoliceBike', speed=120, quantity=2,
                           capability=['traffic accident', 'traffic control'],
                           prep_time=2, effectiveness=['investigate', 'control'])

listofavailableunits = [fireEngineA, fireEngineB, fireFastResponse, ambulance, medicalFastResponse, policePatrolCar,
                        trafficPoliceBike]


# for i in listofavailableunits:
#    i.checker(location={'a': 20, 'b': 10}, situation='injury-serious', solution='evacuate')

# user_input = 'ADD'
class Situation:

    def __init__(self, distFromA, distFromB, situation, solution, numUnits):
        self.dist = {'a': distFromA, 'b': distFromB}
        self.situation = situation
        self.solution = solution
        self.numUnits = numUnits

    def print(self, number, sType):
        print('\nSituation ' + str(number) + ': ' + sType)
        print(self.dist)
        print(self.situation)
        print(self.solution)


def deploy(sList, situationList, sType):
    for i in sList:  # list of index of a particular size type (Large, small, medium)
        situationList[i].print(i, sType)
        for _ in range(situationList[i].numUnits):
            foundUnit = False
            for unit in listofavailableunits:
                if unit.checker(situationList[i]):
                    foundUnit = True
                    break
            if not foundUnit:
                print('No more units could be deployed')
                break


def main():
    n = int(input('How many situations are there:'))
    situationList = []
    situationPriorityQueue = {
        'small': [],
        'medium': [],
        'large': []
    }
    for i in range(n):
        while True:
            print('Enter details of the situation ' + str(i))
            dist_a = int(input('What is the distance from station A:'))
            dist_b = int(input('What is the distance from station B:'))
            situation = input('What is the Situation?\n')
            solution = input('What solution is needed?\n')
            sType = input('What is the size of situation? small, medium or large\n')
            numUnits = int(input('How many units are needed to be deployed:'))

            # Validity Checks
            if situation not in capabilities:
                print('Invalid situation, try again\n')
                continue
            if solution not in effects:
                print('Invalid solution, try again\n')
                continue
            if sType not in sizes:
                print('Invalid size, try again\n')
                continue
            newSituation = Situation(dist_a, dist_b, situation, solution, numUnits)
            situationList.append(newSituation)
            newSituation.print(i, sType)
            situationPriorityQueue[sType].append(i)
            break
    deploy(situationPriorityQueue['large'], situationList, 'large')
    deploy(situationPriorityQueue['medium'], situationList, 'medium')
    deploy(situationPriorityQueue['small'], situationList, 'small')


main()


schedule = []
# seed random number generator
seed(1)
# generate some integers
for _ in range(168):
	value = randint(0, 1)
	schedule.append(value)
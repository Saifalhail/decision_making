from random import randint
from random import seed

list_of_nurses = ['A','B','C','D','E','F','G','H']

# nurses' respective shift preferences - morning,evening,night
# assuming it's daily preference
shiftPreferences = [
    [1,0,0],
    [1,1,0],
    [0,0,1],
    [0,1,0],
    [0,1,0],
    [0,1,1],
    [1,1,1],
    [0,1,0]
]
# min and max number of nurses allowed for each shift - morning, evening, night
shiftMin = [2,2,1]
shiftMax = [3,4,2]

# max shifts per week allowed for each nurse
maxShiftsPerWeek = 5

# number of weeks we create a schedule for:
weeks = 1

# useful values
shiftsPerDay = len(shiftMin)
shiftsPerWeek = 7 * shiftsPerDay

def getNurseShift(schedule):
    """
    Converts the entire schedule into a dictionary with a separate schedule for each nurse
    :param schedule: a list of binary values describing the given schedule
    :return: a dictionary with each nurse as a key and the corresponding shifts as the value
    """
    shiftsPerNurse = len(schedule)//len(list_of_nurses)  # for our case here, we have 21 shifts per nurse
    nurseShiftsDict = {}
    shiftIndex = 0
    for nurse in list_of_nurses:
        nurseShiftsDict[nurse] = schedule[shiftIndex: (shiftIndex + shiftsPerNurse)]
        shiftIndex += shiftsPerNurse
    return nurseShiftsDict

def countConsecutiveShiftViolations(nurseShiftsDict):
    """
    Counts the consecutive shift violations in the schedule
    :param nurseShiftsDict: a dictionary with a separate schedule for each nurse
    :return: count of violations found
    """
    violations = 0
    # iterate over the shifts of each nurse:
    for nurseShifts in nurseShiftsDict.values():
        # look for two cosecutive '1's:
        for shift1, shift2 in zip(nurseShifts, nurseShifts[1:]):
            if shift1 == 1 and shift2 == 1:
                violations += 1
    return violations




schedule = []
# seed random number generator
seed(1)
# generate some integers
for _ in range(36):
	value = randint(0, 1)
	schedule.append(value)


# countConsecutiveShiftViolations(getNurseShift(schedule=schedule))

# a = [1,2,3,4]

# for s1, s2 in zip(a, a[1:]):
#     print(s1, s2)

def countShiftsPerWeekViolations(nurseShiftsDict):
    """
    Counts the max-shifts-per-week violations in the schedule
    :param nurseShiftsDict: a dictionary with a separate schedule for each nurse
    :return: count of violations found
    """
    violations = 0
    weeklyShiftsList = []
    # iterate over the shifts of each nurse:
    for nurseShifts in nurseShiftsDict.values():  # all shifts of a single nurse
        # iterate over the shifts of each weeks:
        for i in range(0, weeks*shiftsPerWeek, shiftsPerWeek):
            # shiftsPerWeek is 21 (3 shifts per day*7)
            # count all the '1's over the week:
            weeklyShifts = sum(nurseShifts[i:i + shiftsPerWeek])
            weeklyShiftsList.append(weeklyShifts)
            if weeklyShifts > maxShiftsPerWeek:
                violations += weeklyShifts - maxShiftsPerWeek

    return weeklyShiftsList, violations

# for i in range(0,2*7,7): # <- assuming we have a 2-week schedule
#     print(i, i+7)

def countNursesPerShiftViolations(nurseShiftsDict):
    """
    Counts the number-of-nurses-per-shift violations in the schedule
    :param nurseShiftsDict: a dictionary with a separate schedule for each nurse
    :return: count of violations found
    """
    # sum the shifts over all nurses:
    totalPerShiftList = [sum(shift) for shift in zip(*nurseShiftsDict.values())]

    violations = 0
    # iterate over all shifts and count violations:
    for shiftIndex, numOfNurses in enumerate(totalPerShiftList):
        # (0%3, 1%3, 3%3)
        dailyShiftIndex = shiftIndex % shiftsPerDay  # -> 0, 1, or 2 for the 3 shifts per day
        if (numOfNurses > shiftMax[dailyShiftIndex]):
            violations += numOfNurses - shiftMax[dailyShiftIndex]
        elif (numOfNurses < shiftMin[dailyShiftIndex]):
            violations += shiftMin[dailyShiftIndex] - numOfNurses

    return totalPerShiftList, violations
countNursesPerShiftViolations(getNurseShift(schedule=schedule))
# sample_dict = {
#     'A': [1,0,1,1,0],
#     'B': [1,0,1,0,0],
#     'C': [0,0,0,1,0],
# }
# for i in zip(*sample_dict.values()):
#     print(i)

# [sum(shift) for shift in zip(*sample_dict.values())]

# print(0%3)
# print(1%3)
# print(2%3)
# print(3%3)
# print(4%3)
# print(5%3)
# print(f"Max shift for morning: {shiftMax[0]}")
# print(f"Max shift for evening: {shiftMax[1]}")
# print(f"Max shift for night: {shiftMax[2]}")

# def countShiftPreferenceViolations(nurseShiftsDict):
#     """
#     Counts the nurse-preferences violations in the schedule
#     :param nurseShiftsDict: a dictionary with a separate schedule for each nurse
#     :return: count of violations found
#     """
#     violations = 0
#     for nurseIndex, shiftPref in enumerate(shiftPreferences):
#         # duplicate the shift-preference over the days of the period
#         preference = shiftPref * (shiftsPerWeek // shiftsPerDay)
#         # iterate over the shifts and compare to preferences:
#         shifts = nurseShiftsDict[list_of_nurses[nurseIndex]]
#         for pref, shift in zip(preference, shifts):
#             if pref == 0 and shift == 1: # only when the preference is zero but shift is one, violation counts
#                 violations += 1

#     return violations

# print(shiftPreferences)
# print(f'shifts per week: {shiftsPerWeek}')
# print(f'shifts per day: {shiftsPerDay}')
# print((shiftsPerWeek // shiftsPerDay))

# def printScheduleInfo(schedule):
#     """
#     Prints the schedule and violations details
#     :param schedule: a list of binary values describing the given schedule
#     """
#     nurseShiftsDict = getNurseShift(schedule)

#     print("Schedule for each nurse:")
#     for nurse in nurseShiftsDict:  # all shifts of a single nurse
#         print(nurse, ":", nurseShiftsDict[nurse])

#     print("consecutive shift violations = ", countConsecutiveShiftViolations(nurseShiftsDict))
#     print()

#     weeklyShiftsList, violations = countShiftsPerWeekViolations(nurseShiftsDict)
#     print("weekly Shifts = ", weeklyShiftsList)
#     print("Shifts Per Week Violations = ", violations)
#     print()

#     totalPerShiftList, violations = countNursesPerShiftViolations(nurseShiftsDict)
#     print("Nurses Per Shift = ", totalPerShiftList)
#     print("Nurses Per Shift Violations = ", violations)
#     print()

#     shiftPreferenceViolations = countShiftPreferenceViolations(nurseShiftsDict)
#     print("Shift Preference Violations = ", shiftPreferenceViolations)
#     print()

# def getCost(schedule):
#     """
#     Calculates the total cost of the various violations in the given schedule
#     ...
#     :param schedule: a list of binary values describing the given schedule
#     :return: the calculated cost
#     """

#     # convert entire schedule into a dictionary with a separate schedule for each nurse:
#     nurseShiftsDict = getNurseShift(schedule)

#     # count the various violations:
#     consecutiveShiftViolations = countConsecutiveShiftViolations(nurseShiftsDict)
#     shiftsPerWeekViolations = countShiftsPerWeekViolations(nurseShiftsDict)[1]
#     nursesPerShiftViolations = countNursesPerShiftViolations(nurseShiftsDict)[1]
#     shiftPreferenceViolations = countShiftPreferenceViolations(nurseShiftsDict)

#     # calculate the cost of the violations:
#     hardContstraintViolations = consecutiveShiftViolations + nursesPerShiftViolations + shiftsPerWeekViolations
#     softContstraintViolations = shiftPreferenceViolations

#     return HARD_CONSTRAINT_PENALTY * hardContstraintViolations + softContstraintViolations
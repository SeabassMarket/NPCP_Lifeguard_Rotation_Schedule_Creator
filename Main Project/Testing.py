# import libraries
from CalculateSchedule import CalculateSchedule
from StaticAppInfo import StaticAppInfo
from Time import Time
import time
import tkinter as tk

"""THE FIRST PART OF THIS CODE IS JUST HARDCODING INFORMATION   """
# Create static app info
staticAppInfo = StaticAppInfo(tk.Tk())

# Create all the information for the stands
upStands = {
    "A": [Time(hour=11, minute=0), Time(hour=20, minute=40), 1],
    "B": [Time(hour=11, minute=0), Time(hour=20, minute=40), 1],
    "C": [Time(hour=13, minute=0), Time(hour=17, minute=0), 1],
    "E": [Time(hour=10, minute=0), Time(hour=20, minute=40), 1],
    "H": [Time(hour=9, minute=40), Time(hour=20, minute=40), 1],
    "I": [Time(hour=10, minute=40), Time(hour=18, minute=40), 1],
    "J": [Time(hour=12, minute=0), Time(hour=18, minute=0), 1],
    "K": [Time(hour=9, minute=40), Time(hour=20, minute=30), 1],
    "T": [Time(hour=12, minute=0), Time(hour=18, minute=40), 1],
    "S": [Time(hour=12, minute=0), Time(hour=18, minute=40), 1],
}
timelyDownStands = {
    "SU": [Time(hour=9, minute=0), Time(hour=10, minute=0), 3],
    "DT": [Time(hour=14, minute=0), Time(hour=14, minute=0), 3],
    "ST": [Time(hour=15, minute=0), Time(hour=15, minute=0), 5],
    "CU": [Time(hour=20, minute=40), Time(hour=21, minute=0), 5],
}
priorityDownStands = {
    "O": [Time(hour=0, minute=0), "end of day", 1],
    "X": [Time(hour=0, minute=0), "end of day", 1],
    "P": [Time(hour=0, minute=0), "end of day", 1],
}
fillInDownStands = {
    "W": [Time(hour=0, minute=0), "end of day"],
}
standData = {
    "up": upStands,
    "timely down": timelyDownStands,
    "priority down": priorityDownStands,
    "fill-in down": fillInDownStands,
}

staticAppInfo.setEventDataSpecific(standData, eventDescriptor="stand")

# Create information for the stands
lifeguards = {
    "1": [Time(hour=9, minute=0), Time(hour=17, minute=0)],
    "2": [Time(hour=9, minute=0), Time(hour=17, minute=0)],
    "3": [Time(hour=9, minute=0), Time(hour=17, minute=0)],
    "4": [Time(hour=9, minute=0), Time(hour=17, minute=0)],
    "5": [Time(hour=10, minute=0), Time(hour=18, minute=0)],
    "6": [Time(hour=10, minute=40), Time(hour=18, minute=40)],
    "7": [Time(hour=11, minute=0), Time(hour=19, minute=0)],
    "8": [Time(hour=11, minute=0), Time(hour=19, minute=0)],
    "9": [Time(hour=11, minute=40), Time(hour=19, minute=40)],
    "10": [Time(hour=12, minute=0), Time(hour=20, minute=0)],
    "11": [Time(hour=13, minute=0), Time(hour=21, minute=0)],
    "12": [Time(hour=13, minute=0), Time(hour=21, minute=0)],
    "13": [Time(hour=13, minute=0), Time(hour=21, minute=0)],
    "14": [Time(hour=13, minute=0), Time(hour=21, minute=0)],
    "15": [Time(hour=13, minute=0), Time(hour=21, minute=0)],
    "16": [Time(hour=13, minute=0), Time(hour=21, minute=0)],
    "17": [Time(hour=13, minute=0), Time(hour=21, minute=0)],
    "18": [Time(hour=13, minute=0), Time(hour=21, minute=0)],
    "19": [Time(hour=13, minute=0), Time(hour=21, minute=0)],
}

lifeguardData = {
    "lifeguard": lifeguards,
}

staticAppInfo.setEventDataSpecific(lifeguardData, eventDescriptor="lifeguard")

"""END OF HARDCODING, BEGINNING OF DEVELOPING ALGORITHM"""

calculator = CalculateSchedule(staticAppInfo=staticAppInfo)


def calculateSchedule():
    calculator.resetSchedule()
    calculator.assignBreaks()
    calculator.calculateSchedule()


calculateSchedule()
calculator.printSchedule()

"""
count = 0
start = time.time()
print("starting calculation")
while count < 1:
    calculateSchedule()
    count += 1
print(time.time() - start)

calculator.printSchedule()

print(f"\n{count}")
"""

"""
TEST CODE FOR RECURSIVE FUNCTIONS
values = [
    [4, 8, 1, 3],
    [9, 1, 4, 2],
    [3, 2, 4],
    [8, 4, 9, 11],
    [3, 10, 7, 5, 8],
]

options = calculator.recursivelyGenerateRearrangementPermutations(values)
staticAppInfo.printRecursivelyLongDictionary(options)
print()
optionsList = calculator.recursivelyInterpretGeneratedDictionary(options)
for value in optionsList:
    print(value)

print()
def listsAreEqual(list1, list2, s):
    result = True
    for i in range(0, len(list1)):
        s.incrementCount()
        if list1[i] != list2[i]:
            result = False
    return result

result1 = False
for n in range(0, len(optionsList)):
    for k in range(0, len(optionsList)):
        if k != n:
            if listsAreEqual(optionsList[n], optionsList[k], staticAppInfo):
                result1 = True
print(result1)
print(staticAppInfo.getCount())

print(len(optionsList), "possible permutations generated")
"""

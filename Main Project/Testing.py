# import libraries
import random
import time
import tkinter as tk

from CalculateSchedule import CalculateSchedule
from Stand import Stand
from StaticAppInfo import StaticAppInfo
from Time import Time

"""THE FIRST PART OF THIS CODE IS JUST HARDCODING INFORMATION   """
# Create static app info
staticAppInfo = StaticAppInfo(tk.Tk())

# Create all the information for the stands
upStands = {
    "E": [Time(hour=11, minute=0), Time(hour=20, minute=0), 1],
    "H": [Time(hour=11, minute=0), Time(hour=20, minute=0), 1],
    "K": [Time(hour=11, minute=0), Time(hour=20, minute=0), 1],
    "A": [Time(hour=12, minute=0), Time(hour=19, minute=0), 1],
    "B": [Time(hour=12, minute=0), Time(hour=19, minute=0), 1],
    "I": [Time(hour=13, minute=0), Time(hour=16, minute=0), 1],
    "T": [Time(hour=13, minute=0), Time(hour=19, minute=0), 1],
    "S": [Time(hour=13, minute=0), Time(hour=19, minute=0), 1],
}
timelyDownStands = {
    "SU": [Time(hour=10, minute=40), Time(hour=11, minute=0), 3],
    "DT": [Time(hour=14, minute=0), Time(hour=14, minute=20), 2],
    "ST": [Time(hour=15, minute=0), Time(hour=15, minute=20), 2],
    "CU": [Time(hour=20, minute=0), Time(hour=21, minute=0), 5],
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
    "1": [Time(hour=10, minute=40), Time(hour=18, minute=40)],
    "2": [Time(hour=10, minute=40), Time(hour=18, minute=40)],
    "3": [Time(hour=10, minute=40), Time(hour=18, minute=40)],
    "4": [Time(hour=11, minute=0), Time(hour=19, minute=0)],
    "5": [Time(hour=11, minute=0), Time(hour=14, minute=0)],
    "6": [Time(hour=11, minute=0), Time(hour=19, minute=0)],
    "7": [Time(hour=12, minute=0), Time(hour=20, minute=0)],
    "8": [Time(hour=11, minute=40), Time(hour=19, minute=40)],
    "9": [Time(hour=13, minute=0), Time(hour=21, minute=0)],
    "10": [Time(hour=13, minute=0), Time(hour=21, minute=0)],
    "11": [Time(hour=13, minute=0), Time(hour=21, minute=0)],
    "12": [Time(hour=13, minute=0), Time(hour=21, minute=0)],
    "13": [Time(hour=13, minute=0), Time(hour=21, minute=0)],
}

lifeguardData = {
    "lifeguard": lifeguards,
}

staticAppInfo.setEventDataSpecific(lifeguardData, eventDescriptor="lifeguard")

"""END OF HARDCODING, BEGINNING OF DEVELOPING ALGORITHM"""


def calculateSchedule():
    calc = CalculateSchedule(staticAppInfo=staticAppInfo)
    calc.resetSchedule()
    calc.assignBreaks()
    calc.calculateSchedule()
    return calc


def checkScheduleForDoubles(calc: CalculateSchedule):
    found = False

    calcLifeguards = calc.getLifeguards()

    upStandNames = calc.getUpStandNames()

    for lifeguard in calcLifeguards:
        stands = list(lifeguard.getSchedule().values())

        for i in range(1, len(stands)):
            lastStand = stands[i - 1]
            thisStand = stands[i]

            if thisStand in upStandNames and lastStand == thisStand:
                found = True

                lastTime = list(lifeguard.getSchedule().keys())[i - 1]

                print(
                    f"{lifeguard.getIdNum()} has double stands {lastStand} and {thisStand} at {lastTime.get12Time()}"
                )

    return found


"""
for i in range(100):
    myCalc = calculateSchedule()

    if checkScheduleForDoubles(myCalc):
        myCalc.printSchedule()
        print(f"Calculation number {i}")
        print()
"""


calculator = calculateSchedule()

blockLengthToCount: dict[int, int] = {}
for lifeguard in calculator.getLifeguards():
    schedule = lifeguard.getSchedule()

    for currentTime in schedule:
        currentStand = lifeguard.getStand(currentTime)

        lastTime = Time().setTimeWithMinutes(
            currentTime.getMinutes() - staticAppInfo.getTimeInterval()
        )
        lastStand = lifeguard.getStand(lastTime)

        upStands = calculator.getUpStandNames()

        if currentStand in upStands and lastStand not in upStands:
            blockLength = lifeguard.getUpStandsFromTime(currentTime, upStands)

            count = blockLengthToCount.get(blockLength, 0)

            blockLengthToCount[blockLength] = count + 1

sortedBlockLengthKeys = sorted(list(blockLengthToCount.keys()))
for blockLength in sortedBlockLengthKeys:
    count = blockLengthToCount[blockLength]
    print(f"There were {count} blocks with length {blockLength}")

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

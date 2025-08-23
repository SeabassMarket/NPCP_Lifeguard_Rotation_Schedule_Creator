# import libraries
import tkinter as tk

from InfoManagers.CalculateSchedule import CalculateSchedule
from InfoManagers.StaticAppInfo import StaticAppInfo
from InfoManagers.Time import Time

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

calculator = CalculateSchedule(staticAppInfo)

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


checks = 0


def listsAreEqual(list1, list2):
    global checks

    result = True
    for i in range(0, len(list1)):
        checks += 1
        if list1[i] != list2[i]:
            result = False
    return result


duplicates = False
for n in range(0, len(optionsList)):
    for k in range(0, len(optionsList)):
        if k != n:
            if listsAreEqual(optionsList[n], optionsList[k]):
                duplicates = True

print("Values Tested:")
for valueList in values:
    print(valueList)

print()

print(f"Duplicates? {duplicates}")
print(f"Checks performed: {checks}")
print(len(optionsList), "possible permutations generated")

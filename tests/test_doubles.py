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


def calculateSchedule():
    calc = CalculateSchedule(staticAppInfo=staticAppInfo)
    calc.resetSchedule()
    calc.assignBreaks()
    calc.calculateStands()
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


for i in range(100):
    print(f"Test number {i + 1}: ", end="")
    myCalc = calculateSchedule()

    if checkScheduleForDoubles(myCalc):
        print("positive")
        myCalc.printSchedule()
        print(f"Calculation number {i}")
        print()
    else:
        print("negative")

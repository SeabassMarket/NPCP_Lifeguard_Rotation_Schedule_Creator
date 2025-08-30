# import libraries
import tkinter as tk

from ..InfoManagers.CalculateSchedule import CalculateSchedule
from ..InfoManagers.StaticAppInfo import StaticAppInfo
from ..InfoManagers.Time import Time

from ..GoogleAPICommunicators.GoogleSheetsCommunicator import GSCommunicator

"""THE FIRST PART OF THIS CODE IS JUST HARDCODING INFORMATION"""

# Create static app info
staticAppInfo = StaticAppInfo(tk.Tk())

# Create all the information for the stands
upStands = {
    "E": [Time(hour=11, minute=0), Time(hour=20, minute=0), 1],
    "H": [Time(hour=11, minute=0), Time(hour=20, minute=0), 1],
    "K": [Time(hour=11, minute=0), Time(hour=20, minute=0), 1],
    "A": [Time(hour=13, minute=0), Time(hour=19, minute=0), 1],
    "B": [Time(hour=13, minute=0), Time(hour=19, minute=0), 1],
    "I": [Time(hour=11, minute=0), Time(hour=19, minute=0), 1],
}
timelyDownStands = {
    "SU": [Time(hour=10, minute=40), Time(hour=11, minute=0), 10],
    "DT": [Time(hour=14, minute=0), Time(hour=14, minute=20), 3],
    "ST": [Time(hour=15, minute=0), Time(hour=15, minute=20), 3],
    "CU": [Time(hour=20, minute=0), Time(hour=21, minute=0), 10],
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
    "Anik": [Time(hour=10, minute=40), Time(hour=18, minute=40)],
    "Kyle": [Time(hour=10, minute=40), Time(hour=18, minute=40)],
    "Eve": [Time(hour=11, minute=0), Time(hour=19, minute=0)],
    "Grayson": [Time(hour=11, minute=0), Time(hour=19, minute=0)],
    "Rowan": [Time(hour=11, minute=0), Time(hour=15, minute=0)],
    "Sophie": [Time(hour=11, minute=0), Time(hour=19, minute=0)],
    "Ty": [Time(hour=11, minute=40), Time(hour=15, minute=0)],
    "Brynn": [Time(hour=13, minute=0), Time(hour=21, minute=0)],
    "Connie": [Time(hour=13, minute=0), Time(hour=21, minute=0)],
    "Saniya": [Time(hour=13, minute=0), Time(hour=21, minute=0)],
    "Shalen": [Time(hour=13, minute=0), Time(hour=21, minute=0)],
    "Christian": [Time(hour=15, minute=0), Time(hour=17, minute=0)],
    "Milla": [Time(hour=17, minute=0), Time(hour=19, minute=40)],
}

lifeguardData = {
    "lifeguard": lifeguards,
}

staticAppInfo.setEventDataSpecific(lifeguardData, eventDescriptor="lifeguard")

"""END OF HARDCODING, BEGINNING OF DEVELOPING ALGORITHM"""

calculator = CalculateSchedule(staticAppInfo)
calculator.calculateSchedule()
calculator.printSchedule()

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

            if blockLength == 3:
                print(currentTime.get12Time())

sortedBlockLengthKeys = sorted(list(blockLengthToCount.keys()))
for blockLength in sortedBlockLengthKeys:
    count = blockLengthToCount[blockLength]
    print(f"There were {count} blocks with length {blockLength}")

print("Continue?", end="")
input()

# Use GSCommunicator
gs = GSCommunicator(staticAppInfo, calculator, 3, 1)

gs.setWorksheet("Lifeguard Schedule", "NPCP_GOOGLE_SHEETS_KEY")
gs.writeScheduleToWorksheet()
print(f"Schedule uploaded: {gs.getItem('spreadsheet').url}")

# Functions for program

# Main program for lifeguard rotation schedule

# Import classes
from ReplLifeguard import Lifeguard
from ReplPool import Pool
from ReplSchedule import Schedule
from ReplTime import Time

# Create pool
pool = (
    Pool()
    .setLifeguardsAugust3rd()
    .autoSetPoolsOpenAndClose()
    .sortLifeguardsBasedOnShifts()
    .generateBreaks()
    .updateLifeguardsBreaksInStands()
    .sortLifeguardsBasedOnBreaks()
)

# Create schedule
schedule = Schedule()
schedule.setStandA(
    [
        [Time(12, 0), Time(20, 0)],
    ]
)
schedule.setStandB(
    [
        [Time(11, 0), Time(20, 0)],
    ]
)
schedule.setStandC(
    [
        [Time(13, 0), Time(19, 0)],
    ]
)
schedule.setStandE(
    [
        [Time(11, 0), Time(20, 0)],
    ]
)
schedule.setStandF([])
schedule.setStandG([])
schedule.setStandH(
    [
        [Time(11, 0), Time(20, 0)],
    ]
)
schedule.setStandI(
    [
        [Time(12, 0), Time(19, 0)],
    ]
)
schedule.setStandJ([])
schedule.setStandK(
    [
        [Time(11, 0), Time(20, 0)],
    ]
)
schedule.setStandT(
    [
        [Time(13, 0), Time(19, 0)],
    ]
)
schedule.setStandS(
    [
        [Time(13, 0), Time(19, 0)],
    ]
)
schedule.setExtraStands({})
schedule.setDownStands(
    [
        {
            "DT": [3, [Time(14, 0)]],
            "ST": [3, [Time(15, 0)]],
            "SU": [6, [Time(10, 40), Time(11, 0)]],
            "CU": [20, [Time(20, 0), Time(20, 20), Time(20, 40)]],
        },
        ["O", "X", "P"],
        ["W"],
        ["Y"],
    ]
)

# Testing
pool.generateRotationSchedule(schedule).printRotationSchedule(4)

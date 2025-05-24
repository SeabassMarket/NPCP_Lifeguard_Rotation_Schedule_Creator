# Imports classes
from ReplLifeguard import Lifeguard
import math
import random
from ReplSchedule import Schedule
from ReplTime import Time


# Creates a pool object to store information and data about a pool
class Pool:

    # Constructs pool object
    def __init__(self,
                 poolOpen=None,
                 poolClose=None,
                 upperPoolOpen=None,
                 upperPoolClose=None,
                 lowerPoolOpen=None,
                 lowerPoolClose=None,
                 defaultUpperPoolStands=None,
                 defaultLowerPoolStands=None,
                 breakLength=None,
                 timePerStand=None,
                 maxTimeWithoutBreak=None,
                 maxGuardsOnBreak=2,
                 lifeguards=None,
                 diveTestTime=None,
                 swimTestTime=None):
        self.setPool(poolOpen,
                     poolClose,
                     upperPoolOpen,
                     upperPoolClose,
                     lowerPoolOpen,
                     lowerPoolClose,
                     defaultUpperPoolStands,
                     defaultLowerPoolStands,
                     breakLength,
                     timePerStand,
                     maxTimeWithoutBreak,
                     maxGuardsOnBreak,
                     lifeguards,
                     diveTestTime,
                     swimTestTime)

    # Getters
    def getPoolOpen(self):
        return Time(self._poolOpen.get24Hour(), self._poolOpen.getMinute())

    def getReferencePoolOpen(self):
        return self._poolOpen

    def getPoolClose(self):
        return Time(self._poolClose.get24Hour(), self._poolClose.getMinute())

    def getReferencePoolClose(self):
        return self._poolClose

    def getUpperPoolOpen(self):
        return Time(self._upperPoolOpen.get24Hour(), self._upperPoolOpen.getMinute())

    def getReferenceUpperPoolOpen(self):
        return self._upperPoolOpen

    def getUpperPoolClose(self):
        return Time(self._upperPoolClose.get24Hour(), self._upperPoolClose.getMinute())

    def getReferenceUpperPoolClose(self):
        return self._upperPoolClose

    def getLowerPoolOpen(self):
        return Time(self._lowerPoolOpen.get24Hour(), self._lowerPoolOpen.getMinute())

    def getReferenceLowerPoolOpen(self):
        return self._lowerPoolOpen

    def getLowerPoolClose(self):
        return Time(self._lowerPoolClose.get24Hour(), self._lowerPoolClose.getMinute())

    def getReferenceLowerPoolClose(self):
        return self._lowerPoolClose

    def getDefaultUpperPoolStands(self):
        return list(self._defaultUpperPoolStands)

    def getReferenceUpperPoolStands(self):
        return self._defaultUpperPoolStands

    def getDefaultLowerPoolStands(self):
        return list(self._defaultLowerPoolStands)

    def getReferenceDefaultLowerPoolStands(self):
        return self._defaultLowerPoolStands

    def getBreakLength(self):
        return self._breakLength

    def getTimePerStand(self):
        return Time(self._timePerStand.get24Hour(), self._timePerStand.getMinute())

    def getMaxTimeWithoutBreak(self):
        return Time(self._maxTimeWithoutBreak.get24Hour(),
                    self._maxTimeWithoutBreak.getMinute())

    def getMaxGuardsOnBreak(self):
        return self._maxGuardsOnBreak

    def getLifeguards(self):
        list = []
        for guards in self._lifeguards:
            list.append(guards.getLifeguard())
        return list

    def getReferenceLifeguards(self):
        return self._lifeguards

    def getDiveTestTime(self):
        return Time(self._diveTestTime.get24Hour(), self._diveTestTime.getMinute())

    def getReferenceDiveTestTime(self):
        return self._diveTestTime

    def getSwimTestTime(self):
        return Time(self._swimTestTime.get24Hour(), self._swimTestTime.getMinute())

    def getReferenceSwimTestTime(self):
        return self._swimTestTime

    def getGuardsWorking(self, currentTime):
        count = 0
        if isinstance(currentTime, Time):
            for lifeguard in self._lifeguards:
                if lifeguard.isWorking(currentTime):
                    count = count + 1
        return count

    def getWorkingLifeguards(self, currentTime):
        list = []
        if isinstance(currentTime, Time):
            for lifeguard in self._lifeguards:
                if lifeguard.isWorking(currentTime):
                    list.append(lifeguard)
        return list

    def isPoolOpen(self, currentTime):
        if isinstance(currentTime, Time):
            return (self._poolOpen.getMinutes() <= currentTime.getMinutes() and
                    self._poolClose.getMinutes() > currentTime.getMinutes())
        return False

    def isUpperPoolOpen(self, currentTime):
        if isinstance(currentTime, Time):
            return (self._upperPoolClose.getMinutes() <= currentTime.getMinutes() and
                    self._upperPoolClose.getMinutes() > currentTime.getMinutes())
        return False

    def isLowerPoolOpen(self, currentTime):
        if isinstance(currentTime, Time):
            return (self._lowerPoolOpen.getMinutes() <= currentTime.getMinutes() and
                    self._lowerPoolClose.getMinutes() > currentTime.getMinutes())
        return False

    # Setters
    def setPoolOpen(self, time):
        if isinstance(time, Time):
            self._poolOpen = time
        else:
            self._poolOpen = Time(9, 0)
        return self

    def setPoolClose(self, time):
        if isinstance(time, Time):
            self._poolClose = time
        else:
            self._poolClose = Time(21, 0)
        return self

    def setUpperPoolOpen(self, time):
        if isinstance(time, Time):
            self._upperPoolOpen = time
        else:
            self._upperPoolOpen = Time(9, 0)
        return self

    def setUpperPoolClose(self, time):
        if isinstance(time, Time):
            self._upperPoolClose = time
        else:
            self._upperPoolClose = Time(21, 0)
        return self

    def setLowerPoolOpen(self, time):
        if isinstance(time, Time):
            self._lowerPoolOpen = time
        else:
            self._lowerPoolOpen = Time(9, 0)
        return self

    def setLowerPoolClose(self, time):
        if isinstance(time, Time):
            self._lowerPoolClose = time
        else:
            self._lowerPoolClose = Time(21, 0)
        return self

    def setDefaultUpperPoolStands(self, defaultUpperPoolStands):
        if isinstance(defaultUpperPoolStands, list):
            self._defaultUpperPoolStands = defaultUpperPoolStands
        else:
            self._defaultUpperPoolStands = ["A", "B"]
        return self

    def setDefaultLowerPoolStands(self, defaultLowerPoolStands):
        if isinstance(defaultLowerPoolStands, list):
            self._defaultLowerPoolStands = defaultLowerPoolStands
        else:
            self._defaultLowerPoolStands = ["E", "K", "H"]
        return self

    def setBreakLength(self, breakLength):
        if isinstance(breakLength, int):
            self._breakLength = breakLength
        else:
            self._breakLength = 2
        return self

    def setTimePerStand(self, timePerStand):
        if isinstance(timePerStand, Time):
            self._timePerStand = timePerStand
        else:
            self._timePerStand = Time(0, 20)
        return self

    def setMaxTimeWithoutBreak(self, maxTimeWithoutBreak):
        if isinstance(maxTimeWithoutBreak, Time):
            self._maxTimeWithoutBreak = maxTimeWithoutBreak
        else:
            self._maxTimeWithoutBreak = Time(5, 0)
        return self

    def setMaxGuardsOnBreak(self, maxGuardsOnBreak):
        if isinstance(maxGuardsOnBreak, int):
            self._maxGuardsOnBreak = maxGuardsOnBreak
        else:
            self._maxGuardsOnBreak = 2
        return self

    def setLifeguards(self, lifeguards):
        valid = True
        if isinstance(lifeguards, list):
            for lifeguard in lifeguards:
                if not isinstance(lifeguard, Lifeguard):
                    valid = False
        else:
            valid = False
        if valid:
            self._lifeguards = lifeguards
        else:
            self._lifeguards = []
        return self

    def setDiveTestTime(self, diveTestTime):
        if isinstance(diveTestTime, Time):
            self._diveTestTime = diveTestTime
        else:
            self._diveTestTime = Time(14, 00)
        return self

    def setSwimTestTime(self, swimTestTime):
        if isinstance(swimTestTime, Time):
            self._swimTestTime = swimTestTime
        else:
            self._swimTestTime = Time(15, 0)
        return self

    def setDefaultLifeguards(self):
        self._lifeguards = []
        for i in range(0, 6):
            self._lifeguards.append(Lifeguard(i, Time(10, 40), Time(18, 40)))
        self._lifeguards.append(Lifeguard(6, Time(11, 0), Time(19, 0)))
        self._lifeguards.append(Lifeguard(7, Time(11, 20), Time(19, 20)))
        self._lifeguards.append(Lifeguard(8, Time(11, 40), Time(19, 40)))
        self._lifeguards.append(Lifeguard(9, Time(12, 0), Time(20, 0)))
        for i in range(10, 16):
            self._lifeguards.append(Lifeguard(i, Time(13, 0), Time(21, 0)))
        self._lifeguards.append(Lifeguard(16, Time(13, 0), Time(18, 0)))
        return self

    def setLifeguardsAugust3rd(self):
        self._lifeguards = []
        for i in range(0, 3):
            self._lifeguards.append(Lifeguard(i, Time(10, 40), Time(18, 40)))
        for i in range(3, 7):
            self._lifeguards.append(Lifeguard(i, Time(11, 0), Time(19, 0)))
        self._lifeguards.append(Lifeguard(7, Time(11, 40), Time(19, 40)))
        self._lifeguards.append(Lifeguard(8, Time(12, 0), Time(20, 0)))
        for i in range(9, 15):
            self._lifeguards.append(Lifeguard(i, Time(13, 0), Time(21, 0)))
        return self

    def autoSetPoolsOpenAndClose(self):
        if len(self._lifeguards) > 0:
            minimum = self._lifeguards[0].getShiftStart().getMinutes()
            for lifeguard in self._lifeguards:
                if lifeguard.getShiftStart().getMinutes() < minimum:
                    minimum = lifeguard.getShiftStart().getMinutes()
            self.setPoolOpen(Time().setTimeWithMinutes(minimum))
            self.setUpperPoolOpen(Time().setTimeWithMinutes(minimum))
            self.setLowerPoolOpen(Time().setTimeWithMinutes(minimum))
            maximum = self._lifeguards[0].getShiftEnd().getMinutes()
            for lifeguard in self._lifeguards:
                if lifeguard.getShiftEnd().getMinutes() > maximum:
                    maximum = lifeguard.getShiftEnd().getMinutes()
            self.setPoolClose(Time().setTimeWithMinutes(maximum))
            self.setUpperPoolClose(Time().setTimeWithMinutes(maximum))
            self.setLowerPoolClose(Time().setTimeWithMinutes(maximum))
        return self

    def setPool(self,
                poolOpen=None,
                poolClose=None,
                upperPoolOpen=None,
                upperPoolClose=None,
                lowerPoolOpen=None,
                lowerPoolClose=None,
                defaultUpperPoolStands=None,
                defaultLowerPoolStands=None,
                breakLength=None,
                timePerStand=None,
                maxTimeWithoutBreak=None,
                maxGuardsOnBreak=2,
                lifeguards=None,
                diveTestTime=None,
                swimTestTime=None):
        self.setPoolOpen(poolOpen)
        self.setPoolClose(poolClose)
        self.setUpperPoolOpen(upperPoolOpen)
        self.setUpperPoolClose(upperPoolClose)
        self.setLowerPoolOpen(lowerPoolOpen)
        self.setLowerPoolClose(lowerPoolClose)
        self.setDefaultUpperPoolStands(defaultUpperPoolStands)
        self.setDefaultLowerPoolStands(defaultLowerPoolStands)
        self.setBreakLength(breakLength)
        self.setTimePerStand(timePerStand)
        self.setMaxTimeWithoutBreak(maxTimeWithoutBreak)
        self.setMaxGuardsOnBreak(maxGuardsOnBreak)
        self.setLifeguards(lifeguards)
        self.setDiveTestTime(diveTestTime)
        self.setSwimTestTime(swimTestTime)
        return self

    # Generators/Advanced functions
    def generateBreaks(self):
        for lifeguard in self._lifeguards:

            # Checks how many breaks will be needed for the guard
            breaks = math.ceil((lifeguard.getShiftLength().getMinutes() -
                                self.getMaxTimeWithoutBreak().getMinutes())
                               / (self.getMaxTimeWithoutBreak().getMinutes() +
                                  self.getBreakLength() * self.getTimePerStand().getMinutes()))

            # Store eligible times for each lifeguard
            if breaks == 1:
                eligibleTimes = []
                time = lifeguard.getShiftStart()
                while time.getMinutes() < lifeguard.getShiftEnd().getMinutes():
                    if (lifeguard.getTimeIntoShift(time).getMinutes() <=
                            self._maxTimeWithoutBreak.getMinutes() and
                            lifeguard.getTimeLeftShift(
                                time.getTime().addMinutes(
                                    self._breakLength * self.getTimePerStand().getMinutes())
                            ).getMinutes() <=
                            self._maxTimeWithoutBreak.getMinutes()):
                        eligibleTimes.append(time.getTime())
                    time.addTime(self.getTimePerStand())

                # Get how many guards will be working during the break
                guardsWorking = []
                for time in eligibleTimes:
                    breakTimes = []
                    for i in range(0, self._breakLength):
                        breakTimes.append(self.getGuardsWorking(Time().setTimeWithMinutes(
                            time.getMinutes() + i * self.getTimePerStand().getMinutes())))
                    guardsWorking.append(breakTimes)

                # Get the best time for each guard
                totals = []
                for nums in guardsWorking:
                    total = 0
                    for num in nums:
                        total = total + num
                    totals.append(total)

                max = totals[0]
                index = 0
                for i in range(0, len(totals)):
                    if totals[i] >= max:
                        max = totals[i]
                        index = i

                # Set the best time for the guard
                lifeguard.setBreakStart(eligibleTimes[index].getTime())
                lifeguard.setBreakEnd(eligibleTimes[index].getTime().addMinutes(
                    self.getBreakLength() * self.getTimePerStand().getMinutes()))

                '''
                print(breaks)
                for i in range(0, len(guardsWorking)):
                  print(str(totals[i]) + " " + str(guardsWorking[i]) + " " + 
                  eligibleTimes[i].get24Time())
                print(str(index) + " " + (eligibleTimes[index].get24Time()))
              print()
              '''
        return self

    # Generates the rotation schedule
    def generateRotationSchedule(self, schedule):
        if isinstance(schedule, Schedule):

            # Reset random chances in lifeguards
            for lifeguard in self._lifeguards:
                lifeguard.setRandomChance(0)

            # Iterate through each time
            time = self.getPoolOpen()
            while time.getMinutes() < self.getPoolClose().getMinutes():

                # Assign each open stand to a working lifeguard
                openStands = schedule.getOnlyOpenStands(time)
                workingLifeguards = self.getWorkingLifeguards(time)
                lifeguardsOnStand = []

                # Find out who's on stand
                for j in range(0, len(openStands)):

                    # Find out who has the least amount of stands up
                    standsUp = []
                    for lifeguard in workingLifeguards:
                        standsUp.append(lifeguard.getStandsUp(time, schedule))
                    minimum = min(standsUp) if len(standsUp) > 0 else 0
                    lifeguardsWithLowestStandsUp = []
                    for i in range(0, len(standsUp)):
                        if standsUp[i] == minimum:
                            lifeguardsWithLowestStandsUp.append(workingLifeguards[i])

                    # Find who has the least amount of time until break or done
                    lifeguardsWithLowestTimeUntilOff = []
                    if len(lifeguardsWithLowestStandsUp) > 1:
                        timeUntilOff = []
                        for lifeguard in lifeguardsWithLowestStandsUp:
                            if (lifeguard.getTimeUntilBreak(time).getMinutes() >
                                    lifeguard.getTimeLeftShift(time).getMinutes()):
                                timeUntilOff.append(lifeguard.getTimeLeftShift(time).getMinutes())
                            else:
                                timeUntilOff.append(lifeguard.getTimeUntilBreak(time).getMinutes())
                        minimum = min(timeUntilOff)
                        for i in range(0, len(timeUntilOff)):
                            if timeUntilOff[i] == minimum:
                                lifeguardsWithLowestTimeUntilOff.append(
                                    lifeguardsWithLowestStandsUp[i]
                                )
                    elif len(lifeguardsWithLowestStandsUp) == 1:
                        lifeguardsOnStand.append(lifeguardsWithLowestStandsUp[0])
                        workingLifeguards.pop(workingLifeguards.index(
                            lifeguardsWithLowestStandsUp[0]
                        ))

                    # Find who has the least amount of random chance generations
                    if len(lifeguardsWithLowestTimeUntilOff) > 1:
                        randomChance = []
                        for lifeguard in lifeguardsWithLowestTimeUntilOff:
                            randomChance.append(lifeguard.getRandomChance())
                        lifeguardsWithLowestRandomChance = []
                        minimum = min(randomChance)
                        for i in range(0, len(randomChance)):
                            if randomChance[i] == minimum:
                                lifeguardsWithLowestRandomChance.append(
                                    lifeguardsWithLowestTimeUntilOff[i]
                                )
                        # If there is more than one lifeguard with the lowest random chance
                        if len(lifeguardsWithLowestRandomChance) > 1:
                            randomNumber = random.randint(
                                0, len(lifeguardsWithLowestRandomChance) - 1
                            )
                            lifeguardsOnStand.append(lifeguardsWithLowestRandomChance[randomNumber])
                            # If it really does come down to random chance, up the random chance value
                            if len(openStands) - j < len(lifeguardsWithLowestRandomChance):
                                lifeguardsWithLowestRandomChance[randomNumber].setRandomChance(
                                    lifeguardsWithLowestRandomChance[randomNumber].getRandomChance() + 1
                                )
                            workingLifeguards.pop(workingLifeguards.index(
                                lifeguardsWithLowestRandomChance[randomNumber]
                            ))
                        # Otherwise, just pick the one in the list
                        elif len(lifeguardsWithLowestRandomChance) == 1:
                            lifeguardsOnStand.append(lifeguardsWithLowestRandomChance[0])
                            workingLifeguards.pop(workingLifeguards.index(
                                lifeguardsWithLowestRandomChance[0]
                            ))
                    # If there is only one lifeguard with the lowest time until off,
                    # Assign them the stand
                    elif len(lifeguardsWithLowestTimeUntilOff) == 1:
                        lifeguardsOnStand.append(lifeguardsWithLowestTimeUntilOff[0])
                        workingLifeguards.pop(workingLifeguards.index(
                            lifeguardsWithLowestTimeUntilOff[0]
                        ))

                # Generate lifeguards that are down
                lifeguardsDown = []
                for lifeguard in workingLifeguards:
                    if lifeguard not in lifeguardsOnStand:
                        lifeguardsDown.append(lifeguard)

                # Set stand assignments
                previousStands = []
                for lifeguard in lifeguardsOnStand:
                    previousStands.append(
                        lifeguard.getStands()[lifeguard.getPriorStandTime(time).getMinutes()]
                    )
                unAssignedStands = []
                for stand in openStands:
                    eligibleLifeguards = []
                    for i in range(0, len(lifeguardsOnStand)):
                        if previousStands[i] != stand:
                            eligibleLifeguards.append(lifeguardsOnStand[i])
                    if len(eligibleLifeguards) == 0:
                        unAssignedStands.append(stand)
                    else:
                        randomNumber = random.randint(0, len(eligibleLifeguards) - 1)
                        eligibleLifeguards[randomNumber].getReferenceStands()[
                            time.getMinutes()] = stand
                        index = lifeguardsOnStand.index(eligibleLifeguards[randomNumber])
                        lifeguardsOnStand.pop(index)
                        previousStands.pop(index)
                if len(unAssignedStands) == len(lifeguardsOnStand):
                    for i in range(0, len(unAssignedStands)):
                        lifeguardsOnStand[i].getReferenceStands()[
                            time.getMinutes()] = unAssignedStands[i]

                # Set down assignments
                downStands = []
                j = 0
                while j < len(lifeguardsDown):
                    assigned = False
                    if not assigned:
                        for name, list1 in schedule.getReferenceDownStands()[0].items():
                            for value in list1[1]:
                                if (not assigned and time.getMinutes() == value.getMinutes() and
                                        list1[0] > 0):
                                    downStands.append(name)
                                    list1[0] = list1[0] - 1
                                    assigned = True
                    if not assigned:
                        for i in range(0, len(schedule.getDownStands()[1])):
                            if schedule.getDownStands()[1][i] not in downStands and not assigned:
                                downStands.append(schedule.getDownStands()[1][i])
                                assigned = True
                    if not assigned:
                        downStands.append(schedule.getDownStands()[2][0])
                        assigned = True
                    j = j + 1
                for lifeguard in lifeguardsDown:
                    randomNumber = random.randint(0, len(downStands) - 1)
                    lifeguard.getReferenceStands()[time.getMinutes()] = downStands[randomNumber]
                    downStands.pop(randomNumber)

                # Add time
                time.addTime(self.getTimePerStand())
        return self

    def sortLifeguardsBasedOnBreaks(self):
        breakStartTimes = []
        newLifeguardsSorting = []
        for lifeguard in self._lifeguards:
            breakStartTimes.append(lifeguard.getBreakStart().getMinutes())
        sortedBreakStartTimes = sorted(breakStartTimes)
        for num in sortedBreakStartTimes:
            index = breakStartTimes.index(num)
            newLifeguardsSorting.append(self._lifeguards[index])
            breakStartTimes[index] = "Taken"
        duplicate = []
        for lifeguard in newLifeguardsSorting:
            if lifeguard.getBreakLength().getMinutes() > 0:
                duplicate.append(lifeguard)
        for lifeguard in newLifeguardsSorting:
            if lifeguard.getBreakLength().getMinutes() == 0:
                duplicate.append(lifeguard)
        newLifeguardsSorting = duplicate
        self._lifeguards = newLifeguardsSorting
        for i in range(0, len(self._lifeguards)):
            self._lifeguards[i].setNumber(i)
        return self

    def sortLifeguardsBasedOnShifts(self):
        shiftStartTimes = []
        newLifeguardsSorting = []
        for lifeguard in self._lifeguards:
            shiftStartTimes.append(lifeguard.getShiftStart().getMinutes())
        sortedShiftStartTimes = sorted(shiftStartTimes)
        for num in sortedShiftStartTimes:
            index = shiftStartTimes.index(num)
            newLifeguardsSorting.append(self._lifeguards[index])
            shiftStartTimes[index] = -1
        self._lifeguards = newLifeguardsSorting
        for i in range(0, len(self._lifeguards)):
            self._lifeguards[i].setNumber(i)
        return self

    def printLifeguardBreaks(self):
        for lifeguard in self._lifeguards:
            print("%-2d" % (lifeguard.getNumber()) + " " +
                  lifeguard.getShiftStart().get12Time() + " - " +
                  lifeguard.getShiftEnd().get12Time() + " " +
                  lifeguard.getBreakStart().get12Time() + " - " +
                  lifeguard.getBreakEnd().get12Time())
        return self

    def updateLifeguardsBreaksInStands(self):
        for lifeguard in self._lifeguards:
            lifeguard.updateBreaksInStands()
        return self

    def printRotationSchedule(self, spacingLength):
        if isinstance(spacingLength, int):
            line = "%-8s" % ("Number") + "|"
            for lifeguard in self._lifeguards:
                line = (line + " " * (spacingLength - len(str(lifeguard.getNumber())))
                        + str(lifeguard.getNumber()) + "|")
            print(line)
            print("--------|" + ("-" * spacingLength + "|") * len(self._lifeguards))
            time = self.getPoolOpen()
            while time.getMinutes() < self.getPoolClose().getMinutes():
                line = ""
                line = line + time.get12Time() + "|"
                for lifeguard in self._lifeguards:
                    if time.getMinutes() in lifeguard.getStands():
                        line = (line + " " * (
                                spacingLength - len(lifeguard.getStands()[time.getMinutes()])
                        ) + lifeguard.getStands()[time.getMinutes()] + "|")
                    else:
                        line = line + (" " * spacingLength + "|")
                print(line)
                print("--------|" + ("-" * spacingLength + "|") * len(self._lifeguards))
                time.addTime(self.getTimePerStand())
        return self
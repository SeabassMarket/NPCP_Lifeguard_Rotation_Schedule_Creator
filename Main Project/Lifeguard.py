# import libraries
import math
from Time import Time
import time
from Stand import Stand
from StaticAppInfo import StaticAppInfo


# This object represents the aspects of a lifeguard
class Lifeguard:
    # Initialize lifeguard
    def __init__(
        self,
        shiftTimes,
        name,
        idNum,
        staticAppInfo,
        breakTimes=None,
    ):
        if isinstance(shiftTimes, list) and len(shiftTimes) == 2:
            self._startTime = shiftTimes[0]
            self._endTime = shiftTimes[1]
        else:
            self._startTime = Time()
            self._endTime = Time()

        # Initialize name
        self._name = name

        # Initialize idNum
        self._id = idNum

        # Initialize staticAppInfo
        if isinstance(staticAppInfo, StaticAppInfo):
            self._staticAppInfo = staticAppInfo
        else:
            self._staticAppInfo = StaticAppInfo("ERROR")
            print("ERROR, STATIC APP INFO NOT INITIALIZED")

        # Initialize break times
        if breakTimes is None:
            self._breakTimes = []
        else:
            self._breakTimes = breakTimes

        # Calculate the amount of breaks needed for a shift of the given length
        self._numBreaks = math.ceil(
            (
                self._endTime.getMinutes()
                - self._startTime.getMinutes()
                + self._staticAppInfo.getBreakTime()
            )
            / (
                self._staticAppInfo.getLongestTimeWorking()
                + self._staticAppInfo.getBreakTime()
            )
            - 1
        )
        # Set the manuel break to true or false depending on numBreaks
        self._manuelBreak = False
        if self._numBreaks > 1:
            self._manualBreak = True

        # Create a dictionary where the key is the time and the stand is the value
        self._schedule = dict()
        # Assign every time in the lifeguard schedule to NA
        for t in range(
            self._startTime.getMinutes(),
            self._endTime.getMinutes(),
            self._staticAppInfo.getTimeInterval(),
        ):
            # Create the time object
            thisTime = Time().setTimeWithMinutes(t)
            self._schedule[thisTime] = "EMPTY"
        self.updateBreaks()

        # Initialize random chance selections to 0
        self._randomChance = dict()
        self.resetRandomChance()

    # Returns the furthest time back until either the nearest shift start or break end
    def getFurthestTimeBackToDisruption(self, currentTime):
        # Check the type
        if not isinstance(currentTime, Time):
            print("ERROR IN LIFEGUARD - gFTBTD")
            return Time()

        # Create a list with all the shift start times and the break times
        # Initialize the list with the shift start
        timesOfBreaksAndShiftStarts = [self._startTime.getMinutes()]

        # Append the break times
        for breakTime in self._breakTimes:
            # Appends the end of the break
            timesOfBreaksAndShiftStarts.append(
                breakTime.getMinutes() + self._staticAppInfo.getBreakTime()
            )

        # Go back in time and go until the break times
        for t in range(len(timesOfBreaksAndShiftStarts) - 1, -1, -1):
            if timesOfBreaksAndShiftStarts[t] <= currentTime.getMinutes():
                return Time().setTimeWithMinutes(timesOfBreaksAndShiftStarts[t])

        # Return a string message if the current time is before the shift start (which will result in no time detected)
        return "CURRENT TIME BEFORE SHIFT START"

    # Swap the random chances going back to a certain time starting at a certain time with another lifeguard
    def swapRandomChances(self, otherLifeguard, backTime, nextTime):
        # Check type
        if (
            not isinstance(otherLifeguard, Lifeguard)
            or not isinstance(backTime, Time)
            or not isinstance(nextTime, Time)
        ):
            print("ERROR IN LIFEGUARD - sRC")
            return

        # Get the random chance dictionary of the other lifeguard
        otherRandomChance = otherLifeguard.getRandomChanceFullDictionary()

        # Swap the values between the two times given
        for t in range(
            backTime.getMinutes(),
            nextTime.getMinutes(),
            self._staticAppInfo.getTimeInterval(),
        ):
            timeBeingAnalyzed = Time().setTimeWithMinutes(t)
            otherTime = Time()
            for thisTime in otherRandomChance:
                if thisTime.equals(timeBeingAnalyzed):
                    otherTime = thisTime
            thisTime = Time()
            for thisTime in self._randomChance:
                if thisTime.equals(timeBeingAnalyzed):
                    thisTime = thisTime
            tempRandomChanceValue = otherRandomChance[otherTime]
            otherRandomChance[otherTime] = self._randomChance[thisTime]
            self._randomChance[thisTime] = tempRandomChanceValue

    # Returns the random chance dictionary of this lifeguard
    def getRandomChanceFullDictionary(self):
        return self._randomChance

    # Adds one to random chance
    def incrementRandomChance(self, currentTime):
        for thisTime in self._randomChance:
            if thisTime.equals(currentTime):
                self._randomChance[thisTime] = 1

    # Resets the random chance
    def resetRandomChance(self):
        self._randomChance = dict()
        for t in range(
            self._startTime.getMinutes(),
            self._endTime.getMinutes(),
            self._staticAppInfo.getTimeInterval(),
        ):
            thisTime = Time().setTimeWithMinutes(t)
            self._randomChance[thisTime] = 0

    # Returns the random chance
    def getRandomChance(self, currentTime):
        count = 0
        if isinstance(currentTime, Time):
            for thisTime in self._randomChance:
                if thisTime.getMinutes() < currentTime.getMinutes():
                    count += self._randomChance[thisTime]
        else:
            print("ERROR IN LIFEGUARD - gRC")
        return count

    # Returns how long the lifeguard has been up on stand given the time
    def getIntervalsUpOnStand(self, thisTime):
        # Check the type of the parameter
        if isinstance(thisTime, Time):
            # Get the index of the time given in self._schedule keys
            index = None
            scheduleTimes = list(self._schedule.keys())
            if thisTime.equals(self._endTime):
                index = len(scheduleTimes)
            else:
                for i in range(0, len(scheduleTimes)):
                    if scheduleTimes[i].equals(thisTime):
                        index = i
            # If the index is not assigned then the time given is invalid
            if index is None:
                return -1

            # Get the upStands list
            upStands = list(
                list(self._staticAppInfo.getEventDataSpecific("stand").values())[
                    0
                ].keys()
            )
            upStands.append(self._staticAppInfo.getUpStandCode())

            # Count how many stands in the current schedule prior to the given time are up stands
            count = 0
            i = 1
            while (
                index - i >= 0 and self._schedule[scheduleTimes[index - i]] in upStands
            ):
                count += 1
                i += 1

            # Return the value of count
            return count

        # Print error message and return a bad number
        print("ERROR IN LIFEGUARD - gIUOS wrong type")
        return -1

    # Returns how many intervals the lifeguard has been down on stand for a certain time
    def getIntervalsDownOnStand(self, thisTime):
        # Check the type of the parameter
        if isinstance(thisTime, Time):
            # Get the index of the time given in self._schedule keys
            index = None
            scheduleTimes = list(self._schedule.keys())
            if thisTime.equals(self._endTime):
                index = len(scheduleTimes)
            else:
                for i in range(0, len(scheduleTimes)):
                    if scheduleTimes[i].equals(thisTime):
                        index = i
            # If the index is not assigned then the time given is invalid
            if index is None:
                return -1

            # Get the upStands list
            upStands = list(
                list(self._staticAppInfo.getEventDataSpecific("stand").values())[
                    0
                ].keys()
            )

            # Count how many stands in the current schedule prior to the given time are not up stands
            count = 0
            i = 1
            while (
                index - i >= 0
                and self._schedule[scheduleTimes[index - i]] not in upStands
            ):
                count += 1
                i += 1

            # Return the value of count
            return count

        # Print error message and return a bad number
        print("ERROR IN LIFEGUARD - gIDOS wrong type")
        return -1

    # Returns the lifeguard's name
    def getName(self):
        return self._name

    # Swaps schedules up in a certain time frame with another lifeguard
    def swapSchedulesBetweenTimes(self, otherLifeguard, backTime, nextTime):
        # Check type
        if (
            not isinstance(otherLifeguard, Lifeguard)
            or not isinstance(backTime, Time)
            or not isinstance(nextTime, Time)
        ):
            print("ERROR IN LIFEGUARD - sSBT")
            return

        # Get the other schedule dictionary from the other lifeguard
        otherScheduleDictionary = otherLifeguard.getSchedule()

        # Iterate through and swap each stand at each location between back time and current time
        for t in range(
            backTime.getMinutes(),
            nextTime.getMinutes(),
            self._staticAppInfo.getTimeInterval(),
        ):
            # Get the keys for the two dictionaries
            timeBeingAnalyzed = Time().setTimeWithMinutes(t)

            otherTime = Time()
            for scheduleTime in otherScheduleDictionary:
                if scheduleTime.equals(timeBeingAnalyzed):
                    otherTime = scheduleTime

            thisTime = Time()
            for scheduleTime in self._schedule:
                if scheduleTime.equals(timeBeingAnalyzed):
                    thisTime = scheduleTime

            # Swap the values
            tempStandValue = otherScheduleDictionary[otherTime]
            otherScheduleDictionary[otherTime] = self._schedule[thisTime]
            self._schedule[thisTime] = tempStandValue

    # Swaps schedules with another lifeguard
    def swapSchedules(self, otherLifeguard):
        if isinstance(otherLifeguard, Lifeguard):
            tempSchedule = otherLifeguard.getSchedule()
            otherLifeguard.setSchedule(self._schedule)
            otherLifeguard.updateBreaks()
            self._schedule = tempSchedule
            self.updateBreaks()
        else:
            print("ERROR IN LIFEGUARD - SWAP SCHEDULE")

    # Swap at a specific time in the schedule with another lifeguard
    def swapSingularStandAtTime(self, otherLifeguard, currentTime):
        if isinstance(currentTime, Time) and isinstance(otherLifeguard, Lifeguard):
            tempStand = otherLifeguard.getStand(currentTime)
            otherLifeguard.addStand(currentTime, self.getStand(currentTime))
            self.addStand(currentTime, tempStand)
        else:
            print("ERROR IN LIFEGUARD - sSTAT")

    # Sets the schedule outright - CHECK FORMAT OUTSIDE OF THIS FUNCTION
    def setSchedule(self, schedule):
        self._schedule = schedule

    # Returns the schedule dictionary
    def getSchedule(self):
        return self._schedule

    # Returns the stand at a certain time
    def getStand(self, thisTime) -> str | None:
        if isinstance(thisTime, Time):
            for scheduleTime in self._schedule:
                if scheduleTime.equals(thisTime):
                    return self._schedule[scheduleTime]
        else:
            print("ERROR IN LIFEGUARD - GET STAND")
        return None

    # Adds a stand to the lifeguard's schedule at a certain time
    def addStand(self, thisTime, standName):
        if isinstance(thisTime, Time) and isinstance(standName, str):
            for scheduleTime in self._schedule:
                if scheduleTime.equals(thisTime):
                    self._schedule[scheduleTime] = standName
                    return scheduleTime
            print("ERROR IN LIFEGUARD - ADD STAND TIME NOT FOUND")
        else:
            print("ERROR IN LIFEGUARD - ADD STAND")
        return Time()

    # Returns the break times list
    def getBreakTimes(self):
        return self._breakTimes

    # Updates the break times in the schedule
    def updateBreaks(self):
        # Add in the break times
        for breakTime in self._breakTimes:
            for i in range(0, self._staticAppInfo.getBreakInterval()):
                thisTime = Time().setTimeWithMinutes(
                    breakTime.getMinutes() + i * self._staticAppInfo.getTimeInterval()
                )
                for scheduleTime in self._schedule:
                    if scheduleTime.equals(thisTime):
                        self._schedule[scheduleTime] = (
                            self._staticAppInfo.getBreakCode()
                        )

    # Adds a break to the list
    # NOTE: Breaks must be assigned in increasing order
    def addBreakTime(self, givenTime):
        for breakTime in self._breakTimes:
            if breakTime.equals(givenTime):
                print("ERROR IN LIFEGUARD - DUPLICATE TIME IN ADD BREAK TIME")
                return -1
        self._breakTimes.append(givenTime)
        self.updateBreaks()
        return 0

    # Sets the id number of the lifeguard
    def setIdNum(self, num):
        if isinstance(num, int):
            self._id = num

    # Returns the id number of the lifeguard
    def getIdNum(self):
        return self._id

    # Return the shift start time
    def getShiftStartTime(self):
        return self._startTime

    # Return the shift end time
    def getShiftEndTime(self):
        return self._endTime

    # Returns the range of possible break times in the form of a list with two values, start and end
    def calculateRangeOfPossibleBreakTimes(self):
        # Check to see if a manuel break will be needed (If there is quit)
        if self._manuelBreak:
            print("ERROR I HAVEN'T CODED THIS YET")
            return [Time(), Time()]

        # Otherwise continue the algorithm
        earliestTime = Time().setTimeWithMinutes(
            self._endTime.getMinutes()
            - self._staticAppInfo.getLongestTimeWorking()
            - self._staticAppInfo.getBreakTime()
        )
        latestTime = Time().setTimeWithMinutes(
            self._startTime.getMinutes() + self._staticAppInfo.getLongestTimeWorking()
        )
        return [earliestTime, latestTime]

    # Returns whether the lifeguard is working during that time
    def isWorking(self, thisTime):
        if not isinstance(thisTime, Time):
            return False
        if self.isOnBreak(thisTime):
            return False
        return thisTime.getIsInBetweenExclusiveEnd(self._startTime, self._endTime)

    # Returns whether the lifeguard is on break at the given time
    def isOnBreak(self, givenTime):
        if not isinstance(givenTime, Time):
            return False
        for thisTime in self._breakTimes:
            if givenTime.getIsInBetweenExclusiveEnd(
                thisTime,
                Time().setTimeWithMinutes(
                    thisTime.getMinutes() + self._staticAppInfo.getBreakTime()
                ),
            ):
                return True
        return False

    # Returns whether the lifeguard is on shift or not
    def isOnShift(self, thisTime):
        if isinstance(thisTime, Time):
            return thisTime.getIsInBetweenExclusiveEnd(self._startTime, self._endTime)
        print("ERROR IN LIFEGUARD - isOnShift")
        return False

    # Returns how many breaks the lifeguard has
    def getNumBreaks(self):
        return self._numBreaks

    # Resets the lifeguard
    def resetLifeguardSchedule(self):
        self._breakTimes = []

        # Reset the schedule dictionary
        self._schedule = dict()
        for t in range(
            self._startTime.getMinutes(),
            self._endTime.getMinutes(),
            self._staticAppInfo.getTimeInterval(),
        ):
            # Create the time object
            thisTime = Time().setTimeWithMinutes(t)
            self._schedule[thisTime] = self._staticAppInfo.getEmptyCode()

        self.resetRandomChance()

    def getUpStandsFromTime(self, givenTime: Time, upStands: list[Stand]) -> int:
        stand = self.getStand(givenTime)

        if stand is None:
            return -1  # error code

        upStandNames = Stand.getStandNames(upStands)
        upStandNames.append(self._staticAppInfo.getUpStandCode())

        count = 0
        while stand is not None and stand in upStandNames:
            stand = self.getStand(
                Time().setTimeWithMinutes(
                    givenTime.getMinutes()
                    + self._staticAppInfo.getTimeInterval() * (count + 1)
                )
            )

            count += 1

        return count

    def convertScheduleToUp(self, upStands: list[Stand]):
        upStandNames = Stand.getStandNames(upStands)

        for scheduleTime in self._schedule:
            if self._schedule[scheduleTime] in upStandNames:
                self._schedule[scheduleTime] = self._staticAppInfo.getUpStandCode()

    def getIsUpOnStand(self, givenTime: Time, upStands: list[Stand]) -> bool:
        stand = self.getStand(givenTime)

        upStandNames = Stand.getStandNames(upStands)
        upStandNames.append(self._staticAppInfo.getUpStandCode())

        return stand in upStandNames

#import libraries
import math
from Time import Time
from StaticAppInfo import StaticAppInfo

#This object represents the aspects of a lifeguard
class Lifeguard:

    #Initialize lifeguard
    def __init__(self,
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

        #Initialize name
        self._name = name

        #Initialize idNum
        self._id = idNum

        #Initialize staticAppInfo
        if isinstance(staticAppInfo, StaticAppInfo):
            self._staticAppInfo = staticAppInfo
        else:
            self._staticAppInfo = StaticAppInfo("ERROR")
            print("ERROR, STATIC APP INFO NOT INITIALIZED")

        #Initialize break times
        if breakTimes is None:
            self._breakTimes = []
        else:
            self._breakTimes = breakTimes

        #Calculate the amount of breaks needed for a shift of the given length
        self._numBreaks = math.ceil(
            (self._endTime.getMinutes() -
             self._startTime.getMinutes() +
             self._staticAppInfo.getBreakTime()) / (self._staticAppInfo.getLongestTimeWorking() +
                                                    self._staticAppInfo.getBreakTime()) - 1
                                    )
        #Set the manuel break to true or false depending on numBreaks
        self._manuelBreak = False
        if self._numBreaks > 1:
            self._manualBreak = True

        #Create a dictionary where the key is the time and the stand is the value
        self._schedule = dict()
        #Assign every time in the lifeguard schedule to NA
        for t in range(self._startTime.getMinutes(), self._endTime.getMinutes(), self._staticAppInfo.getTimeInterval()):
            #Create the time object
            time = Time().setTimeWithMinutes(t)
            self._schedule[time] = "EMPTY"
        self.updateBreaks()

        #Initialize random chance selections to 0
        self._randomChance = dict()
        self.resetRandomChance()

    #Swap the random chances going back to a certain time starting at a certain time with another lifeguard
    def swapRandomChances(self, otherLifeguard, backTime, currentTime):

        #Check type
        if (not isinstance(otherLifeguard, Lifeguard) or
        not isinstance(backTime, Time) or
        not isinstance(currentTime, Time)):
            print("ERROR IN LIFEGUARD - sRC")
            return

        #Get the random chance dictionary of the other lifeguard
        otherRandomChance = otherLifeguard.getRandomChanceFullDictionary()

        #Swap the values between the two times given
        for t in range(backTime.getMinutes(), currentTime.getMinutes(), self._staticAppInfo.getTimeInterval()):
            timeBeingAnalyzed = Time().setTimeWithMinutes(t)
            otherTime = Time()
            for time in otherRandomChance:
                if time.equals(timeBeingAnalyzed):
                    otherTime = time
            thisTime = Time()
            for time in self._randomChance:
                if time.equals(timeBeingAnalyzed):
                    thisTime = time
            tempRandomChanceValue = otherRandomChance[otherTime]
            otherRandomChance[otherTime] = self._randomChance[thisTime]
            self._randomChance[thisTime] = tempRandomChanceValue


    #Returns the random chance dictionary of this lifeguard
    def getRandomChanceFullDictionary(self):
        return self._randomChance

    #Adds one to random chance
    def incrementRandomChance(self, currentTime):
        for time in self._randomChance:
            if time.equals(currentTime):
                self._randomChance[time] = 1

    #Resets the random chance
    def resetRandomChance(self):
        self._randomChance = dict()
        for t in range(self._startTime.getMinutes(),
                       self._endTime.getMinutes(),
                       self._staticAppInfo.getTimeInterval()):
            time = Time().setTimeWithMinutes(t)
            self._randomChance[time] = 0

    #Returns the random chance
    def getRandomChance(self, currentTime):
        count = 0
        if isinstance(currentTime, Time):
            for time in self._randomChance:
                if time.getMinutes() < currentTime.getMinutes():
                    count += self._randomChance[time]
        else:
            print("ERROR IN LIFEGUARD - gRC")
        return count


    #Returns how long the lifeguard has been up on stand given the time
    def getIntervalsUpOnStand(self, time):

        #Check the type of the parameter
        if isinstance(time, Time):

            #Get the index of the time given in self._schedule keys
            index = None
            scheduleTimes = list(self._schedule.keys())
            for i in range(0, len(scheduleTimes)):
                if scheduleTimes[i].equals(time):
                    index = i
            #If the index is not assigned then the time given is invalid
            if index is None:
                return -1

            #Get the upStands list
            upStands = list(list(self._staticAppInfo.getEventDataSpecific("stand").values())[0].keys())

            #Count how many stands in the current schedule prior to the given time are up stands
            count = 0
            i = 1
            while index - i >= 0 and self._schedule[scheduleTimes[index - i]] in upStands:
                count += 1
                i += 1

            #Return the value of count
            return count

        #Print error message and return a bad number
        print("ERROR IN LIFEGUARD - gIPOS wrong type")
        return -1

    #Returns the lifeguard's name
    def getName(self):
        return self._name

    #Swaps schedules up in a certain time frame with another lifeguard
    def swapSchedulesBetweenTimes(self, otherLifeguard, backTime, currentTime):

        #Check type
        if (not isinstance(otherLifeguard, Lifeguard) or
        not isinstance(backTime, Time) or
        not isinstance(currentTime, Time)):
            print("ERROR IN LIFEGUARD - sSBT")
            return

        #Get the other schedule dictionary from the other lifeguard
        otherScheduleDictionary = otherLifeguard.getSchedule()

        #Iterate through and swap each stand at each location between back time and current time
        for t in range(backTime.getMinutes(), currentTime.getMinutes(), self._staticAppInfo.getTimeInterval()):

            #Get the keys for the two dictionaries
            timeBeingAnalyzed = Time().setTimeWithMinutes(t)
            otherTime = Time()
            for time in otherScheduleDictionary:
                if time.equals(timeBeingAnalyzed):
                    otherTime = time
            thisTime = Time()
            for time in self._schedule:
                if time.equals(timeBeingAnalyzed):
                    thisTime = time

            #Swap the values
            tempStandValue = otherScheduleDictionary[otherTime]
            otherScheduleDictionary[otherTime] = self._schedule[thisTime]
            self._schedule[thisTime] = tempStandValue

    #Swaps schedules with another lifeguard
    def swapSchedules(self, otherLifeguard):
        if isinstance(otherLifeguard, Lifeguard):
            tempSchedule = otherLifeguard.getSchedule()
            otherLifeguard.setSchedule(self._schedule)
            otherLifeguard.updateBreaks()
            self._schedule = tempSchedule
            self.updateBreaks()
        else:
            print("ERROR IN LIFEGUARD - SWAP SCHEDULE")

    #Swap at a specific time in the schedule with another lifeguard
    def swapSingularStandAtTime(self, otherLifeguard, currentTime):
        if isinstance(currentTime, Time) and isinstance(otherLifeguard, Lifeguard):
            tempStand = otherLifeguard.getStand(currentTime)
            otherLifeguard.addStand(currentTime, self.getStand(currentTime))
            self.addStand(currentTime, tempStand)
        else:
            print("ERROR IN LIFEGUARD - sSTAT")

    #Sets the schedule outright - CHECK FORMAT OUTSIDE OF THIS FUNCTION
    def setSchedule(self, schedule):
        self._schedule = schedule

    #Returns the schedule dictionary
    def getSchedule(self):
        return self._schedule

    #Returns the stand at a certain time
    def getStand(self, time):
        if isinstance(time, Time):
            for scheduleTime in self._schedule:
                if scheduleTime.equals(time):
                    return self._schedule[scheduleTime]
        else:
            print("ERROR IN LIFEGUARD - GET STAND")
        return ""

    #Adds a stand to the lifeguard's schedule at a certain time
    def addStand(self, time, standName):
        if isinstance(time, Time) and isinstance(standName, str):
            for scheduleTime in self._schedule:
                if scheduleTime.equals(time):
                    self._schedule[scheduleTime] = standName
                    return scheduleTime
            print("ERROR IN LIFEGUARD - ADD STAND TIME NOT FOUND")
        else:
            print("ERROR IN LIFEGUARD - ADD STAND")
        return Time()

    #Returns the break times list
    def getBreakTimes(self):
        return self._breakTimes

    #Updates the break times in the schedule
    def updateBreaks(self):
        #Add in the break times
        for breakTime in self._breakTimes:
            for i in range(0, self._staticAppInfo.getBreakInterval()):
                time = Time().setTimeWithMinutes(breakTime.getMinutes() + i * self._staticAppInfo.getTimeInterval())
                for scheduleTime in self._schedule:
                    if scheduleTime.equals(time):
                        self._schedule[scheduleTime] = "BREAK"

    #Adds a break to the list
    def addBreakTime(self, givenTime):
        for breakTime in self._breakTimes:
            if breakTime.equals(givenTime):
                print("ERROR IN LIFEGUARD - DUPLICATE TIME IN ADD BREAK TIME")
                return -1
        self._breakTimes.append(givenTime)
        self.updateBreaks()

    #Sets the id number of the lifeguard
    def setIdNum(self, num):
        if isinstance(num, int):
            self._id = num

    #Returns the id number of the lifeguard
    def getIdNum(self):
        return self._id


    #Return the shift start time
    def getShiftStartTime(self):
        return self._startTime

    #Return the shift end time
    def getShiftEndTime(self):
        return self._endTime

    #Returns the range of possible break times in the form of a list with two values, start and end
    def calculateRangeOfPossibleBreakTimes(self):

        #Check to see if a manuel break will be needed (If there is quit)
        if self._manuelBreak:
            print("ERROR I HAVEN'T CODED THIS YET")
            return [Time(), Time()]

        #Otherwise continue the algorithm
        earliestTime = Time().setTimeWithMinutes(self._endTime.getMinutes() -
                                                 self._staticAppInfo.getLongestTimeWorking() -
                                                 self._staticAppInfo.getBreakTime())
        latestTime = Time().setTimeWithMinutes(self._startTime.getMinutes() +
                                                 self._staticAppInfo.getLongestTimeWorking())
        return [earliestTime, latestTime]


    #Returns whether the lifeguard is working during that time
    def isWorking(self, time):
        if not isinstance(time, Time):
            return False
        if self.isOnBreak(time):
            return False
        return time.getIsInBetweenExclusiveEnd(self._startTime, self._endTime)

    #Returns whether the lifeguard is on break at the given time
    def isOnBreak(self, givenTime):
        if not isinstance(givenTime, Time):
            return False
        for time in self._breakTimes:
            if givenTime.getIsInBetweenExclusiveEnd(time,
                                                    Time().setTimeWithMinutes(time.getMinutes() +
                                                                                    self._staticAppInfo.getBreakTime())
                                                    ):
                return True
        return False

    #Returns whether the lifeguard is on shift or not
    def isOnShift(self, time):
        if isinstance(time, Time):
            return time.getIsInBetweenExclusiveEnd(self._startTime, self._endTime)
        print("ERROR IN LIFEGUARD - isOnShift")
        return False

    #Returns how many breaks the lifeguard has
    def getNumBreaks(self):
        return self._numBreaks
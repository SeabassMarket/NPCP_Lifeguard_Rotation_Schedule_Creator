#import libraries
from Lifeguard import Lifeguard
import random
from Stand import Stand
from StaticAppInfo import StaticAppInfo
from Time import Time

#This object will be used to calculate and organize different data
class CalculateSchedule:

    #Initialize object
    def __init__(self,
                 staticAppInfo):

        #Initialize staticAppInfo
        if isinstance(staticAppInfo, StaticAppInfo):
            self._staticAppInfo = staticAppInfo
        else:
            self._staticAppInfo = StaticAppInfo("ERROR")
            print("ERROR, STATIC APP INFO NOT INITIALIZED")

        #Get lifeguardData from staticAppInfo
        lifeguardData = self._staticAppInfo.getEventDataSpecific("lifeguard")

        #Create lifeguard objects
        for lifeguardKey in lifeguardData:
            self._lifeguards = []
            lifeguards = lifeguardData[lifeguardKey]
            count = 0
            for lifeguard in lifeguards:
                self._lifeguards.append(Lifeguard(shiftTimes=lifeguards[lifeguard],
                                                  name=lifeguard,
                                                  idNum=count,
                                                  staticAppInfo=self._staticAppInfo
                                                  ))
                count += 1

        #Get stand date from staticAppInfo
        standData = self._staticAppInfo.getEventDataSpecific("stand")
        #Up stands
        upStandData = list(standData.values())[0]
        self._upStands = []
        for stand in upStandData:
            newStand = Stand(name=stand,
                             standType=list(standData.keys())[0],
                             startTime=upStandData[stand][0],
                             endTime=upStandData[stand][1],
                             amountPerInterval=upStandData[stand][2])
            self._upStands.append(newStand)
        #Timely down stands
        timelyDownStandData = list(standData.values())[1]
        self._timelyDownStands = []
        for stand in timelyDownStandData:
            newStand = Stand(name=stand,
                             standType=list(standData.keys())[1],
                             startTime=timelyDownStandData[stand][0],
                             endTime=timelyDownStandData[stand][1],
                             amountPerInterval=timelyDownStandData[stand][2])
            self._timelyDownStands.append(newStand)
        #Priority down stands
        priorityDownStandData = list(standData.values())[2]
        self._priorityDownStands = []
        for stand in priorityDownStandData:
            newStand = Stand(name=stand,
                             standType=list(standData.keys())[2],
                             isAllDay=True,
                             startTime=priorityDownStandData[stand][0],
                             endTime=priorityDownStandData[stand][1],
                             amountPerInterval=priorityDownStandData[stand][2])
            self._priorityDownStands.append(newStand)
        #Fill-in down stands
        fillInDownStandData = list(standData.values())[3]
        self._fillInDownStands = []
        for stand in fillInDownStandData:
            newStand = Stand(name=stand,
                             standType=list(standData.keys())[3],
                             isAllDay=True,
                             startTime=fillInDownStandData[stand][0],
                             endTime=fillInDownStandData[stand][1])
            self._fillInDownStands.append(newStand)

        #Initialize the breaks instance variable
        self._breaks = []

    #Calculate the schedule itself by creating each schedule for each lifeguard
    def calculateSchedule(self):

        #Get the time range of when the pool is open
        timeRange = self.calculatePoolOpenTimeRange()
        earliestTime = timeRange[0]
        latestTime = timeRange[1]

        #For each time between the earliest time and the latest time (excluding latest)
        for t in range(earliestTime.getMinutes(), latestTime.getMinutes(), self._staticAppInfo.getTimeInterval()):

            #Create a time object for this iteration/current time being observed
            currentTime = Time().setTimeWithMinutes(t)

            #Assign the up stands for the lifeguards
            self.assignUpStandsAtTime(currentTime)

            #Assign the timely down stands
            self.assignTimelyDownStandsAtTime(currentTime)

            #Assign the priority down stands
            self.assignPriorityDownStandsAtTime(currentTime)

            #Assign the fill-in down stands
            self.assignFillInDownStandsAtTime(currentTime)

            #Swap shifts in case someone is starting a break next to optimize stand up intervals

            #Create a list of lifeguards going on break at the next time interval
            nextTime = Time().setTimeWithMinutes(currentTime.getMinutes() + 20)
            lifeguardsStartingBreakNext = self.getLifeguardsStartingBreak(nextTime)

    #Assigns the fill-in down stands to lifeguards at a given time
    def assignFillInDownStandsAtTime(self, currentTime):

        # Continue if time is actually a time
        if isinstance(currentTime, Time):
            self._staticAppInfo.getTimeInterval()
            pass
        else:
            print("ERROR IN CALCULATE SCHEDULE - aFIDSAT")

    #Assigns the priority down stands to lifeguards at a given time
    def assignPriorityDownStandsAtTime(self, currentTime):

        # Continue if time is actually a time
        if isinstance(currentTime, Time):
            self._staticAppInfo.getTimeInterval()
            pass
        else:
            print("ERROR IN CALCULATE SCHEDULE - aPDSAT")

    #Assigns the timely down stands to lifeguards at a given time
    def assignTimelyDownStandsAtTime(self, currentTime):

        # Continue if time is actually a time
        if isinstance(currentTime, Time):
            self._staticAppInfo.getTimeInterval()
            pass
        else:
            print("ERROR IN CALCULATE SCHEDULE - aTDSAT")

    #Assigns the up stands to lifeguards at a given time
    def assignUpStandsAtTime(self, currentTime):

        #Continue if time is actually a time
        if isinstance(currentTime, Time):

            #Create a list with all the lifeguards working at this time
            lifeguardsWorkingAtTime = self.getLifeguardsWorkingAtASpecificTime(currentTime)

            #Get the up stands for this time
            upStandsAtTime = self.getStandsOpenAtTime(currentTime, self._upStands)

            #Calculate the amount of iterations necessary
            numIterations = min([len(upStandsAtTime), len(lifeguardsWorkingAtTime)])

            #Assign the stands to lifeguards based on:
            #1 those who have the lowest intervals up on stand
            #2 who has the shortest time left in their shift
            #3 those who have been selected for random chance the least
            #4 random chance
            for i in range (0, numIterations):

                '''CHOOSE STAND TO ADD'''
                #Get the stand that we are going to be adding and pop it too
                standToAdd = upStandsAtTime.pop(upStandsAtTime.index(random.choice(upStandsAtTime)))

                '''CREATE THE TEMP LIFEGUARD LIST THAT WILL BE TORN APART AS WE GO THROUGH'''
                # Create a duplicate list of the lifeguards that we can tear apart as we qualify lifeguards
                tempLifeguards = []
                for lifeguard in lifeguardsWorkingAtTime:
                    tempLifeguards.append(lifeguard)

                '''HERE WE CHECK WHO HAS THE LOWEST INTERVALS ON STAND (ALGORITHM #1)'''
                # Get a list of how much each lifeguard that is working at this time has been up on stand
                intervalsUpOnStand = []
                for lifeguard in tempLifeguards:
                    intervalsUpOnStand.append(lifeguard.getIntervalsUpOnStand(currentTime))


                #First figure out if we can use the minimum intervals method and get the lifeguard who would apply for '
                # this method
                tieBreaker = False
                minimum = min(intervalsUpOnStand)
                # Get all the values with the minimum and pop the lifeguards who don't have the minimum
                for j in range(len(intervalsUpOnStand) - 1, -1, -1):
                    if intervalsUpOnStand[j] != minimum:
                        tempLifeguards.pop(j)
                        intervalsUpOnStand.pop(j)
                # Continue to tie-breaker if we're going to need it
                if len(tempLifeguards) > numIterations - i:
                    tieBreaker = True

                # Set the index
                index = intervalsUpOnStand.index(minimum)
                lifeguard = tempLifeguards[index]
                index = lifeguardsWorkingAtTime.index(lifeguard)
                message = "INTERVALS UP ON STAND USED ON"

                '''HERE WE CHECK WHO HAS THE SHORTEST TIME LEFT ON THEIR SHIFT (ALGORITHM #2)'''
                # Figure out if we can use the shortest time left method if the last one didn't work
                if tieBreaker:

                    # Get a list of all the end shift times of the lifeguards working at this time
                    lifeguardEndShiftTimes = []
                    for lifeguard in tempLifeguards:
                        lifeguardEndShiftTimes.append(lifeguard.getShiftEndTime().getMinutes())

                    #Check eligibility of the second picking algorithm and get the lifeguard who would apply for this
                    tieBreaker = False
                    minimum = min(lifeguardEndShiftTimes)
                    #Get all the values with the minimum and pop the lifeguards who don't have the minimum
                    for j in range(len(lifeguardEndShiftTimes) - 1, -1, -1):
                        if lifeguardEndShiftTimes[j] != minimum:
                            tempLifeguards.pop(j)
                            lifeguardEndShiftTimes.pop(j)
                    #Continue to tie-breaker if we're going to need it
                    if len(tempLifeguards) > numIterations - i:
                        tieBreaker = True

                    # Set the index
                    index = lifeguardEndShiftTimes.index(minimum)
                    lifeguard = tempLifeguards[index]
                    index = lifeguardsWorkingAtTime.index(lifeguard)
                    message = "TIME LEFT IN SHIFT USED ON"

                '''HERE WE CHECK WHO HAS THE LEAST AMOUNT OF RANDOM CHANCES (ALGORITHM #3)'''
                # Figure out if we can use the least amount of random chances method if the last one didn't work
                if tieBreaker:

                    # Get a list of all the random chances of the lifeguards working at this time
                    lifeguardRandomChances = []
                    for lifeguard in tempLifeguards:
                        lifeguardRandomChances.append(lifeguard.getRandomChance())

                    # Check eligibility of the second picking algorithm
                    tieBreaker = False
                    minimum = min(lifeguardRandomChances)
                    #Get all the values with the minimum and pop the lifeguards who don't have the minimum
                    for j in range(len(lifeguardRandomChances) - 1, -1, -1):
                        if lifeguardRandomChances[j] != minimum:
                            tempLifeguards.pop(j)
                            lifeguardRandomChances.pop(j)
                    #Continue to tie-breaker if we're going to need it
                    if len(lifeguardRandomChances) > numIterations - i:
                        tieBreaker = True

                    # Set the index
                    index = lifeguardRandomChances.index(minimum)
                    lifeguard = tempLifeguards[index]
                    index = lifeguardsWorkingAtTime.index(lifeguard)
                    message = "RANDOM CHANCE USED ON"

                '''RANDOMLY PICK AN INDEX FOR THE LIFEGUARD IF ALL ELSE FAILS (ALGORITHM #4)'''
                #If there is no tie-breaker, assign using the lowest interval algorithm
                if tieBreaker: #If there is a tie-breaker, finally just use random chance

                    #Randomly select a lifeguard
                    index = random.randint(a=0, b=len(tempLifeguards) - 1)
                    lifeguard = tempLifeguards[index]
                    lifeguard.incrementRandomChance()
                    index = lifeguardsWorkingAtTime.index(lifeguard)
                    message = "COMPLETELY RANDOM CHANCE USED ON"

                '''FINALLY ASSIGN THE STAND'''
                lifeguard = lifeguardsWorkingAtTime.pop(index)
                lifeguard.addStand(time=currentTime, standName=standToAdd)

                #Print info to help with testing
                '''
                self.printSchedule()
                print(currentTime.get12Time() + " - " + message + " " + str(lifeguard.getIdNum()), end="")
                input()
                print()'''

            #Reorganize the assigned stands if needed
            self.reorganizeLifeguards(currentTime)

        else:
            print("ERROR IN CALCULATE SCHEDULE - aUSAT")

    #Reorganizes stands so that lifeguards aren't on the same stand or something
    def reorganizeLifeguards(self, currentTime):

        #Check to make sure current time is a time
        if isinstance(currentTime, Time):

            #First, create a list with all the lifeguards working at this time again
            lifeguardsWorkingAtTime = self.getLifeguardsWorkingAtASpecificTime(currentTime)

            #Get the previous time
            if currentTime.getMinutes() - self._staticAppInfo.getTimeInterval() < 0:
                print("error-ish in calculate schedule - aUSAT previous time")
                return "Previous time not evaluated"
            previousTime = Time().setTimeWithMinutes(currentTime.getMinutes() - self._staticAppInfo.getTimeInterval())

            #Get a list of the lifeguard working at the last time
            lifeguardsWorkingAtLastTime = self.getLifeguardsWorkingAtASpecificTime(previousTime)

            # Get a list of all the up stands
            upStandNames = []
            for stand in self._upStands:
                upStandNames.append(stand.getName())

            #Snip both lifeguard lists so that they only include the lifeguards on up stands
            for i in range(len(lifeguardsWorkingAtTime) - 1, -1, -1):
                if not lifeguardsWorkingAtTime[i].getStand(currentTime) in upStandNames:
                    lifeguardsWorkingAtTime.pop(i)
            for i in range(len(lifeguardsWorkingAtLastTime) - 1, -1, -1):
                if not lifeguardsWorkingAtLastTime[i].getStand(previousTime) in upStandNames:
                    lifeguardsWorkingAtLastTime.pop(i)

            #Get the overlap between the two lists
            lifeguardsUpOnStandBeforeAndNow = []
            for lifeguard in lifeguardsWorkingAtTime:
                if lifeguard in lifeguardsWorkingAtLastTime:
                    lifeguardsUpOnStandBeforeAndNow.append(lifeguard)

            #Create two lists where each list is the stands that the lifeguards are on
            upStandBefore = []
            upStandNow = []
            for lifeguard in lifeguardsUpOnStandBeforeAndNow:
                upStandBefore.append(lifeguard.getStand(previousTime))
                upStandNow.append(lifeguard.getStand(currentTime))

            #Print that there is an issue if the lifeguard is on the same up stand twice
            for i in range(0, len(lifeguardsUpOnStandBeforeAndNow)):
                if upStandNow[i] == upStandBefore[i]:
                    print("DUPLICATE STANDS DETECTED:", previousTime.get12Time(), "-", currentTime.get12Time(), upStandNow[i])

            #Reorganize the stands by taking the two lists, matching up the values, and then changing the index by one
            #so that every lifeguard is guaranteed a unique stand
            print(upStandBefore)
            print(upStandNow)
            for i in range(0, len(upStandBefore)):
                if upStandBefore[i] in upStandNow:
                    index = 0
                    for j in range(0, len(upStandNow)):
                        if upStandBefore[i] == upStandNow[j]:
                            index = j
                    temp = upStandNow[i]
                    upStandNow[i] = upStandNow[index]
                    upStandNow[index] = temp
            print(upStandBefore)
            print(upStandNow)

        else:
            print("ERROR IN CALCULATE SCHEDULE - rL")

    #Returns a list with the stands that are open at that time (works for both up stands and downs stands)
    @staticmethod
    def getStandsOpenAtTime(time, standList):

        #Create the list where the stands are going to be appended to
        standsToReturn = []

        #Check to make sure the time is a time
        if isinstance(time, Time):
            for stand in standList:
                if stand.isOpen(time):
                    for i in range(0, stand.getAmountPerInterval()):
                        standsToReturn.append(stand.getName())
        else:
            print("ERROR IN CALCULATE SCHEDULE - gSOAT")

        #Return the created list
        return standsToReturn

    #Gets a list of the lifeguards going on break right now
    def getLifeguardsStartingBreak(self, time):

        #Create list
        lifeguardsStartingBreak = []

        #Continue if the type of the parameter time is correct
        if isinstance(time, Time):
            #For each lifeguard, check if one of the break times is the given time
            for lifeguard in self._lifeguards:
                for breakTime in lifeguard.getBreakTimes():
                    if breakTime.equals(time):
                        lifeguardsStartingBreak.append(lifeguard)
        else: #Print error if the type of time is wrong
            print("ERROR IN CALCULATE SCHEDULE - gLSB")

        #Return the list
        return lifeguardsStartingBreak

    #Sorts the lifeguards in increasing order of their shift start times
    def sortLifeguards(self):

        #Create a list that directly corresponds to the lifeguards of the times of shift starts and ends
        shiftStartAndEnds = []
        for lifeguard in self._lifeguards:
            shiftStartAndEnds.append([lifeguard.getShiftStartTime(), lifeguard.getShiftEndTime()])

        #Sort the times and, by doing so, the lifeguards
        for i in range(0, len(self._lifeguards)):

            #Create the minimum index
            minIndex = i
            #For each lifeguard
            for j in range(i, len(self._lifeguards)):
                #If the shift start times are equal we use the tiebreaker
                # noinspection PyUnresolvedReferences
                if shiftStartAndEnds[j][0].getMinutes() == shiftStartAndEnds[minIndex][0].getMinutes():
                    #Tiebreaker is whoever has the early end time is the minimum
                    # noinspection PyUnresolvedReferences
                    if shiftStartAndEnds[j][1].getMinutes() < shiftStartAndEnds[minIndex][1].getMinutes():
                        minIndex = j
                #If the shift start time at j is less than our current minimum, j is the new minimum
                # noinspection PyUnresolvedReferences
                elif shiftStartAndEnds[j][0].getMinutes() < shiftStartAndEnds[minIndex][0].getMinutes():
                    minIndex = j


            #Swap in both the lifeguard and the time lists
            tempLifeguard = self._lifeguards[i]
            self._lifeguards[i] = self._lifeguards[minIndex]
            self._lifeguards[minIndex] = tempLifeguard
            tempList = shiftStartAndEnds[i]
            shiftStartAndEnds[i] = shiftStartAndEnds[minIndex]
            shiftStartAndEnds[minIndex] = tempList

    #Assigns the created breaks to lifeguards. The parameter is for if we are using hardcoded breaks
    def assignBreaks(self, breaks=None):

        #Automatically calculate the breaks if breaks are not explicitly given
        if breaks is None:
            self.calculateBreaks()
        else:
            self._breaks = breaks

        #Get the lifeguards that actually need breaks (NOTE: IS SORTED)
        lifeguardsWithBreaks = self.getLifeguardsWithBreaks()

        #Create a list for lifeguards if they just didn't get a break
        lifeguardsNeedingBreaks = []

        #For each lifeguard, assign the breaks
        for i in range(0, len(lifeguardsWithBreaks)):
            timeRange = lifeguardsWithBreaks[i].calculateRangeOfPossibleBreakTimes()
            earliestTime = timeRange[0]
            latestTime = timeRange[1]
            if self._breaks[i].getIsInBetweenInclusive(earliestTime, latestTime):
                lifeguardsWithBreaks[i].addBreakTime(self._breaks[i])
            else:
                lifeguardsNeedingBreaks.append(lifeguardsWithBreaks[i])

        #Assign the best possible breaks for lifeguards who the previous algorithm didn't work for
        self.calculateAndAssignLeftoverBreaks(lifeguardsNeedingBreaks)

    #Calculates and assigns the breaks for the lifeguards which the previous algorithm didn't work for
    def calculateAndAssignLeftoverBreaks(self, lifeguardsNeedingBreaks):

        #For each lifeguard in the given list
        for lifeguard in lifeguardsNeedingBreaks:

            # Get the dictionary with all the scores for the lifeguards at each time
            lifeguardsAtTime = self.getLifeguardsOnDutyDict()

            #Get the ratio dictionary
            lifeguardStandRatios = self.getLifeguardToStandRatios(lifeguardsAtTime)

            #Get the time that has the highest ratio of lifeguards scores to stands
            timeWithHighestRatio = self._staticAppInfo.findDictMax(lifeguardStandRatios)

            #Keep on generating times until the time with the highest ratio is within the break range for this specific
            #lifeguard
            #Get the two times for the range
            earliestTime = lifeguard.calculateRangeOfPossibleBreakTimes()[0]
            latestTime = lifeguard.calculateRangeOfPossibleBreakTimes()[1]
            #While it is still invalid
            while not timeWithHighestRatio.getIsInBetweenInclusive(earliestTime, latestTime):
                #Pop out the bad time
                lifeguardStandRatios.pop(timeWithHighestRatio)
                #Recalculate
                timeWithHighestRatio = self._staticAppInfo.findDictMax(lifeguardStandRatios)

            #Now with the confirmed best time, assign the break
            lifeguard.addBreakTime(timeWithHighestRatio)
            print("Leftover algorithm used on lifeguard", lifeguard.getName())

    #Calculates the breaks based on the lifeguard information
    def calculateBreaks(self):

        #List of prospective breaks to give to lifeguards
        breaks = []

        #Create a dictionary of times with the amount of lifeguards at each time
        lifeguardsAtTime = self.getLifeguardsOnDutyDict()
        possibleBreakRange = self.calculateBreakRange()
        self._staticAppInfo.clipDictionaryToTimeRange(lifeguardsAtTime, possibleBreakRange)

        #Create a new list with the lifeguards to make sure that they all actually need breaks
        lifeguardsWithBreaks = self.getLifeguardsWithBreaks()

        #For one iteration per lifeguard
        for i in range(0, len(lifeguardsWithBreaks)):

            #Create a new dictionary where the key is the time and the value is the lifeguards at the time divided
            #by the amount of up stands present
            lifeguardStandRatios = self.getLifeguardToStandRatios(lifeguardsAtTime)

            #Get the time that has the highest ratio of lifeguards scores to stands
            timeWithHighestRatio = self._staticAppInfo.findDictMax(lifeguardStandRatios)
            breaks.append(timeWithHighestRatio)

            #Remove one lifeguard working from the time found to assign the break as well as the times the
            #break will bleed into
            self.reduceLifeguardScore(lifeguardsAtTime, timeWithHighestRatio)

        #Sort the break times
        self._staticAppInfo.sortTimesAscending(breaks)

        #Set the breaks
        self._breaks = breaks

    #Calculates the range of time when breaks are actually feasible throughout the day
    def calculateBreakRange(self):

        #Establish two times, earliest time and latest time
        earliestTime = Time()
        latestTime = Time()

        firstTime = True
        #For each lifeguard in lifeguards, check to see the earliest and latest times
        for lifeguard in self._lifeguards:

            #Get the two times, earliest and latest
            time1 = lifeguard.calculateRangeOfPossibleBreakTimes()[0]
            time2 = lifeguard.calculateRangeOfPossibleBreakTimes()[1]

            #Check if these are the extremes or simply just the first time
            if time1.getMinutes() < earliestTime.getMinutes() or firstTime:
                earliestTime = time1
            if time2.getMinutes() > latestTime.getMinutes() or firstTime:
                latestTime = time2
            firstTime = False

        #Return the created list of the two times
        return [earliestTime, latestTime]

    #Creates a dictionary where the key is the time and the value is the lifeguards working / the amount of up stands
    def getLifeguardToStandRatios(self, lifeguardsAtTime):

        #Create the dictionary
        lifeguardStandRatios = dict()

        #Get the amount of up stands at each time and create a dictionary
        standsAtTime = self.getUpStandsAtTimeDict()

        #For each time in lifeguards at time, create the values of the dictionary
        for time in lifeguardsAtTime:
            #Create time for the key of the ratio
            ratioKeyTime = Time().setTimeWithMinutes(time.getMinutes())

            #Find the equivalent key in standsAtTime
            standKeyTime = Time()
            for standTime in standsAtTime:
                if standTime.equals(time):
                    standKeyTime = standTime
            if standsAtTime[standKeyTime] == 0:
                lifeguardStandRatios[ratioKeyTime] = 0
            else:
                lifeguardStandRatios[ratioKeyTime] = lifeguardsAtTime[time] / standsAtTime[standKeyTime]

        return lifeguardStandRatios

    #Returns a dictionary with the amount of up stands at every time of the day
    def getUpStandsAtTimeDict(self):

        #Create the dictionary
        upStandsAtTimeDict = dict()

        #For each time of the day record the amount of up stands
        for i in range(0, 1440, self._staticAppInfo.getTimeInterval()):

            #Initialize count to 0
            count = 0

            #Set the time being used for the key
            time = Time().setTimeWithMinutes(i)

            #For each stand in upStandData, check to see if it is open at the given time
            for stand in self._upStands:

                #Get the times of the start and end of the stand
                time1 = stand.getStartTime()
                time2 = stand.getEndTime()

                #Increase count by 1 if the current time is between the start and end of the time
                if time.getIsInBetweenExclusiveEnd(time1, time2):
                    count += 1

            #Set the dictionary value with its proper key
            upStandsAtTimeDict[time] = count

        #Return the created dictionary
        return upStandsAtTimeDict

    #Reduces the lifeguard score by the appropriate amount given a lifeguard is put on break at a time
    def reduceLifeguardScore(self, lifeguardsAtTime, timeWithHighestRatio):

        #For each interval in the break interval
        for j in range(0, self._staticAppInfo.getBreakInterval()):
            # Create the time to remove from going forward
            timeToRemoveFromForward = Time().setTimeWithMinutes(timeWithHighestRatio.getMinutes() +
                                                                j * self._staticAppInfo.getTimeInterval())
            # Reduce the lifeguards working score by the calculated amount for the forward time
            for time in lifeguardsAtTime:
                if time.equals(timeToRemoveFromForward):
                    lifeguardsAtTime[time] -= self._staticAppInfo.getBreakInterval() - j

            # Only do if j is not 0 (initial time so that it goes like a pyramid)
            if j != 0:
                # Create the time to remove from going backward
                timeToRemoveFromBackward = Time().setTimeWithMinutes(timeWithHighestRatio.getMinutes() -
                                                                     j * self._staticAppInfo.getTimeInterval())
                # Reduce the lifeguards working score by the calculated amount for the backward time
                for time in lifeguardsAtTime:
                    if time.equals(timeToRemoveFromBackward):
                        lifeguardsAtTime[time] -= self._staticAppInfo.getBreakInterval() - j

    #Returns a dictionary with a score for the amount of lifeguards at every time of the day (for breaks)
    def getLifeguardsOnDutyDict(self):

        # Define a dictionary that stores each time and the number of lifeguards at the time
        lifeguardsAtTime = dict()

        # Create the dictionary where at each time (key) it describes the amount of lifeguard working at that time
        for i in range(0, 1440, self._staticAppInfo.getTimeInterval()):

            #Set the lifeguard score to 0 (this is what determines is the best time)
            lifeguardScore = 0

            #Set the time being observed
            time = Time().setTimeWithMinutes(i)

            #For each time in the break being observed
            for j in range(0, self._staticAppInfo.getBreakInterval()):

                #Set the time
                timeObserving = Time().setTimeWithMinutes(time.getMinutes() + j * self._staticAppInfo.getTimeInterval())

                #Only count it if the time being observed is before the end of the day (12 AM)
                if timeObserving.getMinutes() < 1440:
                    for lifeguard in self._lifeguards:
                        if lifeguard.isWorking(timeObserving):
                            lifeguardScore += 1
            lifeguardsAtTime[time] = lifeguardScore

        return lifeguardsAtTime

    #Returns the lifeguards list
    def getLifeguards(self):
        return self._lifeguards

    #Returns lifeguards that are working at a specific time
    def getLifeguardsWorkingAtASpecificTime(self, time):

        #Create an empty list that will be appended to
        lifeguardsWorkingAtTime = []

        #Continue if the time is a Time object
        if isinstance(time, Time):
            for lifeguard in self._lifeguards:
                if lifeguard.isWorking(time):
                    lifeguardsWorkingAtTime.append(lifeguard)
        else:
            print("ERROR IN CALCULATE SCHEDULE - time variable not correct for gLWAAST")

        #Return the list
        return lifeguardsWorkingAtTime

    #Returns a list of people who actually have breaks in sorted order
    def getLifeguardsWithBreaks(self):
        self.sortLifeguards()
        lifeguardsWithBreaks = []
        for lifeguard in self._lifeguards:
            if lifeguard.getNumBreaks() > 0:
                lifeguardsWithBreaks.append(lifeguard)
        return lifeguardsWithBreaks

    #Returns the time range between when the first lifeguard enters to when the last lifeguard leaves
    def calculatePoolOpenTimeRange(self):

        #Set variables for the earliest time and the latest time
        earliestTime = Time()
        latestTime = Time()
        if len(self._lifeguards) > 0:
            earliestTime = self._lifeguards[0].getShiftStartTime()
            latestTime = self._lifeguards[0].getShiftEndTime()

        #Check the start and end of each lifeguard and change the earliest time and latest time variables if needed
        for i in range(1, len(self._lifeguards)):
            lifeguard = self._lifeguards[i]
            if lifeguard.getShiftStartTime().getMinutes() < earliestTime.getMinutes():
                earliestTime = lifeguard.getShiftStartTime()
            if lifeguard.getShiftEndTime().getMinutes() > latestTime.getMinutes():
                latestTime = lifeguard.getShiftEndTime()

        #Return a list that is the pair of the two times together
        return [earliestTime, latestTime]

    #Prints the schedule (good for testing)
    def printSchedule(self):

        #Print the first two line
        line = ""
        #Header
        line += "Schedule" + "|"
        #Lifeguard numbers up top
        for lifeguard in self._lifeguards:
            line += (3- len(str(lifeguard.getIdNum()))) * " " + str(lifeguard.getIdNum()) + "|"
        #Print the line and then the line of dashes
        print(line)
        print("-" * len(line))

        #Get the time range
        timeRange = self.calculatePoolOpenTimeRange()
        earliestTime = timeRange[0]
        latestTime = timeRange[1]

        #For each time from the start to the end of the shifts
        for t in range(earliestTime.getMinutes(), latestTime.getMinutes(), self._staticAppInfo.getTimeInterval()):

            #Create a variable for the current line
            line = ""

            #Set the current time
            currentTime = Time().setTimeWithMinutes(t)

            #Add to the line
            line += currentTime.get12Time() + "|"

            #Add each lifeguard's stand at this time
            for lifeguard in self._lifeguards:
                stand = lifeguard.getStand(currentTime)
                if stand == "BREAK":
                    stand = "Y"
                if stand == "EMPTY":
                    stand = "NA"
                line += (3 - len(stand)) * " " + stand + "|"

            #Print the time
            print(line)
            print("-" * len(line))
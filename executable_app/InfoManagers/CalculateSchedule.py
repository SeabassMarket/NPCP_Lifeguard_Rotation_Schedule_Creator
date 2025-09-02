# import libraries
from .Lifeguard import Lifeguard
import random
from .Stand import Stand
from .StaticAppInfo import StaticAppInfo
from .Time import Time


# Helper class to raise errors
class CalculaterException(Exception):
    pass


# This object will be used to calculate and organize different data
class CalculateSchedule:
    # Initialize object
    def __init__(self, staticAppInfo):
        # Initialize staticAppInfo
        if isinstance(staticAppInfo, StaticAppInfo):
            self._staticAppInfo = staticAppInfo
        else:
            self._staticAppInfo = StaticAppInfo("ERROR")
            print("ERROR, STATIC APP INFO NOT INITIALIZED")

        # Get lifeguardData from staticAppInfo
        lifeguardData = self._staticAppInfo.getEventDataSpecific("lifeguard")

        # Get stand date from staticAppInfo
        standData = self._staticAppInfo.getEventDataSpecific("stand")

        # Check data length
        if len(lifeguardData) < 1 or len(standData) < 1:
            raise CalculaterException("Data not set")

        # Create lifeguard objects
        for lifeguardKey in lifeguardData:
            self._lifeguards: list[Lifeguard] = []
            lifeguards = lifeguardData[lifeguardKey]
            count = 0
            for lifeguard in lifeguards:
                self._lifeguards.append(
                    Lifeguard(
                        shiftTimes=lifeguards[lifeguard],
                        name=lifeguard,
                        idNum=count,
                        staticAppInfo=self._staticAppInfo,
                    )
                )
                count += 1

        # Create lifeguard dict
        self._lifeguardDict: dict[str, Lifeguard] = {}
        for lifeguard in self._lifeguards:
            self._lifeguardDict[lifeguard.getName()] = lifeguard

        # Up stands
        upStandData = list(standData.values())[0]
        self._upStands = []
        for stand in upStandData:
            newStand = Stand(
                name=stand,
                standType=list(standData.keys())[0],
                startTime=upStandData[stand][0],
                endTime=upStandData[stand][1],
            )
            self._upStands.append(newStand)
        # Timely down stands
        timelyDownStandData = list(standData.values())[1]
        self._timelyDownStands = []
        for stand in timelyDownStandData:
            newStand = Stand(
                name=stand,
                standType=list(standData.keys())[1],
                startTime=timelyDownStandData[stand][0],
                endTime=timelyDownStandData[stand][1],
                amountPerInterval=timelyDownStandData[stand][2],
            )
            self._timelyDownStands.append(newStand)
        # Priority down stands
        priorityDownStandData = list(standData.values())[2]
        self._priorityDownStands = []
        for stand in priorityDownStandData:
            newStand = Stand(
                name=stand,
                standType=list(standData.keys())[2],
                isAllDay=True,
                startTime=priorityDownStandData[stand][0],
                endTime=priorityDownStandData[stand][1],
                amountPerInterval=priorityDownStandData[stand][2],
            )
            self._priorityDownStands.append(newStand)
        # Fill-in down stands
        fillInDownStandData = list(standData.values())[3]
        self._fillInDownStands = []
        for stand in fillInDownStandData:
            newStand = Stand(
                name=stand,
                standType=list(standData.keys())[3],
                isAllDay=True,
                startTime=fillInDownStandData[stand][0],
                endTime=fillInDownStandData[stand][1],
            )
            self._fillInDownStands.append(newStand)

        # Initialize the breaks instance variable
        self._breaks = []

        # Initialize branch time
        self._branchTime = Time(0, 0)

    def addLifeguardSchedule(self, lifeguardNamesToSchedule: dict[str, list[str]]):
        for name in lifeguardNamesToSchedule:
            lifeguard = self._lifeguardDict[name]

            schedule = lifeguardNamesToSchedule[name]

            lifeguardSchedule = lifeguard.getSchedule()

            index = 0
            for scheduleTime in lifeguardSchedule:
                if index < len(schedule):
                    break

                stand = schedule[index]

                lifeguardSchedule[scheduleTime] = stand

                index += 1

    def calculateSchedule(self, branchTime: Time = Time(0, 0)):
        self._branchTime = branchTime

        self.resetSchedule()
        self.assignBreaks()
        self.calculateStands()

    def calculateStands(self):
        # Get the time range of when the pool is open
        earliestTime, latestTime = self.calculatePoolOpenTimeRange()

        times = [earliestTime.getMinutes(), self._branchTime.getMinutes()]

        earliestTime = Time().setTimeWithMinutes(max(times))

        # For each time between the earliest time and the latest time (excluding latest)
        for t in range(
            earliestTime.getMinutes(),
            latestTime.getMinutes(),
            self._staticAppInfo.getTimeInterval(),
        ):
            # Create a time object for this iteration/current time being observed
            currentTime = Time().setTimeWithMinutes(t)

            # Assign the up stands for the lifeguards
            self.assignUpStandsAtTime(currentTime)

            # Swap stands in case someone is starting a break next to optimize stand up intervals
            self.optimizeUpcomingBreaks(currentTime)

        # Reorganize the lifeguard stands to fix circular issues, duplicates, and make it pretty
        self.reorganizeLifeguards()

        # For each time between the earliest time and the latest time (excluding latest)
        for t in range(
            earliestTime.getMinutes(),
            latestTime.getMinutes(),
            self._staticAppInfo.getTimeInterval(),
        ):
            # Create a time object for this iteration/current time being observed
            currentTime = Time().setTimeWithMinutes(t)

            # Assign the timely down stands
            self.assignTimelyDownStandsAtTime(currentTime)

            # Assign the priority down stands
            self.assignPriorityDownStandsAtTime(currentTime)

            # Assign the fill-in down stands
            self.assignFillInDownStandsAtTime(currentTime)

    # Optimizes the stands so that the lifeguard going on break has the most up stand intervals
    def optimizeUpcomingBreaks(self, currentTime):
        # Check to make sure currentTime is a time
        if not isinstance(currentTime, Time):
            print("ERROR IN CALCULATE SCHEDULE - oUB")
            return

        # Stands are eligible for swapping if they both have the same amount of intervals up on stand at some point, so
        # have to check the history of the other lifeguards currently working

        # Figure out what the next time is
        nextTime = Time().setTimeWithMinutes(
            currentTime.getMinutes() + self._staticAppInfo.getTimeInterval()
        )

        # Get the lifeguards who are working at this time
        lifeguardsWorkingAtTime = self.getLifeguardsWorkingAtASpecificTime(currentTime)

        # Get the lifeguards going on break or fully off shift in the next interval
        # NOTE - lifeguards going on break also includes lifeguards going off shift
        lifeguardsGoingOnBreak = self.getLifeguardGoingOnBreakOrClockingOutNext(
            currentTime
        )

        # Pop out the lifeguards going on break in lifeguards working at time so that we don't compare them against
        # themselves or each other
        for i in range(len(lifeguardsWorkingAtTime) - 1, -1, -1):
            if lifeguardsWorkingAtTime[i] in lifeguardsGoingOnBreak:
                lifeguardsWorkingAtTime.pop(i)

        # For each lifeguard that is going on break, check if a swap is available
        # Create a dictionary with all the options for each lifeguard
        possibilitiesForStandSwapsForEachLifeguard = dict()
        for lifeguard in lifeguardsGoingOnBreak:
            # Create a dictionary with times as the key and a list of the intervals up on stand for each lifeguard as
            # the value
            timesAndIntervalsUpOnStand = dict()

            # Also create an equivalent dictionary but for the lifeguard going on break
            timesAndIntervalsUpOnStandGoingOnBreak = dict()

            # Get the time that we are going back until
            timeFurthestBack = lifeguard.getFurthestTimeBackToDisruption(currentTime)

            times = [timeFurthestBack.getMinutes(), self._branchTime.getMinutes()]

            timeFurthestBack = Time().setTimeWithMinutes(max(times))

            # Get the time variable that will be used to go backwards
            timeBeingAnalyzed = currentTime.getMinutes()
            while timeBeingAnalyzed >= timeFurthestBack.getMinutes():
                # Create a time object out of the time being analyzed
                timeObjectBeingAnalyzed = Time().setTimeWithMinutes(timeBeingAnalyzed)

                # Assign the value to the dictionary for the other lifeguards not going on break
                listToAdd = []
                for lifeguardNotGoingToBreak in lifeguardsWorkingAtTime:
                    listToAdd.append(
                        lifeguardNotGoingToBreak.getIntervalsUpOnStand(
                            timeObjectBeingAnalyzed
                        )
                    )
                timesAndIntervalsUpOnStand[timeBeingAnalyzed] = listToAdd

                # Assign the value to the dictionary for the lifeguard going on break
                timesAndIntervalsUpOnStandGoingOnBreak[timeBeingAnalyzed] = (
                    lifeguard.getIntervalsUpOnStand(timeObjectBeingAnalyzed)
                )

                # Decrease the time by the interval time
                timeBeingAnalyzed -= self._staticAppInfo.getTimeInterval()

            # Traverse the dictionary to find times and matches for when the intervals up on stand is 0
            # Record these instances in a dictionary where the key is the time and the values are lists of the indices
            # of the lifeguards that match this criteria
            possibilitiesForSwitching = dict()
            for thisTime in timesAndIntervalsUpOnStandGoingOnBreak:
                # Get the intervals on stand at this time for the lifeguard going up on stand
                respectiveIntervalsUpOnStandGoingOnBreak = (
                    timesAndIntervalsUpOnStandGoingOnBreak[thisTime]
                )

                # If the lifeguard going on break has no intervals on stand at this time, check the others
                if respectiveIntervalsUpOnStandGoingOnBreak == 0:
                    # Create a list of the respective intervals up on stand
                    respectiveIntervalsUpOnStandList = timesAndIntervalsUpOnStand[
                        thisTime
                    ]

                    # Check the list to see if it has a matching value of 0
                    # If it does add the index to the indices that match list
                    # NOTE: Do not add the index to the list if the time being analyzed is past the furthest back time
                    # as calculated using the current time
                    indicesThatMatchList = []
                    for i in range(0, len(respectiveIntervalsUpOnStandList)):
                        # Generate the furthest back time (time to nearest break or shift start backwards)
                        furthestBackTime = lifeguardsWorkingAtTime[
                            i
                        ].getFurthestTimeBackToDisruption(currentTime)

                        times = [
                            furthestBackTime.getMinutes(),
                            self._branchTime.getMinutes(),
                        ]

                        furthestBackTime = Time().setTimeWithMinutes(max(times))

                        # Check to see if the guard at this index has 0 up stand intervals at this time and also that a
                        # swap would be viable. A swap is not viable if the time is less than the furthest back time
                        if (
                            respectiveIntervalsUpOnStandList[i] == 0
                            and furthestBackTime.getMinutes() <= thisTime
                        ):
                            indicesThatMatchList.append(i)

                    # Add the entry to the dictionary
                    possibilitiesForSwitching[thisTime] = indicesThatMatchList

            # Add the created dictionary to the dictionary for all the lifeguards under the key lifeguard
            possibilitiesForStandSwapsForEachLifeguard[lifeguard] = (
                possibilitiesForSwitching
            )

        # Create a dictionary with the unique lifeguards that could be swapped with
        uniqueLifeguardsThatCanBeSwappedWith = dict()
        for lifeguard in possibilitiesForStandSwapsForEachLifeguard:
            # Get the dictionary
            singularPossibilitiesDictionary = (
                possibilitiesForStandSwapsForEachLifeguard[lifeguard]
            )

            # Go through the values of the dictionary and append the unique values
            uniqueIndices = []
            for listOfIndicesAtTime in list(singularPossibilitiesDictionary.values()):
                for index in listOfIndicesAtTime:
                    if index not in uniqueIndices:
                        uniqueIndices.append(index)

            # Add it to the dictionary
            uniqueLifeguardsThatCanBeSwappedWith[lifeguard] = uniqueIndices

        # Create a new dictionary. The key is the lifeguard going on break, and the value is a list with the same length
        # as the unique lifeguard that can be swapped with. However, instead of the index of the lifeguard it is the
        # intervals up on stand directly prior to the
        uniqueLifeguardsUpStandIntervalsScore = dict()
        lifeguardGoingOnBreakUpStandIntervalScore = dict()
        for lifeguard in uniqueLifeguardsThatCanBeSwappedWith:
            # Add to the dictionary for the lifeguard actually going on break
            lifeguardGoingOnBreakUpStandIntervalScore[lifeguard] = (
                lifeguard.getIntervalsUpOnStand(nextTime)
            )

            # Get the list of indices
            listOfIndices = uniqueLifeguardsThatCanBeSwappedWith[lifeguard]

            # Create a new list with the score for each of the lifeguards at the given index
            # NOTE: lifeguards Working At Time is actually lifeguards not going on break because we popped it earlier
            lifeguardsScores = []
            indicesToPop = []
            for i in range(0, len(listOfIndices)):
                index = listOfIndices[i]
                intervalsUpOnStand = lifeguardsWorkingAtTime[
                    index
                ].getIntervalsUpOnStand(nextTime)
                lifeguardsScores.append(
                    intervalsUpOnStand - lifeguard.getIntervalsUpOnStand(nextTime)
                )
                if intervalsUpOnStand <= lifeguard.getIntervalsUpOnStand(nextTime):
                    indicesToPop.append(i)
            for i in range(len(listOfIndices) - 1, -1, -1):
                if i in indicesToPop:
                    listOfIndices.pop(i)
                    lifeguardsScores.pop(i)
            uniqueLifeguardsUpStandIntervalsScore[lifeguard] = lifeguardsScores

        """
        THIS CODE IS CURRENTLY NOT BEING USED BECAUSE THE SORTING IS NOT NEEDED, BUT I DO NOT WANT TO DELETE IT OUTRIGHT
        #Sort the lifeguards into who needs the swap the most (aka who has the lowest up stand interval score to start)
        lifeguardGoingOnBreakOrder = []
        scores = list(lifeguardGoingOnBreakUpStandIntervalScore.values())
        lifeguards = list(lifeguardGoingOnBreakUpStandIntervalScore.keys())
        for i in range(0, len(lifeguardGoingOnBreakUpStandIntervalScore)):
            index = scores.index(min(scores))
            scores.pop(index)
            lifeguardGoingOnBreakOrder.append(lifeguards.pop(index))

        #Sort the lists for each (for better observation)
        for lifeguard in lifeguardGoingOnBreakOrder:

            #Sort the lifeguards that can be swapped with so that the ones that would be best are in the front
            uniqueSwappableLifeguards = uniqueLifeguardsThatCanBeSwappedWith[lifeguard]
            uniqueSwappableLifeguardIntervalScores = uniqueLifeguardsUpStandIntervalsScore[lifeguard]
            for i in range(0, len(uniqueSwappableLifeguards)):

                #Find the max of the other unique swappable lifeguard interval scores and use that to sort
                maxIntervalScore = uniqueSwappableLifeguardIntervalScores[i]
                maxIndex = i
                for j in range(i, len(uniqueSwappableLifeguardIntervalScores)):
                    if uniqueSwappableLifeguardIntervalScores[j] > maxIntervalScore:
                        maxIntervalScore = uniqueSwappableLifeguardIntervalScores[j]
                        maxIndex = j

                #Swap the value at i with the max value
                tempIntervalScore = uniqueSwappableLifeguardIntervalScores[i]
                uniqueSwappableLifeguardIntervalScores[i] = uniqueSwappableLifeguardIntervalScores[maxIndex]
                uniqueSwappableLifeguardIntervalScores[maxIndex] = tempIntervalScore
                tempUniqueLifeguard = uniqueSwappableLifeguards[i]
                uniqueSwappableLifeguards[i] = uniqueSwappableLifeguards[maxIndex]
                uniqueSwappableLifeguards[maxIndex] = tempUniqueLifeguard
        """

        # Go through each lifeguard and perform a swap if possible. Pick the best possible choice, which is calculated
        # by a recursive algorithm that checks all the permutations
        if len(lifeguardsGoingOnBreak) > 0:
            bestPermutation = self.getBestPossiblePermutationOfLifeguardRearrangements(
                uniqueLifeguardsThatCanBeSwappedWith,
                uniqueLifeguardsUpStandIntervalsScore,
                lifeguardGoingOnBreakUpStandIntervalScore,
            )
            # Swap the shifts
            for i in range(0, len(lifeguardsGoingOnBreak)):
                if isinstance(bestPermutation[i], int):
                    # Get the index of the lifeguard from the permutation (index in lifeguards Working At Time)
                    lifeguardNum = bestPermutation[i]

                    # Get the lifeguard being swapped (in lifeguards going on break)
                    lifeguardBeingSwapped = lifeguardsGoingOnBreak[i]

                    # Calculate the back time
                    backTime = Time()
                    for thisTime in possibilitiesForStandSwapsForEachLifeguard[
                        lifeguardBeingSwapped
                    ]:
                        lifeguardSwaps = possibilitiesForStandSwapsForEachLifeguard[
                            lifeguardBeingSwapped
                        ][thisTime]
                        if lifeguardNum in lifeguardSwaps:
                            backTime = Time().setTimeWithMinutes(thisTime)
                            break

                    # Get the lifeguard being swapped with using the previously found index
                    lifeguardBeingSwappedWith = lifeguardsWorkingAtTime[lifeguardNum]

                    # Swap the random chance and schedule between the two guards (using back time and next time because
                    # it is inclusive of the first time but exclusive of the last time)
                    lifeguardBeingSwapped.swapSchedulesBetweenTimes(
                        lifeguardBeingSwappedWith, backTime, nextTime
                    )
                    lifeguardBeingSwapped.swapRandomChances(
                        lifeguardBeingSwappedWith, backTime, nextTime
                    )

                    # Print out which lifeguards are being swapped
                    message = (
                        currentTime.get12Time()
                        + ": "
                        + "Swapped "
                        + str(lifeguardBeingSwapped.getIdNum())
                        + (2 - len(str(lifeguardBeingSwapped.getIdNum()))) * " "
                        + " with "
                        + str(lifeguardBeingSwappedWith.getIdNum())
                    )
                    try:
                        # noinspection PyUnboundLocalVariable
                        messages.append(message)
                    except NameError:
                        messages = [message]

        """
        # Print info
        if len(lifeguardsGoingOnBreak) > 0:
            print(currentTime.get12Time(), end=": ")

        for lifeguard in lifeguardsGoingOnBreak:
            print(lifeguard.getIdNum(), end=" ")

        if len(lifeguardsGoingOnBreak) > 0:
            print()
            print()

        for lifeguard in possibilitiesForStandSwapsForEachLifeguard:
            print(
                "Lifeguard ID:",
                lifeguard.getIdNum(),
                "- Lifeguard interval score:",
                lifeguardGoingOnBreakUpStandIntervalScore[lifeguard],
            )
            for time in possibilitiesForStandSwapsForEachLifeguard[lifeguard]:
                time1 = Time().setTimeWithMinutes(time)
                print(time1.get12Time(), end=": ")
                print(possibilitiesForStandSwapsForEachLifeguard[lifeguard][time])
            print(uniqueLifeguardsThatCanBeSwappedWith[lifeguard])
            print(uniqueLifeguardsUpStandIntervalsScore[lifeguard])
            print()

        if len(lifeguardsGoingOnBreak) > 0:
            # noinspection PyUnboundLocalVariable
            print(bestPermutation)

        try:
            # noinspection PyUnboundLocalVariable
            for message in messages:
                print(message)
        except NameError:
            pass

        if len(lifeguardsGoingOnBreak) > 0:
            print("END HERE")
            print()
        """

    # This returns the best possible permutation of lifeguard swaps before a break
    def getBestPossiblePermutationOfLifeguardRearrangements(
        self,
        uniqueLifeguardsThatCanBeSwappedWith,
        uniqueLifeguardsUpStandIntervalsScore,
        lifeguardGoingOnBreakUpStandIntervalScore,
    ):
        # Create values being looked at
        lifeguardValues = list(uniqueLifeguardsThatCanBeSwappedWith.values())

        # First create a list of the different permutations that are possible
        optionsDictionary = self.recursivelyGenerateRearrangementPermutations(
            lifeguardValues
        )

        # Generate the permutations in one giant list
        optionsList = self.recursivelyInterpretGeneratedDictionary(optionsDictionary)

        # Go through each one of the options and give it a score
        optionsScores = []
        scoreValues = list(uniqueLifeguardsUpStandIntervalsScore.values())
        for option in optionsList:
            score = 0
            for i in range(0, len(option)):
                if isinstance(option[i], int):
                    lifeguardValuesForThisGuard = lifeguardValues[i]
                    scoreValuesForThisGuard = scoreValues[i]
                    index = lifeguardValuesForThisGuard.index(option[i])
                    score += scoreValuesForThisGuard[index]
            optionsScores.append([score, option])

        # Now that we have a score for each one, filter for the ones that have the highest cumulative score
        maxScore = 0
        for score in optionsScores:
            if score[0] > maxScore:
                maxScore = score[0]
        for i in range(len(optionsScores) - 1, -1, -1):
            if optionsScores[i][0] != maxScore:
                optionsScores.pop(i)

        # Bad options have been popped, so now find the options that has the least difference between the most up stands
        # before break and the least up stands before break
        for option in optionsScores:
            optionBeingAnalyzed = option[1]
            newUpStandIntervalsList = []
            for i in range(0, len(optionBeingAnalyzed)):
                newUpStandInterval = list(
                    lifeguardGoingOnBreakUpStandIntervalScore.values()
                )[i]
                if isinstance(optionBeingAnalyzed[i], int):
                    lifeguardValuesForThisGuard = lifeguardValues[i]
                    scoreValuesForThisGuard = scoreValues[i]
                    index = lifeguardValuesForThisGuard.index(optionBeingAnalyzed[i])
                    newUpStandInterval += scoreValuesForThisGuard[index]
                newUpStandIntervalsList.append(newUpStandInterval)
            biggestDisparity = max(newUpStandIntervalsList) - min(
                newUpStandIntervalsList
            )
            option[0] = biggestDisparity

        # Now that we have gone through each of the best choices, the choices left are essentially tied. Just return a
        # random choice
        return random.choice(optionsScores)[1]

    # Interpret the dictionary generated recursively to return just a straight-up list of the permutations
    def recursivelyInterpretGeneratedDictionary(
        self, dictionary, depth=None, optionsList=None
    ):
        # Set the depth if it is None
        if depth is None:
            depth = []

        # Set the options list if it is None
        if optionsList is None:
            optionsList = []

        # If it is a dictionary
        if isinstance(dictionary, dict):
            for key in dictionary:
                newDepth = list(depth)
                newDepth.append(key)
                self.recursivelyInterpretGeneratedDictionary(
                    dictionary[key], newDepth, optionsList
                )

        # If it is a list
        if isinstance(dictionary, list):
            for value in dictionary:
                newDepth = list(depth)
                newDepth.append(value)
                optionsList.append(newDepth)

        # Return the created options list
        return optionsList

    # Generates a dictionary of dictionaries ending in a list that can be interpreted to generate permutations
    def recursivelyGenerateRearrangementPermutations(self, values, depth=None):
        # Set depth if it is None
        if depth is None:
            depth = []

        # Create the options dictionary or list
        if len(depth) + 1 < len(values):
            options = dict()
        else:
            options = []

        # Get the values for this depth
        valuesAtThisDepth = list(values[len(depth)])

        # Get rid of the values that are in depth
        for i in range(len(valuesAtThisDepth) - 1, -1, -1):
            if valuesAtThisDepth[i] in depth:
                valuesAtThisDepth.pop(i)

        # Go through each layer at the current depth and add it to the dictionary
        for value in valuesAtThisDepth:
            # Code for if it is a dictionary
            if isinstance(options, dict):
                newDepth = list(depth)
                newDepth.append(value)
                options[value] = self.recursivelyGenerateRearrangementPermutations(
                    values, newDepth
                )

            # Code for if it is a list
            if isinstance(options, list):
                options.append(value)

        # Pick doing nothing at all
        # For dictionaries
        if isinstance(options, dict):
            newDepth = list(depth)
            newDepth.append("NOTHING")
            options["NOTHING"] = self.recursivelyGenerateRearrangementPermutations(
                values, newDepth
            )

        # For lists
        if isinstance(options, list):
            options.append("NOTHING")

        return options

    # Assigns the fill-in down stands to lifeguards at a given time
    def assignFillInDownStandsAtTime(self, currentTime: Time):
        lifeguardsDownAtTime = self.getLifeguardsOnGivenStandsAtTime(
            currentTime, [self._staticAppInfo.getEmptyCode()]
        )

        lifeguardsLength = len(lifeguardsDownAtTime)

        standsOpen = Stand.getStandNames(self._fillInDownStands)

        if len(standsOpen) < 1:
            return

        for i in range(lifeguardsLength):
            lifeguard = lifeguardsDownAtTime.pop(
                random.randrange(len(lifeguardsDownAtTime))
            )

            stand = standsOpen[random.randrange(len(standsOpen))]

            lifeguard.addStand(currentTime, stand)

    # Assigns the priority down stands to lifeguards at a given time
    def assignPriorityDownStandsAtTime(self, currentTime: Time):
        lifeguardsDownAtTime = self.getLifeguardsOnGivenStandsAtTime(
            currentTime, [self._staticAppInfo.getEmptyCode()]
        )

        standsOpen = Stand.getStandNames(self._priorityDownStands)

        minimum = min([len(lifeguardsDownAtTime), len(standsOpen)])

        for i in range(minimum):
            lifeguard = lifeguardsDownAtTime.pop(
                random.randrange(len(lifeguardsDownAtTime))
            )

            stand = standsOpen.pop(0)

            lifeguard.addStand(currentTime, stand)

    # Assigns the timely down stands to lifeguards at a given time
    def assignTimelyDownStandsAtTime(self, currentTime: Time):
        lifeguardsDownAtTime = self.getLifeguardsOnGivenStandsAtTime(
            currentTime, [self._staticAppInfo.getEmptyCode()]
        )

        standsOpen = self.getStandsOpenAtTime(currentTime, self._timelyDownStands)

        minimum = min([len(lifeguardsDownAtTime), len(standsOpen)])

        for i in range(minimum):
            lifeguard = lifeguardsDownAtTime.pop(
                random.randrange(len(lifeguardsDownAtTime))
            )

            stand = standsOpen.pop(0)

            lifeguard.addStand(currentTime, stand)

    # Gets the lifeguards on a specific set of stands at a given time
    def getLifeguardsOnGivenStandsAtTime(
        self, currentTime: Time, standList: list[Stand | str]
    ) -> list[Lifeguard]:
        standListNames = Stand.getStandNames(standList)

        lifeguardsWorkingAtTime = self.getLifeguardsWorkingAtASpecificTime(currentTime)

        lifeguardsOnGivenStands = []
        for lifeguard in lifeguardsWorkingAtTime:
            if lifeguard.getStand(currentTime) in standListNames:
                lifeguardsOnGivenStands.append(lifeguard)

        return lifeguardsOnGivenStands

    # Assigns the up stands to lifeguards at a given time
    def assignUpStandsAtTime(self, currentTime):
        # Continue if time is actually a time
        if isinstance(currentTime, Time):
            # Create a list with all the lifeguards working at this time
            lifeguardsWorkingAtTime = self.getLifeguardsWorkingAtASpecificTime(
                currentTime
            )

            # Get the up stands for this time
            upStandsAtTime = self.getStandsOpenAtTime(currentTime, self._upStands)

            # Calculate the amount of iterations necessary
            numIterations = min([len(upStandsAtTime), len(lifeguardsWorkingAtTime)])

            # Assign the stands to lifeguards based on:
            # 1 those who have the lowest intervals up on stand
            # 2 who has the shortest time left in their shift
            # 3 Pick who has the most amount of downs IF there are more lifeguard with 0 up intervals than
            # up stands to pick from
            # 4 those who have been selected for random chance the least
            # 5 random chance
            for i in range(0, numIterations):
                """CHOOSE STAND TO ADD"""
                # Get the stand that we are going to be adding and pop it too
                standToAdd = upStandsAtTime.pop(
                    upStandsAtTime.index(random.choice(upStandsAtTime))
                )

                """CREATE THE TEMP LIFEGUARD LIST THAT WILL BE TORN APART AS WE GO THROUGH"""
                # Create a duplicate list of the lifeguards that we can tear apart as we qualify lifeguards
                tempLifeguards = []
                for lifeguard in lifeguardsWorkingAtTime:
                    tempLifeguards.append(lifeguard)

                """HERE WE CHECK WHO HAS THE LOWEST INTERVALS ON STAND (ALGORITHM #1)"""
                # Get a list of how much each lifeguard that is working at this time has been up on stand
                intervalsUpOnStand = []
                for lifeguard in tempLifeguards:
                    intervalsUpOnStand.append(
                        lifeguard.getIntervalsUpOnStand(currentTime)
                    )

                # First figure out if we can use the minimum intervals method and get the lifeguard who would apply for '
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
                # message = "INTERVALS UP ON STAND USED ON"

                """HERE WE CHECK WHO HAS THE SHORTEST TIME LEFT ON THEIR SHIFT (ALGORITHM #2)"""

                """
                For now I want to disable this because I think it isn't really great
                
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
                """

                """HERE WE CHECK WHO HAS THE MOST AMOUNT OF DOWN STANDS IF THERE ARE MORE LIFEGUARD WITH 0 UP STANDS
                THAN UP STANDS TO BE ASSIGNED (NEW ALGORITHM #3)"""
                if tieBreaker and intervalsUpOnStand[0] == 0:
                    # Get list of intervals down on stand
                    intervalsDownOnStand = []
                    for lifeguard in tempLifeguards:
                        intervalsDownOnStand.append(
                            lifeguard.getIntervalsDownOnStand(currentTime)
                        )

                    # Check eligibility of the third picking algorithm
                    tieBreaker = False
                    maximum = max(intervalsDownOnStand)

                    # Get all the values with the maximum and pop the lifeguards who don't have the maximum
                    for j in range(len(intervalsDownOnStand) - 1, -1, -1):
                        if intervalsDownOnStand[j] != maximum:
                            tempLifeguards.pop(j)
                            intervalsDownOnStand.pop(j)

                    # Continue to tie-breaker if we're going to need it
                    if len(intervalsDownOnStand) > numIterations - i:
                        tieBreaker = True

                    # Set the index
                    index = intervalsDownOnStand.index(maximum)
                    lifeguard = tempLifeguards[index]
                    index = lifeguardsWorkingAtTime.index(lifeguard)
                    message = "MAX DOWN STANDS USED ON"

                """HERE WE CHECK WHO HAS THE LEAST AMOUNT OF RANDOM CHANCES (ALGORITHM #4)"""
                # Figure out if we can use the least amount of random chances method if the last one didn't work
                if tieBreaker:
                    # Get a list of all the random chances of the lifeguards working at this time
                    lifeguardRandomChances = []
                    for lifeguard in tempLifeguards:
                        lifeguardRandomChances.append(
                            lifeguard.getRandomChance(currentTime)
                        )

                    # Check eligibility of the fourth picking algorithm
                    tieBreaker = False
                    minimum = min(lifeguardRandomChances)
                    # Get all the values with the minimum and pop the lifeguards who don't have the minimum
                    for j in range(len(lifeguardRandomChances) - 1, -1, -1):
                        if lifeguardRandomChances[j] != minimum:
                            tempLifeguards.pop(j)
                            lifeguardRandomChances.pop(j)
                    # Continue to tie-breaker if we're going to need it
                    if len(lifeguardRandomChances) > numIterations - i:
                        tieBreaker = True

                    # Set the index
                    index = lifeguardRandomChances.index(minimum)
                    lifeguard = tempLifeguards[index]
                    index = lifeguardsWorkingAtTime.index(lifeguard)
                    # message = "RANDOM CHANCE USED ON"

                """RANDOMLY PICK AN INDEX FOR THE LIFEGUARD IF ALL ELSE FAILS (ALGORITHM #5)"""
                # If there is no tie-breaker, assign using the lowest interval algorithm
                if (
                    tieBreaker
                ):  # If there is a tie-breaker, finally just use random chance
                    # Randomly select a lifeguard
                    index = random.randint(a=0, b=len(tempLifeguards) - 1)
                    lifeguard = tempLifeguards[index]
                    lifeguard.incrementRandomChance(currentTime)
                    index = lifeguardsWorkingAtTime.index(lifeguard)
                    # message = "COMPLETELY RANDOM CHANCE USED ON"

                """FINALLY ASSIGN THE STAND"""
                lifeguard = lifeguardsWorkingAtTime.pop(index)
                lifeguard.addStand(thisTime=currentTime, standName=standToAdd)

                # Print info to help with testing
                """
                self.printSchedule()
                print(currentTime.get12Time() + " - " + message + " " + str(lifeguard.getIdNum()), end="")
                input()
                print()
                """

        else:
            print("ERROR IN CALCULATE SCHEDULE - aUSAT")

    # Reorganizes stands that lifeguards are on to optimize relieving
    def reorganizeLifeguards(self):
        earliestTime, latestTime = self.calculatePoolOpenTimeRange()

        times = [earliestTime.getMinutes(), self._branchTime.getMinutes()]

        earliestTime = Time().setTimeWithMinutes(max(times))

        # Store the up stands found in the schedule
        timeToUpStandChoices = {}
        for t in range(
            earliestTime.getMinutes() - self._staticAppInfo.getTimeInterval(),
            latestTime.getMinutes(),
            self._staticAppInfo.getTimeInterval(),
        ):
            currentTime = Time().setTimeWithMinutes(t)

            timeToUpStandChoices[currentTime] = (
                self.getStandsAtTimeFromLifeguardSchedules(currentTime, self._upStands)
            )

        # Reset each lifeguard so each up stand is just the up stand code
        for lifeguard in self._lifeguards:
            lifeguard.convertScheduleToUp(self._upStands, self._branchTime)

        # Reorganize for each time of day
        for i in range(1, len(timeToUpStandChoices)):
            """
            For each time in the day, reorganize the lifeguards according to the pretty + backup algorithms.
            
            The pretty algorithm is to make an effort for lifeguard to follow patterns (e.g. T -> S, A -> B, J -> K)
            
            The backup algorithm is to cover the holes left behind by the pretty algorithm to follow these rules:
                1. No consecutive, identical up stands (e.g. E -> E, J -> J)
                2. No circular rotations (e.g. A -> B, B -> C, C -> A; in this situation everyone relieves each other)
                
            These two algorithms are combined with the function call below
            """
            self.reorganizeLifeguardsAtTime(timeToUpStandChoices, i)

    def reorganizeLifeguardsAtTime(
        self, timeToUpStandChoices: dict[Time, list[str]], index: int
    ):
        # Checks

        currentStandChoices = list(timeToUpStandChoices.values())[index].copy()
        if len(currentStandChoices) < 1:
            return

        # Get needed lists / groups / other data
        """
        We need two main groups. They are:
        1. Lifeguards going up twice in a row. These are problematic because this is where the issues actually occur
        2. Lifeguards coming from a down to up. These lifeguards ensure that an outside source is a part of the
        rotation. If all people in a rotation are up on stand, who starts it? (Answer - nobody. That's bad)
        
        We will also need the following information:
        
        Dictionaries:
        1. lifeguardToBlockLength: dict[Lifeguard, int] - this houses the block length of every down to up lifeguard
        2. lifeguardToPreviousStand: dict[Lifeguard, str] - this houses the previous stand of every twice up lifeguard
        3. previousStandToLifeguard: dict[str, Lifeguard] - the inverse of lifeguardToPreviousStand
        
        Lists:
        1. freshStands: list[str] - all of the stands in currentStandChoices that are not in previousStandToLifeguard
        """

        currentTime = list(timeToUpStandChoices.keys())[index]
        currentLifeguardsUp = self.getLifeguardsUpOnStandAtSpecificTime(currentTime)
        random.shuffle(currentLifeguardsUp)

        if index > 0:
            lastTime = list(timeToUpStandChoices.keys())[index - 1]
            lastLifeguardsUp = self.getLifeguardsUpOnStandAtSpecificTime(lastTime)
        else:
            lastTime = None
            lastLifeguardsUp = []

        upTwiceCode = "2^"
        lifeguardsUpTwice = []
        for lifeguard in currentLifeguardsUp:
            if lifeguard in lastLifeguardsUp:
                lifeguardsUpTwice.append(lifeguard)

        downToUpCode = "_ -> ^"
        downToUpLifeguards = self.getLifeguardsComingFromDownAtTime(
            currentLifeguardsUp, currentTime
        )

        # Create block length dictionary

        lifeguardToBlockLength: dict[Lifeguard, int] = {}
        for lifeguard in downToUpLifeguards:
            blockLength = lifeguard.getUpStandsFromTime(currentTime, self._upStands)

            lifeguardToBlockLength[lifeguard] = blockLength

        # Create previous stand dictionary and reverse

        lifeguardToPreviousStand: dict[Lifeguard, str] = {}
        if index > 0:
            lifeguardToPreviousStand: dict[Lifeguard, str] = {}
            for lifeguard in lifeguardsUpTwice:
                previousStand = lifeguard.getStand(lastTime)

                lifeguardToPreviousStand[lifeguard] = previousStand
        previousStandToLifeguard = {v: k for k, v in lifeguardToPreviousStand.items()}

        # Calculate freshStands

        freshStands: list[str] = []
        for stand in currentStandChoices:
            if stand not in previousStandToLifeguard:
                freshStands.append(stand)

        # FUNCTIONS
        """
        The functions below are used to retrieve and implement stand combo data
        """

        # Get the stand combos permutations and remove all those that include stands not present at time

        def getValidPermutations(limit: int) -> dict[int, list[list[str]]]:
            """
            We have three checks here:
            1. all stands must be in currentStandChoices
            2. The last stand cannot be in previousStandToLifeguard IF the length of the permutation is the same
            as the limit (otherwise it doesn't matter because more will be added later if the permutation is
            picked.)
            3. It has to leave fresh stands for other clusters as well (at least one for each cluster left)
            """

            permutations = self._staticAppInfo.getStandComboPermutations()

            maxLimit = len(permutations)
            if limit > maxLimit:
                limit = maxLimit

            clustersNeedingFreshStands = 0
            for hasFreshStand in hasFreshStandList:
                if not hasFreshStand:
                    clustersNeedingFreshStands += 1

            newPermutations: dict[int, list[list[str]]] = {}

            for i in range(1, limit + 1):
                permutationList = list(permutations.get(i, []))

                for p in range(len(permutationList) - 1, -1, -1):
                    permutation = permutationList[p]

                    # Bool of whether it should pop
                    shouldPop = False

                    # Set freshStandCounter
                    freshStandCounter = len(freshStands)

                    # Check every stand
                    for s in range(len(permutation)):
                        thisStand = permutation[s]

                        if thisStand not in currentStandChoices:
                            shouldPop = True

                        if thisStand in freshStands:
                            freshStandCounter -= 1

                    # Check the last stand
                    if i == limit and permutation[-1] in previousStandToLifeguard:
                        shouldPop = True

                    # Check freshStandCounter
                    # We can subtract one from clusters needing fresh stands if we are at the limit because then we
                    # don't need to consider ourselves after this
                    if i == limit:
                        if freshStandCounter < clustersNeedingFreshStands - 1:
                            shouldPop = True
                    elif freshStandCounter < clustersNeedingFreshStands:
                        shouldPop = True

                    # Pop if any of the checks failed
                    if shouldPop:
                        permutationList.pop(p)

                if len(permutationList) > 0:
                    newPermutations[i] = permutationList

            return newPermutations

        # Used to find the stand combo potential of starting with certain stands (function)

        def getStandComboPotential(blockLength: int) -> dict[str, int]:
            standToComboPotential = {}

            permutations = self._staticAppInfo.getStandComboPermutations()

            newPermutations: dict[int, list[list[str]]] = {}

            for i in range(1, blockLength + 1):
                permutationList = list(permutations.get(i, []))

                for p in range(len(permutationList) - 1, -1, -1):
                    permutation = permutationList[p]

                    popped = False
                    for s in range(0, len(permutation)):
                        standList = list(timeToUpStandChoices.values())[index + s]

                        thisStand = permutation[s]

                        if not popped and thisStand not in standList:
                            permutationList.pop(p)

                            popped = True

                if len(permutationList) > 1:
                    newPermutations[i] = permutationList

            permutations = newPermutations

            if len(permutations) < 1:
                return standToComboPotential

            permutationList = list(permutations.values())[-1]

            for permutation in permutationList:
                stand = permutation[0]

                count = standToComboPotential.get(stand, 0)

                standToComboPotential[stand] = count + 1

            return standToComboPotential

        # Create clusters
        """
        The clusters follow the roles describes for the 3 lifeguard groups described above.
        
        The amount of clusters is dependent on the number of down to up lifeguards (significance explain above).
        """
        clusters: list[dict[str, list[Lifeguard | None]]] = []

        clusterLength = len(downToUpLifeguards)

        if clusterLength < 1:
            raise CalculaterException(
                f"reorganizing: no lifeguards going down to up at time {currentTime.get12Time()}"
            )

        # Create empty clusters

        for i in range(clusterLength):
            clusters.append({})

        # Distribute up twice lifeguards WITH stand combos
        """
        The way we pick up-twice lifeguards is:
        1. We find the length of the cluster list that it will be added to
        2. We find the best permutation for this cluster list based on its length
        3. Now the we have the permutation, we match it with the lifeguards who had that as their previous stand. If
        a lifeguard did not have that as a previous stand, a placeholder None is added.
        4. We substitute in lifeguards for all the None placeholders
        """

        hasFreshStandList: list[bool] = []
        for i in range(len(clusters)):
            hasFreshStandList.append(False)

        lifeguardsUpTwiceLen = len(lifeguardsUpTwice)

        permutations: list[list[str | None]] = []
        for i in range(len(clusters)):
            # Set cluster list length and create the empty list

            clusterListLen = lifeguardsUpTwiceLen // len(clusters)

            remainder = lifeguardsUpTwiceLen % len(clusters)

            if i + 1 <= remainder:
                clusterListLen += 1

            # Get the valid permutations and find the most optimal one we will try to accomplish

            permutationLength = clusterListLen + 1

            validPermutations = getValidPermutations(permutationLength)

            permutationList: list[list[str | None]] = []
            while len(validPermutations) >= 2:
                permutation: list[str] = list(validPermutations.values())[-1][0]

                permutationList.append(permutation)

                for s in range(len(currentStandChoices) - 1, -1, -1):
                    stand = currentStandChoices[s]

                    if stand in permutation:
                        currentStandChoices.pop(s)

                permutationLength -= len(permutation)

                validPermutations = getValidPermutations(permutationLength)

            if permutationLength > 0:
                permutation: list[None] = []

                for j in range(permutationLength):
                    permutation.append(None)

                permutationList.append(permutation)

            combPermutationList: list[str | None] = []
            for permutation in permutationList:
                combPermutationList += permutation

            for s in range(len(combPermutationList)):
                stand = combPermutationList[s]

                if stand in freshStands:
                    freshStands.pop(freshStands.index(stand))

                    if s == len(combPermutationList) - 1:
                        hasFreshStandList[i] = True

            permutations.append(combPermutationList)

            # Use each permutation's previous stands to try and find a lifeguard.
            # If we can't find one we'll use None as a placeholder

            lifeguardCluster: list[Lifeguard | None] = []
            for s in range(len(combPermutationList)):
                if s + 1 < len(combPermutationList):
                    stand = combPermutationList[s]

                    lifeguard = previousStandToLifeguard.get(stand)

                    lifeguardCluster.append(lifeguard)

                    if lifeguard is not None:
                        lifeguardsUpTwice.pop(lifeguardsUpTwice.index(lifeguard))

            cluster = clusters[i]

            cluster[upTwiceCode] = lifeguardCluster

        # Holes for stand permutations
        """
        While we were filling in the stands before, we left None placeholders when we weren't able to get a permutation
        to fill out the whole thing. Now, we will go back and fill in these holes with stands so that it prioritizes
        the continuation of fresh stands at the end of a stand sequence.
        """

        for i in range(len(permutations)):
            permutation = permutations[i]

            hasFreshStand = hasFreshStandList[i]

            if not hasFreshStand:
                freshStand = freshStands.pop(random.randrange(len(freshStands)))

                permutation[-1] = freshStand

                currentStandChoices.pop(currentStandChoices.index(freshStand))

        for permutation in permutations:
            for i in range(len(permutation)):
                stand = permutation[i]

                if stand is None:
                    stand = currentStandChoices.pop(
                        random.randrange(len(currentStandChoices))
                    )

                    permutation[i] = stand

        # Distribute down to up lifeguards
        """
        The way we pick down-to-up lifeguards is:
        1. Sort the down-to-up lifeguards based on block length (in max value descending)
        2. Create a list of the first stands
        3. Assign the lifeguards to the first stands based on the potential for their given block length
        """

        sortedDownToUpLifeguards: list[Lifeguard] = []
        for i in range(len(clusters)):
            maxIndex = 0

            maxBlockLength = lifeguardToBlockLength[downToUpLifeguards[0]]

            for j in range(1, len(downToUpLifeguards)):
                blockLength = lifeguardToBlockLength[downToUpLifeguards[j]]

                if blockLength > maxBlockLength:
                    maxBlockLength = blockLength

                    maxIndex = j

            lifeguard = downToUpLifeguards.pop(maxIndex)

            sortedDownToUpLifeguards.append(lifeguard)

        firstStands: list[str] = []
        for permutation in permutations:
            firstStands.append(permutation[0])

        dupeFirstStands = list(firstStands)
        for i in range(len(clusters)):
            maxBlockLength = lifeguardToBlockLength[sortedDownToUpLifeguards[0]]

            lifeguardsWithMaxBlockLength = []
            for lifeguard in sortedDownToUpLifeguards:
                blockLength = lifeguardToBlockLength[lifeguard]

                if blockLength == maxBlockLength:
                    lifeguardsWithMaxBlockLength.append(lifeguard)

            lifeguard = lifeguardsWithMaxBlockLength[
                random.randrange(len(lifeguardsWithMaxBlockLength))
            ]

            sortedDownToUpLifeguards.pop(sortedDownToUpLifeguards.index(lifeguard))

            blockLength = lifeguardToBlockLength[lifeguard]

            standComboPotential = getStandComboPotential(blockLength)

            maxIndex = 0

            maxPotential = standComboPotential.get(dupeFirstStands[0], 0)

            for j in range(1, len(dupeFirstStands)):
                potential = standComboPotential.get(dupeFirstStands[j], 0)

                if potential > maxPotential:
                    maxPotential = potential

                    maxIndex = j

            stand = dupeFirstStands.pop(maxIndex)

            assignmentIndex = firstStands.index(stand)

            cluster = clusters[assignmentIndex]

            cluster[downToUpCode] = [lifeguard]

        # Simplify clusters down to lifeguard groups
        """
        Now that we have designated the lifeguard's spots in the clusters, we can combine both parts of the
        dictionaries together: the up-to-down's and the up-twice's
        """

        lifeguardGroups: list[list[Lifeguard | None]] = []
        for cluster in clusters:
            downToUpLifeguard = cluster.get(downToUpCode)[0]

            upTwiceLifeguards = cluster.get(upTwiceCode, [])

            lifeguards = [downToUpLifeguard] + upTwiceLifeguards

            lifeguardGroups.append(lifeguards)

        # Holes for lifeguards
        """
        While we were filling in the stands for the up-twice lifeguards before, we assigned lifeguards based off the
        stands given. We left holes for when stands would be added later. Now that all the stands are updated, we can
        plug in all the holes!
        """

        for i in range(len(lifeguardGroups)):

            def checkForIssues() -> list[int]:
                issues = []

                for s in range(len(permutation)):
                    stand = permutation[s]

                    if s + 1 < len(permutation):
                        lifeguard = lifeguards[s + 1]

                        if (
                            stand in previousStandToLifeguard
                            and lifeguard != previousStandToLifeguard[stand]
                        ):
                            issues.append(s)
                    else:
                        if stand in previousStandToLifeguard:
                            raise CalculaterException(
                                "Error - should not have a double stand in the last slot"
                            )

                return issues

            permutation = permutations[i]

            lifeguards = lifeguardGroups[i]

            issues = checkForIssues()
            for issueIndex in issues:
                stand = permutation[issueIndex]

                lifeguard = previousStandToLifeguard[stand]

                lifeguards[issueIndex + 1] = lifeguard

                lifeguardsUpTwice.pop(lifeguardsUpTwice.index(lifeguard))

        for i in range(len(lifeguardGroups)):
            group = lifeguardGroups[i]

            for l in range(len(group)):
                lifeguard = group[l]

                if lifeguard is None:
                    newLifeguard = lifeguardsUpTwice.pop(
                        random.randrange(len(lifeguardsUpTwice))
                    )

                    group[l] = newLifeguard

        # Assign stands to lifeguards
        """
        At this point, we have already paired up all the stands and lifeguards.
        Now we just have to assign every stand to its respective lifeguard.
        """

        for i in range(len(lifeguardGroups)):
            lifeguards = lifeguardGroups[i]

            permutation = permutations[i]

            for k in range(len(permutation)):
                stand = permutation[k]

                lifeguard = lifeguards[k]

                lifeguard.addStand(currentTime, stand)

    # Returns up stand names
    def getUpStandNames(self):
        upStandNames = Stand.getStandNames(self._upStands)
        upStandNames.append(self._staticAppInfo.getUpStandCode())

        return upStandNames

    def getLifeguardNames(self) -> list[str]:
        lifeguardNames = []

        for lifeguard in self._lifeguards:
            lifeguardNames.append(lifeguard.getName())

        return lifeguardNames

    def getLifeguardsComingFromUpAtTime(
        self, lifeguards: list[Lifeguard], currentTime: Time
    ) -> list[Lifeguard]:
        lifeguardsComingFromUp = []

        lastTime = Time().setTimeWithMinutes(
            currentTime.getMinutes() - self._staticAppInfo.getTimeInterval()
        )
        for lifeguard in lifeguards:
            if lifeguard.getIsUpOnStand(lastTime, self._upStands):
                lifeguardsComingFromUp.append(lifeguard)

        return lifeguardsComingFromUp

    @staticmethod
    def getLifeguardsComingFromDownAtTime(
        lifeguards: list[Lifeguard], currentTime: Time
    ) -> list[Lifeguard]:
        lifeguardsComingFromDown = []

        for lifeguard in lifeguards:
            if lifeguard.getIntervalsUpOnStand(currentTime) == 0:
                lifeguardsComingFromDown.append(lifeguard)

        return lifeguardsComingFromDown

    def getStandsAtTimeFromLifeguardSchedules(
        self, currentTime: Time, standList: list[Stand] | list[str]
    ):
        standListNames = Stand.getStandNames(standList)

        standsAtTime = []
        for lifeguard in self._lifeguards:
            stand = lifeguard.getStand(currentTime)

            if stand in standListNames:
                standsAtTime.append(stand)

        return standsAtTime

    # Returns a list of lifeguards up on stand at a given time
    def getLifeguardsUpOnStandAtSpecificTime(self, currentTime):
        # Check type of currentTime
        if isinstance(currentTime, Time):
            lifeguardsWorking = self.getLifeguardsWorkingAtASpecificTime(currentTime)

            upStands = Stand.getStandNames(self._upStands)
            upStands.append(self._staticAppInfo.getUpStandCode())

            for i in range(len(lifeguardsWorking) - 1, -1, -1):
                if lifeguardsWorking[i].getStand(currentTime) not in upStands:
                    lifeguardsWorking.pop(i)
            return lifeguardsWorking
        else:
            print("ERROR IN CALCULATE SCHEDULE - gLUOSAST")
            return []

    def getLifeguardsDownOnStandAtASpecificTime(self, currentTime: Time):
        lifeguardsWorking = self.getLifeguardsWorkingAtASpecificTime(currentTime)

        upStands = Stand.getStandNames(self._upStands)
        upStands.append(self._staticAppInfo.getUpStandCode())

        for i in range(len(lifeguardsWorking) - 1, -1, -1):
            if lifeguardsWorking[i].getStand(currentTime) in upStands:
                lifeguardsWorking.pop(i)

        return lifeguardsWorking

    # Returns a list with the stands that are open at that time (works for both up stands and downs stands)
    @staticmethod
    def getStandsOpenAtTime(thisTime: Time, standList: list[Stand]):
        # Create the list where the stands are going to be appended to
        standsToReturn = []

        # Check to make sure the time is a time
        if isinstance(thisTime, Time):
            for stand in standList:
                if stand.isOpen(thisTime):
                    for i in range(stand.getAmountPerInterval()):
                        standsToReturn.append(stand.getName())
        else:
            print("ERROR IN CALCULATE SCHEDULE - gSOAT")

        # Return the created list
        return standsToReturn

    # Gets a list of the lifeguards going on break right now
    # Takes the current time, and then checks if on the NEXT interval it will either be on break or clocking out
    def getLifeguardGoingOnBreakOrClockingOutNext(self, currentTime):
        # Create list
        lifeguardsGoingOnBreakOrClockingOut = []

        # Continue if the type of the parameter time is correct
        if isinstance(currentTime, Time):
            # Create the next time object
            nextTime = Time().setTimeWithMinutes(
                currentTime.getMinutes() + self._staticAppInfo.getTimeInterval()
            )

            # For each lifeguard, check if one of the break times is the given time
            for lifeguard in self._lifeguards:
                if lifeguard.getShiftEndTime().equals(nextTime):
                    lifeguardsGoingOnBreakOrClockingOut.append(lifeguard)
                else:
                    for breakTime in lifeguard.getBreakTimes():
                        if breakTime.equals(nextTime):
                            lifeguardsGoingOnBreakOrClockingOut.append(lifeguard)

        else:  # Print error if the type of time is wrong
            print("ERROR IN CALCULATE SCHEDULE - gLSB")

        # Return the list
        return lifeguardsGoingOnBreakOrClockingOut

    # Sorts the lifeguards in increasing order of their shift start times
    def sortLifeguards(self):
        # Create a list that directly corresponds to the lifeguards of the times of shift starts and ends
        shiftStartAndEnds = []
        for lifeguard in self._lifeguards:
            shiftStartAndEnds.append(
                [lifeguard.getShiftStartTime(), lifeguard.getShiftEndTime()]
            )

        # Sort the times and, by doing so, the lifeguards
        for i in range(0, len(self._lifeguards)):
            # Create the minimum index
            minIndex = i
            # For each lifeguard
            for j in range(i, len(self._lifeguards)):
                # If the shift start times are equal we use the tiebreaker
                # noinspection PyUnresolvedReferences
                if (
                    shiftStartAndEnds[j][0].getMinutes()
                    == shiftStartAndEnds[minIndex][0].getMinutes()
                ):
                    # Tiebreaker is whoever has the early end time is the minimum
                    # noinspection PyUnresolvedReferences
                    if (
                        shiftStartAndEnds[j][1].getMinutes()
                        < shiftStartAndEnds[minIndex][1].getMinutes()
                    ):
                        minIndex = j
                # If the shift start time at j is less than our current minimum, j is the new minimum
                # noinspection PyUnresolvedReferences
                elif (
                    shiftStartAndEnds[j][0].getMinutes()
                    < shiftStartAndEnds[minIndex][0].getMinutes()
                ):
                    minIndex = j

            # Swap in both the lifeguard and the time lists
            tempLifeguard = self._lifeguards[i]
            self._lifeguards[i] = self._lifeguards[minIndex]
            self._lifeguards[minIndex] = tempLifeguard
            tempList = shiftStartAndEnds[i]
            shiftStartAndEnds[i] = shiftStartAndEnds[minIndex]
            shiftStartAndEnds[minIndex] = tempList

    # Assigns the created breaks to lifeguards. The parameter is for if we are using hardcoded breaks
    def assignBreaks(self, automatic=True):
        # Automatically calculate the breaks
        if automatic:
            self.calculateBreaks()

        # Get the lifeguards that actually need breaks (NOTE: IS SORTED)
        lifeguardsWithBreaks = self.getLifeguardsNeedingBreaks()

        # Create a list for lifeguards if they just didn't get a break
        lifeguardsNeedingBreaks = []

        # For each lifeguard, assign the breaks
        for i in range(0, len(lifeguardsWithBreaks)):
            earliestTime, latestTime = lifeguardsWithBreaks[
                i
            ].calculateRangeOfPossibleBreakTimes()

            times = [earliestTime.getMinutes(), self._branchTime.getMinutes()]

            earliestTime = Time().setTimeWithMinutes(max(times))

            if self._breaks[i].getIsInBetweenInclusive(earliestTime, latestTime):
                lifeguardsWithBreaks[i].addBreakTime(self._breaks[i])
            else:
                lifeguardsNeedingBreaks.append(lifeguardsWithBreaks[i])

        # Assign the best possible breaks for lifeguards who the previous algorithm didn't work for
        self.calculateAndAssignLeftoverBreaks(lifeguardsNeedingBreaks)

    # Calculates and assigns the breaks for the lifeguards which the previous algorithm didn't work for
    def calculateAndAssignLeftoverBreaks(self, lifeguardsNeedingBreaks):
        # For each lifeguard in the given list
        for lifeguard in lifeguardsNeedingBreaks:
            # Get the dictionary with all the scores for the lifeguards at each time
            lifeguardsAtTime = self.getLifeguardsOnDutyDict()

            # Get the ratio dictionary
            lifeguardStandRatios = self.getLifeguardToStandRatios(lifeguardsAtTime)

            # Get the time that has the highest ratio of lifeguards scores to stands
            timeWithHighestRatio = self._staticAppInfo.findDictMax(lifeguardStandRatios)

            # Keep on generating times until the time with the highest ratio is within the break range for this specific
            # lifeguard
            # Get the two times for the range
            earliestTime, latestTime = lifeguard.calculateRangeOfPossibleBreakTimes()

            times = [earliestTime.getMinutes(), self._branchTime.getMinutes()]

            earliestTime = Time().setTimeWithMinutes(max(times))

            # While it is still invalid
            while not timeWithHighestRatio.getIsInBetweenInclusive(
                earliestTime, latestTime
            ):
                # Pop out the bad time
                lifeguardStandRatios.pop(timeWithHighestRatio)
                # Recalculate
                timeWithHighestRatio = self._staticAppInfo.findDictMax(
                    lifeguardStandRatios
                )

            # Now with the confirmed best time, assign the break
            lifeguard.addBreakTime(timeWithHighestRatio)
            # print("Leftover algorithm used on lifeguard", lifeguard.getName())

    # Calculates the breaks based on the lifeguard information
    def calculateBreaks(self):
        # List of prospective breaks to give to lifeguards
        breaks = []

        # Create a dictionary of times with the amount of lifeguards at each time
        lifeguardsAtTime = self.getLifeguardsOnDutyDict()
        possibleBreakRange = self.calculateBreakRange()
        self._staticAppInfo.clipDictionaryToTimeRange(
            lifeguardsAtTime, possibleBreakRange
        )

        # Create a new list with the lifeguards to make sure that they all actually need breaks
        lifeguardsWithBreaks = self.getLifeguardsNeedingBreaks()

        # For one iteration per lifeguard
        for i in range(0, len(lifeguardsWithBreaks)):
            # Create a new dictionary where the key is the time and the value is the lifeguards at the time divided
            # by the amount of up stands present
            lifeguardStandRatios = self.getLifeguardToStandRatios(lifeguardsAtTime)

            # Get the time that has the highest ratio of lifeguards scores to stands
            timeWithHighestRatio = self._staticAppInfo.findDictMax(lifeguardStandRatios)
            breaks.append(timeWithHighestRatio)

            # Remove one lifeguard working from the time found to assign the break as well as the times the
            # break will bleed into
            self.reduceLifeguardScore(lifeguardsAtTime, timeWithHighestRatio)

        # Sort the break times
        self._staticAppInfo.sortTimesAscending(breaks)

        # Set the breaks
        self._breaks = breaks

    # Calculates the range of time when breaks are actually feasible throughout the day
    def calculateBreakRange(self):
        # Establish two times, earliest time and latest time
        earliestTime = Time()
        latestTime = Time()

        firstTime = True
        # For each lifeguard in lifeguards, check to see the earliest and latest times
        for lifeguard in self._lifeguards:
            # Get the two times, earliest and latest
            time1 = lifeguard.calculateRangeOfPossibleBreakTimes()[0]
            time2 = lifeguard.calculateRangeOfPossibleBreakTimes()[1]

            # Check if these are the extremes or simply just the first time
            if time1.getMinutes() < earliestTime.getMinutes() or firstTime:
                earliestTime = time1
            if time2.getMinutes() > latestTime.getMinutes() or firstTime:
                latestTime = time2
            firstTime = False

        # Return the created list of the two times
        return [earliestTime, latestTime]

    # Creates a dictionary where the key is the time and the value is the lifeguards working / the amount of up stands
    def getLifeguardToStandRatios(self, lifeguardsAtTime):
        # Create the dictionary
        lifeguardStandRatios = dict()

        # Get the amount of up stands at each time and create a dictionary
        standsAtTime = self.getUpStandsAtTimeDict()

        # For each time in lifeguards at time, create the values of the dictionary
        for thisTime in lifeguardsAtTime:
            # Create time for the key of the ratio
            ratioKeyTime = Time().setTimeWithMinutes(thisTime.getMinutes())

            # Find the equivalent key in standsAtTime
            standKeyTime = Time()
            for standTime in standsAtTime:
                if standTime.equals(thisTime):
                    standKeyTime = standTime
            if standsAtTime[standKeyTime] == 0:
                lifeguardStandRatios[ratioKeyTime] = 0
            else:
                lifeguardStandRatios[ratioKeyTime] = (
                    lifeguardsAtTime[thisTime] / standsAtTime[standKeyTime]
                )

        return lifeguardStandRatios

    # Returns a dictionary with the amount of up stands at every time of the day
    def getUpStandsAtTimeDict(self):
        # Create the dictionary
        upStandsAtTimeDict = dict()

        # For each time of the day record the amount of up stands
        for i in range(0, 1440, self._staticAppInfo.getTimeInterval()):
            # Initialize count to 0
            count = 0

            # Set the time being used for the key
            thisTime = Time().setTimeWithMinutes(i)

            # For each stand in upStandData, check to see if it is open at the given time
            for stand in self._upStands:
                # Get the times of the start and end of the stand
                time1 = stand.getStartTime()
                time2 = stand.getEndTime()

                # Increase count by 1 if the current time is between the start and end of the time
                if thisTime.getIsInBetweenExclusiveEnd(time1, time2):
                    count += 1

            # Set the dictionary value with its proper key
            upStandsAtTimeDict[thisTime] = count

        # Return the created dictionary
        return upStandsAtTimeDict

    # Reduces the lifeguard score by the appropriate amount given a lifeguard is put on break at a time
    def reduceLifeguardScore(self, lifeguardsAtTime, timeWithHighestRatio):
        # For each interval in the break interval
        for j in range(0, self._staticAppInfo.getBreakInterval()):
            # Create the time to remove from going forward
            timeToRemoveFromForward = Time().setTimeWithMinutes(
                timeWithHighestRatio.getMinutes()
                + j * self._staticAppInfo.getTimeInterval()
            )
            # Reduce the lifeguards working score by the calculated amount for the forward time
            for thisTime in lifeguardsAtTime:
                if thisTime.equals(timeToRemoveFromForward):
                    lifeguardsAtTime[thisTime] -= (
                        self._staticAppInfo.getBreakInterval() - j
                    )

            # Only do if j is not 0 (initial time so that it goes like a pyramid)
            if j != 0:
                # Create the time to remove from going backward
                timeToRemoveFromBackward = Time().setTimeWithMinutes(
                    timeWithHighestRatio.getMinutes()
                    - j * self._staticAppInfo.getTimeInterval()
                )
                # Reduce the lifeguards working score by the calculated amount for the backward time
                for thisTime in lifeguardsAtTime:
                    if thisTime.equals(timeToRemoveFromBackward):
                        lifeguardsAtTime[thisTime] -= (
                            self._staticAppInfo.getBreakInterval() - j
                        )

    # Returns a dictionary with a score for the amount of lifeguards at every time of the day (for breaks)
    def getLifeguardsOnDutyDict(self):
        # Define a dictionary that stores each time and the number of lifeguards at the time
        lifeguardsAtTime = dict()

        # Create the dictionary where at each time (key) it describes the amount of lifeguard working at that time
        for i in range(0, 1440, self._staticAppInfo.getTimeInterval()):
            # Set the lifeguard score to 0 (this is what determines is the best time)
            lifeguardScore = 0

            # Set the time being observed
            thisTime = Time().setTimeWithMinutes(i)

            # For each time in the break being observed
            for j in range(0, self._staticAppInfo.getBreakInterval()):
                # Set the time
                timeObserving = Time().setTimeWithMinutes(
                    thisTime.getMinutes() + j * self._staticAppInfo.getTimeInterval()
                )

                # Only count it if the time being observed is before the end of the day (12 AM)
                if timeObserving.getMinutes() < 1440:
                    for lifeguard in self._lifeguards:
                        if lifeguard.isWorking(timeObserving):
                            lifeguardScore += 1
            lifeguardsAtTime[thisTime] = lifeguardScore

        return lifeguardsAtTime

    # Returns the lifeguards list
    def getLifeguards(self) -> list[Lifeguard]:
        return self._lifeguards

    # Returns lifeguards that are working at a specific time
    def getLifeguardsWorkingAtASpecificTime(self, thisTime):
        # Create an empty list that will be appended to
        lifeguardsWorkingAtTime = []

        # Continue if the time is a Time object
        if isinstance(thisTime, Time):
            for lifeguard in self._lifeguards:
                if lifeguard.isWorking(thisTime):
                    lifeguardsWorkingAtTime.append(lifeguard)
        else:
            print("ERROR IN CALCULATE SCHEDULE - time variable not correct for gLWAAST")

        # Return the list
        return lifeguardsWorkingAtTime

    # Returns a list of people who actually have breaks in sorted order
    def getLifeguardsNeedingBreaks(self):
        self.sortLifeguards()
        lifeguardsNeedingBreaks = []
        for lifeguard in self._lifeguards:
            if lifeguard.getNumBreaks() > 0 and len(lifeguard.getBreakTimes()) < 1:
                lifeguardsNeedingBreaks.append(lifeguard)
        return lifeguardsNeedingBreaks

    # Returns the time range between when the first lifeguard enters to when the last lifeguard leaves
    def calculatePoolOpenTimeRange(self) -> tuple[Time, Time]:
        # Set variables for the earliest time and the latest time
        earliestTime = Time()
        latestTime = Time()
        if len(self._lifeguards) > 0:
            earliestTime = self._lifeguards[0].getShiftStartTime()
            latestTime = self._lifeguards[0].getShiftEndTime()

        # Check the start and end of each lifeguard and change the earliest time and latest time variables if needed
        for i in range(1, len(self._lifeguards)):
            lifeguard = self._lifeguards[i]
            if lifeguard.getShiftStartTime().getMinutes() < earliestTime.getMinutes():
                earliestTime = lifeguard.getShiftStartTime()
            if lifeguard.getShiftEndTime().getMinutes() > latestTime.getMinutes():
                latestTime = lifeguard.getShiftEndTime()

        # Return a list that is the pair of the two times together
        return earliestTime, latestTime

    # Prints the schedule (good for testing)
    def printSchedule(self):
        # Establish space length
        spaceLength = 4

        # Print the first two lines
        line = ""
        # Header
        line += "Schedule" + "|"
        # Lifeguard numbers up top
        for lifeguard in self._lifeguards:
            line += (
                (spaceLength - len(str(lifeguard.getIdNum()))) * " "
                + str(lifeguard.getIdNum())
                + "|"
            )

        # Print the line and then the line of dashes'
        dashLength = len(line)
        print(line)
        print("-" * dashLength)

        # Get the time range
        timeRange = self.calculatePoolOpenTimeRange()
        earliestTime = timeRange[0]
        latestTime = timeRange[1]

        for t in range(
            earliestTime.getMinutes(),
            latestTime.getMinutes(),
            self._staticAppInfo.getTimeInterval(),
        ):
            # Create a variable for the current line
            line = ""

            # Set the current time
            currentTime = Time().setTimeWithMinutes(t)

            # Set the last time
            lastTime = Time().setTimeWithMinutes(
                t - self._staticAppInfo.getTimeInterval()
            )

            # Set the next time
            nextTime = Time().setTimeWithMinutes(
                t + self._staticAppInfo.getTimeInterval()
            )

            # Add to the line
            line += currentTime.get12Time() + "|"

            currentUpStands = self.getStandsAtTimeFromLifeguardSchedules(
                currentTime, self._upStands
            )

            lastUpStands = self.getStandsAtTimeFromLifeguardSchedules(
                lastTime, self._upStands
            )

            nextUpStands = self.getStandsAtTimeFromLifeguardSchedules(
                nextTime, self._upStands
            )
            # Add each lifeguard's stand at this time
            for lifeguard in self._lifeguards:
                stand = lifeguard.getStand(currentTime)

                if stand is None:
                    standLength = 0
                else:
                    standLength = len(stand)

                if stand is None:
                    stand = ""
                elif stand == self._staticAppInfo.getUpStandCode():
                    stand = "UP"
                    standLength = len(stand)
                elif stand == self._staticAppInfo.getBreakCode():
                    stand = "\033[93m YYY\033[0m"
                elif stand == self._staticAppInfo.getEmptyCode():
                    stand = "\033[38;2;160;82;45m  NA\033[0m"
                elif (
                    stand in currentUpStands
                    and stand not in lastUpStands
                    and stand not in nextUpStands
                ):
                    stand = f"\033[38;5;208m{stand}\033[0m"
                elif stand in currentUpStands and stand not in lastUpStands:
                    stand = f"\033[92m{stand}\033[0m"
                elif stand in currentUpStands and stand not in nextUpStands:
                    stand = f"\033[91m{stand}\033[0m"
                elif stand not in currentUpStands:
                    stand = f"\033[96m{stand}\033[0m"

                line += (spaceLength - standLength) * " " + stand + "|"

            # Print the time
            print(line)
            print("-" * dashLength)

    # Resets the schedule
    def resetSchedule(self):
        for lifeguard in self._lifeguards:
            lifeguard.resetLifeguardSchedule(self._branchTime)

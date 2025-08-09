# Import libraries
from Time import Time


# This class is meant to store basic information about a stand
class Stand:
    # Constructor
    def __init__(
        self,
        name,
        standType,
        isAllDay=False,
        startTime=Time(),
        endTime=Time(),
        amountPerInterval=1,
    ):
        # Initialize the instance variables
        # Initialize the name
        if isinstance(name, str):
            self._name = name
        else:
            print("ERROR IN STAND - NAME")
            self._name = "ERROR"

        # Initialise the stand type
        if isinstance(standType, str):
            self._standType = standType
        else:
            self._standType = "ERROR NO STAND TYPE"
            print("ERROR IN STAND - STAND TYPE")

        # Initialize whether it is all day or not
        if isinstance(isAllDay, bool):
            self._isAllDay = isAllDay
        else:
            self._isAllDay = False

        # Initialize times
        self._startTime = Time()
        self._endTime = Time()
        if not isAllDay:
            # Initialize the start time
            if isinstance(startTime, Time):
                self._startTime = startTime
            else:
                print("ERROR IN STAND - START TIME")
                self._startTime = Time()

            # Initialize the end time
            if isinstance(endTime, Time):
                self._endTime = endTime
            else:
                print("ERROR IN STAND - END TIME")
                self._endTime = Time()

            # Check if the start time is before the end time
            if self._startTime.getMinutes() > self._endTime.getMinutes():
                print("ERROR IN STAND - START TIME BEFORE END TIME")

        # Initialize the count for the amount per interval
        if isinstance(amountPerInterval, int):
            self._amountPerInterval = amountPerInterval
        else:
            self._amountPerInterval = 1

    # Returns the amount per interval
    def getAmountPerInterval(self):
        return self._amountPerInterval

    # Returns whether the stand is open at a given time
    def isOpen(self, time):
        if self._isAllDay:
            return True
        if isinstance(time, Time):
            return time.getIsInBetweenExclusiveEnd(self._startTime, self._endTime)
        print("ERROR IN STAND - IS OPEN")

    # Returns the name
    def getName(self):
        return self._name

    # Sets the name
    def setName(self, name):
        if isinstance(name, str):
            self._name = name
        else:
            print("ERROR IN STAND - SETTING NAME")

    # Returns the stand type
    def getStandType(self):
        return self._standType

    # Sets the stand type
    def setStandType(self, standType):
        if isinstance(standType, str):
            self._standType = standType
        else:
            print("ERROR IN STAND - SETTING STAND TYPE")

    # Returns whether it is all day or not
    def isAllDay(self):
        return self._isAllDay

    # Sets whether it is all day or not
    def setIsAllDay(self, isAllDay):
        if isinstance(isAllDay, bool):
            self._isAllDay = isAllDay
        else:
            print("ERROR IN STAND - SETTING IS ALL DAY")

    # Gets the start time
    def getStartTime(self):
        return self._startTime

    # Sets the start time
    def setStartTime(self, time):
        if isinstance(time, Time):
            self._startTime = time
        else:
            print("ERROR IN STAND - SETTING IS START TIME")

    # Gets the end time
    def getEndTime(self):
        return self._endTime

    # Sets the end time
    def setEndTime(self, time):
        if isinstance(time, Time):
            self._endTime = time
        else:
            print("ERROR IN STAND - SETTING IS END TIME")

    @staticmethod
    def getStandNames(standList):
        standNames = []
        for stand in standList:
            if isinstance(stand, Stand):
                standNames.append(stand.getName())
            elif isinstance(stand, str):
                standNames.append(stand)
            else:
                raise TypeError(f"expected type Stand or type str, got {type(stand)}")

        return standNames

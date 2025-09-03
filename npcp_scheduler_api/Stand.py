# Import libraries
from Time import Time


# This class is meant to store basic information about a stand
class Stand:
    # Constructor
    def __init__(
        self,
        name,
        times,
        isAllDay=False,
        amountPerInterval=1,
    ):
        # Initialize the instance variables
        # Initialize the name
        if isinstance(name, str):
            self._name = name
        else:
            print("ERROR IN STAND - NAME")
            self._name = "ERROR"

        # Initialize whether it is all day or not
        if isinstance(isAllDay, bool):
            self._isAllDay = isAllDay
        else:
            self._isAllDay = False

        # Initialize times
        self._times = times

        # Initialize the count for the amount per interval
        if isinstance(amountPerInterval, int):
            self._amountPerInterval = amountPerInterval
        elif isinstance(amountPerInterval, str):
            try:
                newAmountPerInterval = int(amountPerInterval)
            except (ValueError, TypeError):
                newAmountPerInterval = 1
            self._amountPerInterval = newAmountPerInterval
        else:
            self._amountPerInterval = 1

    # Returns the amount per interval
    def getAmountPerInterval(self):
        return self._amountPerInterval

    # Returns whether the stand is open at a given time
    def isOpen(self, givenTime):
        if self._isAllDay:
            return True
        if isinstance(givenTime, Time):
            for scheduleTime in self._times:
                if scheduleTime.getMinutes() == givenTime.getMinutes():
                    return True
            return False
        raise TypeError("Expected Time object for function isOpen in Stand")

    # Returns the name
    def getName(self):
        return self._name

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

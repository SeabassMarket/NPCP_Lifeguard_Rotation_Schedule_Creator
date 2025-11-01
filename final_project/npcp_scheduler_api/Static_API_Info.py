# import libraries
from Time import Time
from Stand import Stand


# This class will contain static info that is shared across different
# classes and level
class StaticAPIInfo:
    # Numbers
    timeInterval = 20  # The time interval to be used between event times
    longestTimeWorking = (
        300  # The longest amount of time a lifeguard is consecutively allowed to work
    )
    breakTime = 40  # How long a lifeguard's break is

    # Codes
    standCombos = {
        "T": ["S"],
        "C": ["E"],
        "A": ["B", "C"],
        "J": ["K"],
        "H": ["I", "K"],
        "E": ["H", "K"],
        "F": ["G"],
        "I": ["K", "J"],
        "K": ["H"],
        "B": ["A"],
    }
    upStandCode: str = "UP STAND"
    breakCode: str = "BREAK"
    emptyCode: str = "EMPTY"

    # Construct the object, this class will just house some variables used across classes
    def __init__(self, data):
        self._data = data

    @property
    def data(self):
        return self._data

    # Returns how many intervals long the break time is
    @staticmethod
    def getBreakInterval():
        return int(StaticAPIInfo.breakTime / StaticAPIInfo.timeInterval)

    # Finds the key in a dictionary that has the highest value (provided each value is an int/float)
    # NOTE: It will return the last key that has the max value
    @staticmethod
    def findDictMax(dictionary):
        # Confirm that dictionary is a dictionary
        if isinstance(dictionary, dict) and len(dictionary) > 0:
            # Set the max key to the first term in the dictionary
            maxKey = list(dictionary.keys())[0]

            # Iterate through the dictionary to check and see if a value is greater, if yes change maxKey
            for key in dictionary:
                if dictionary[key] >= dictionary[maxKey]:
                    maxKey = key

            return maxKey

        # Otherwise return an error
        print("TYPE ERROR, findDictMax")
        return "ERROR"

    # Removes values from a dictionary where the keys are times if the keys are not within the given range defined by the
    # two-time list provided as a parameter
    @staticmethod
    def clipDictionaryToTimeRange(dictionary, timeRange):
        # Exit function with error if types are incorrect
        if not isinstance(dictionary, dict):
            print("TYPE ERROR, clipDictionaryToTimeRange")
            return "ERROR"
        if not isinstance(timeRange, list):
            print("TYPE ERROR, clipDictionaryToTimeRange")
            return "ERROR"
        if not isinstance(timeRange[0], Time) or not isinstance(timeRange[1], Time):
            print("TYPE ERROR, clipDictionaryToTimeRange")
            return "ERROR"

        # Initialize the two time variables
        earlyTime = timeRange[0]
        lateTime = timeRange[1]

        # For each time in the dictionary, pop it out if it is not within the given time range
        timesToPop = []
        for time in dictionary:
            if not time.getIsInBetweenInclusive(earlyTime, lateTime):
                timesToPop.append(time)
        for time in timesToPop:
            dictionary.pop(time)

        return "SUCCESS"

    # Sorts a list of times in ascending order
    @staticmethod
    def sortTimesAscending(timesList):
        # Run through each value of the list
        for i in range(0, len(timesList)):
            # Set the minimum index to i
            minIndex = i
            # From i to the rest of the list, find the minimum value so we can swap it
            for j in range(i, len(timesList)):
                if timesList[j].getMinutes() < timesList[minIndex].getMinutes():
                    minIndex = j

            # Swap the values at i and minIndex
            tempTime = timesList[i]
            timesList[i] = timesList[minIndex]
            timesList[minIndex] = tempTime

    # Prints a dictionary that has been created recursively and the last values are lists
    @staticmethod
    def printRecursivelyLongDictionary(dictionary, depth=None):
        # Set the depth if it is None
        if depth is None:
            depth = []

        # If it is a dictionary
        if isinstance(dictionary, dict):
            for key in dictionary:
                # Print where it currently is
                print(len(depth) * "-->" + str(key), "{")

                # Prepare the next one
                # Create a duplicate of depth
                newDepth = list(depth)
                newDepth.append(key)
                StaticAPIInfo.printRecursivelyLongDictionary(dictionary[key], newDepth)
                print(len(depth) * "-->" + "}")

        # If it is a list
        if isinstance(dictionary, list):
            print(len(depth) * "-->", end="")
            print(dictionary)

    @staticmethod
    def getStandComboPermutations(
        permutations: dict[int, list[list[str]]] = None, depth: list[str] = None
    ) -> dict[int, list[list[str]]]:
        if permutations is None:
            permutations = {}

        if depth is None:
            depth = []

        def addPermutation(permutation: list[str]):
            permutation = list(permutation)

            length = len(permutation)

            permutationsOfSameLength = permutations.get(length)

            if permutationsOfSameLength is None:
                permutations[length] = [permutation]
            else:
                permutationsOfSameLength.append(permutation)

        if len(depth) < 1:
            for stand in StaticAPIInfo.standCombos:
                newDepth = [stand]

                StaticAPIInfo.getStandComboPermutations(permutations, newDepth)
                addPermutation(newDepth)
        else:
            possibleCombos = StaticAPIInfo.standCombos.get(depth[-1])

            if possibleCombos is None:
                return permutations

            for combo in possibleCombos:
                if combo not in depth:
                    newDepth = list(depth)

                    newDepth.append(combo)

                    StaticAPIInfo.getStandComboPermutations(permutations, newDepth)
                    addPermutation(newDepth)

        return permutations

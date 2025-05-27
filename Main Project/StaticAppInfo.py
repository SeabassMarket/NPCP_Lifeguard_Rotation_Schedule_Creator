#import libraries
from Time import Time
import tkinter as tk
from tkinter import ttk
from tkinter import font

#This class will contain static info that is shared across different
#classes and level
class StaticAppInfo:
    #Construct the object, this class will just house some variables
    #And values that are used by the classes, such as background colors
    def __init__(self, root):

        #Instantiate root
        self._root = root

        #Global
        self._colors = dict() #Colors to use in the app
        self._fonts = dict()  #Fonts to use in the app
        self._buttonsToDisable = [] #Buttons that are disabled when necessary
        self._fullEvents = dict() #A dictionary full of the event names
        self._eventData = dict() #A dictionary full of the event names AND times
        self._enterAndExit = dict() #A dictionary with scrollable widgets
        self._currentWidget = "" #Global reference of what the current widget is

        #Numbers
        self._timeInterval = 20  # The time interval to be used between event times
        self._longestTimeWorking = 300 # The longest amount of time a lifeguard is consecutively allowed to work
        self._breakTime = 40 # How long a lifeguard's break is

        #For calculations
        self._standCombos = {
            "A": ["B", "C"],
            "B": [],
            "C": ["E"],
            "J": ["K"],
            "E": ["K", "H"],
            "F": ["G"],
            "G": [],
            "H": ["I", "K"],
            "I": ["K"],
            "K": [],
            "T": ["S"],
            "S": [],
        }

        self._count = 0

    def incrementCount(self):
        self._count += 1

    def getCount(self):
        return self._count

    #Returns the stand combos
    def getStandCombos(self):
        return self._standCombos

    #Returns how many intervals long the break time is
    def getBreakInterval(self):
        return int(self._breakTime / self._timeInterval)

    #Returns how long a lifeguard's break is
    def getBreakTime(self):
        return self._breakTime

    #Returns the longest amount of time a lifeguard is consecutively allowed to work
    def getLongestTimeWorking(self):
        return self._longestTimeWorking

    #Scrolling
    @staticmethod
    def onMouseWheel(event, canvas):
        if canvas and canvas.winfo_exists():
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

    #Instantiate global canvas scrolling
    def instantiateScrolling(self):
        for key in self._enterAndExit:
            if key == self._currentWidget:
                frame = self._enterAndExit[key][0]
                canvas = self._enterAndExit[key][1]
                root = self._enterAndExit[key][2]
                if root and root.winfo_exists():
                    frame.update_idletasks()
                    canvas.config(scrollregion=canvas.bbox("all"))
                    canvas.bind_all("<MouseWheel>", lambda event: self.onMouseWheel(event, canvas))
        self._root.after(100, lambda : self.instantiateScrolling())

    #Called whenever a canvas is entered
    def onEnter(self, event):
        widget = event.widget
        for key in self._enterAndExit:
            if self._enterAndExit[key][1] == widget:
                self._currentWidget = key

    #Adds an entry to the enter and exit dictionary
    def addEnterAndExit(self, name, threeValueList):
        self._enterAndExit[name] = threeValueList

    #Returns the enter and exit dictionary (KEEP IN MIND, REFERENCE)
    def getEnterAndExit(self):
        return self._enterAndExit

    #Sets the amount of time between each event
    def setTimeInterval(self, interval):
        if isinstance(interval, int):
            self._timeInterval = interval
        else:
            self._timeInterval = 20

    #Gets the amount of time between each event
    def getTimeInterval(self):
        return self._timeInterval

    #Grabs the full events list depending on the descriptor
    def getCopyFullEventsSpecific(self, eventDescriptor):
        if eventDescriptor in self._fullEvents:
            if isinstance(self._fullEvents[eventDescriptor], list):
                return list(self._fullEvents[eventDescriptor])
        return []

    #Gets the reference to the full events (USE WITH CAUTION)
    def getReferenceFullEventsSpecific(self, eventDescriptor):
        if eventDescriptor in self._fullEvents:
            return self._fullEvents[eventDescriptor]
        return []

    #Remove events from the full events list for that type
    def removeEventsFromFullList(self, eventNames, eventDescriptor):
        events = self.getReferenceFullEventsSpecific(eventDescriptor)
        for i in range(len(events) - 1, -1, -1):
            if events[i] in eventNames:
                events.pop(i)

    #Adds events to the full events lists for that type
    def addEventsToFullListSpecific(self, eventsToAdd, eventDescriptor):
        events = self.getReferenceFullEventsSpecific(eventDescriptor)
        for event in eventsToAdd:
            events.append(event)

    #Creates a new spot in the dictionary for a certain event descriptor
    def addTypeEventToDict(self, eventDescriptor):
        self._fullEvents[eventDescriptor] = []

    #Appends a button to buttons to disable
    def appendButtonToDisable(self, button):
        if isinstance(button, ttk.Button):
            self._buttonsToDisable.append(button)

    #Gets the buttons to disable
    def getButtonsToDisable(self):
        return self._buttonsToDisable

    #Adds a list of buttons to the buttons to disable list
    def appendButtonListToDisable(self, buttons):
        for button in buttons:
            self.appendButtonToDisable(button)

    #Disables buttons in buttons to disable
    def disableButtons(self):
        for button in self._buttonsToDisable:
            button.config(state=tk.DISABLED)

    #Enables buttons in buttons to disable
    def enableButtons(self):
        for button in self._buttonsToDisable:
            button.config(state=tk.NORMAL)

    #Removes all the buttons found in a list from the buttons to disable list
    def removeButtonsFromListToDisable(self, buttons):
        for i in range(len(self._buttonsToDisable) - 1, -1 , -1):
            if self._buttonsToDisable[i] in buttons:
                self._buttonsToDisable.pop(i)

    #Sets the event data to a dictionary (no need for input validation because
    #the functions that use this already validate)
    def setEventDataSpecific(self, eventData, eventDescriptor):
        self._eventData[eventDescriptor] = eventData

    #Returns event data (BE CAREFUL - THIS IS A REFERENCE)
    def getEventDataSpecific(self, eventDescriptor):
        return self._eventData[eventDescriptor]

    #Returns the eventData PERIOD (REFERENCE, CAUTION)
    def getEventData(self):
        return self._eventData

    #Adds a type of event to event data
    def addEventDataSpecific(self, eventDescriptor):
        self._eventData[eventDescriptor] = dict()

    #Adds a new font
    def addFont(self, name, newFont):
        if isinstance(newFont, font.Font) and isinstance(name, str):
            self._fonts[name.lower()] = newFont

    #Returns fonts (RETURNS REFERENCE)
    def getFonts(self):
        return self._fonts

    #Returns a specific font (if it doesn't exist it returns a basic default font)
    def getFont(self, name):
        if name.lower() in self._fonts:
            return self._fonts[name.lower()]
        return font.Font(family="Arial", size=20)

    #Adds a new color
    def addColor(self, name, newColor):
        if isinstance(name, str) and len(newColor) == 7 and newColor[0] == "#":
            valid = True
            for i in range(1, len(newColor)):
                if not (newColor[i].isalpha() or newColor[i].isdigit()):
                    valid = False
            if valid:
                self._colors[name.lower()] = newColor

    #Returns colors (RETURNS REFERENCE)
    def getColors(self):
        return self._colors

    #Returns a specific color (if it doesn't exist it returns black)
    def getColor(self, name):
        if name.lower() in self._colors:
            return self._colors[name.lower()]
        return "#000000"

    #Capitalizes the first letter in each word of a string
    @staticmethod
    def capitalizeTitle(ogString):
        newString = ""
        for i in range(len(ogString)):
            if i == 0:
                newString += ogString[i].upper()
            elif ogString[i-1] == " " or ogString[i-1] == "-":
                newString += ogString[i].upper()
            else:
                newString += ogString[i]
        return newString

    #Finds the key in a dictionary that has the highest value (provided each value is an int/float)
    #NOTE: It will return the last key that has the max value
    @staticmethod
    def findDictMax(dictionary):

        #Confirm that dictionary is a dictionary
        if isinstance(dictionary, dict) and len(dictionary) > 0:

            #Set the max key to the first term in the dictionary
            maxKey = list(dictionary.keys())[0]

            #Iterate through the dictionary to check and see if a value is greater, if yes change maxKey
            for key in dictionary:
                if dictionary[key] >= dictionary[maxKey]:
                    maxKey = key

            return maxKey

        #Otherwise return an error
        print("TYPE ERROR, findDictMax")
        return "ERROR"

    #Removes values from a dictionary where the keys are times if the keys are not within the given range defined by the
    #two-time list provided as a parameter
    @staticmethod
    def clipDictionaryToTimeRange(dictionary, timeRange):

        #Exit function with error if types are incorrect
        if not isinstance(dictionary, dict):
            print("TYPE ERROR, clipDictionaryToTimeRange")
            return "ERROR"
        if not isinstance(timeRange, list):
            print("TYPE ERROR, clipDictionaryToTimeRange")
            return "ERROR"
        if not isinstance(timeRange[0], Time) or not isinstance(timeRange[1], Time):
            print("TYPE ERROR, clipDictionaryToTimeRange")
            return "ERROR"

        #Initialize the two time variables
        earlyTime = timeRange[0]
        lateTime = timeRange[1]

        #For each time in the dictionary, pop it out if it is not within the given time range
        timesToPop = []
        for time in dictionary:
            if not time.getIsInBetweenInclusive(earlyTime, lateTime):
                timesToPop.append(time)
        for time in timesToPop:
            dictionary.pop(time)

    #Sorts a list of times in ascending order
    @staticmethod
    def sortTimesAscending(timesList):

        #Run through each value of the list
        for i in range(0, len(timesList)):

            #Set the minimum index to i
            minIndex = i
            #From i to the rest of the list, find the minimum value so we can swap it
            for j in range(i, len(timesList)):
                if timesList[j].getMinutes() < timesList[minIndex].getMinutes():
                    minIndex = j

            #Swap the values at i and minIndex
            tempTime = timesList[i]
            timesList[i] = timesList[minIndex]
            timesList[minIndex] = tempTime

    #Swaps items in a list given the indexes
    @staticmethod
    def swapItems(givenList, index1, index2):

        if isinstance(givenList, list) and isinstance(index1, int) and isinstance(index2, int):
            temp = givenList[index1]
            givenList[index1] = givenList[index2]
            givenList[index2] = temp
        else:
            print("ERROR IN STATIC APP INFO - swap Items")

    #Prints a dictionary that has been created recursively and the last values are lists
    def printRecursivelyLongDictionary(self, dictionary, depth=None):

        #Set the depth if it is None
        if depth is None:
            depth = []

        #If it is a dictionary
        if isinstance(dictionary, dict):
            for key in dictionary:
                #Print where it currently is
                print(len(depth) * "-->"  + str(key), "{")

                #Prepare the next one
                # Create a duplicate of depth
                newDepth = list(depth)
                newDepth.append(key)
                self.printRecursivelyLongDictionary(dictionary[key], newDepth)
                print(len(depth) * "-->" + "}")

        #If it is a list
        if isinstance(dictionary, list):
            print(len(depth) * "-->", end="")
            print(dictionary)
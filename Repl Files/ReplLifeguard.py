# Imports time class
from ReplSchedule import Schedule
from ReplTime import Time

# Create a module-level Time object
defaultTime = Time(0, 0)


# Creates a lifeguard object to store information and data about a lifeguard
class Lifeguard:

    # Constructs the lifeguard object
    def __init__(self,
                 number=-1,
                 shiftStart=defaultTime,
                 shiftEnd=defaultTime,
                 name="unnamed",
                 stands=None,
                 breakStart=defaultTime,
                 breakEnd=defaultTime,
                 randomChance=0):
        self.setLifeguard(number,
                          shiftStart,
                          shiftEnd,
                          name,
                          stands,
                          breakStart,
                          breakEnd, randomChance)

    # Getters

    def getLifeguard(self):
        return Lifeguard(self._number, self._shiftStart, self._shiftEnd, self._name,
                         self._stands, self._breakStart, self._breakEnd)

    def getNumber(self):
        return self._number

    def getShiftStart(self):
        return Time(self._shiftStart.get24Hour(), self._shiftStart.getMinute())

    def getReferenceShiftStart(self):
        return self._shiftStart

    def getShiftEnd(self):
        return Time(self._shiftEnd.get24Hour(), self._shiftEnd.getMinute())

    def getReferenceShiftEnd(self):
        return self._shiftEnd

    def getName(self):
        return self._name

    def getStands(self):
        return dict(self._stands)

    def getReferenceStands(self):
        return self._stands

    def getBreakStart(self):
        return Time(self._breakStart.get24Hour(), self._breakStart.getMinute())

    def getReferenceBreakStart(self):
        return self._breakStart

    def getBreakEnd(self):
        return Time(self._breakEnd.get24Hour(), self._breakEnd.getMinute())

    def getReferenceBreakEnd(self):
        return self._breakEnd

    def getRandomChance(self):
        return self._randomChance

    def isOnShift(self, currentTime):
        if isinstance(currentTime, Time):
            return (self._shiftStart.getMinutes() <= currentTime.getMinutes() and
                    self._shiftEnd.getMinutes() > currentTime.getMinutes())

    def isOnBreak(self, currentTime):
        if isinstance(currentTime, Time):
            return (self._breakStart.getMinutes() <= currentTime.getMinutes() and
                    self._breakEnd.getMinutes() > currentTime.getMinutes())

    def isWorking(self, currentTime):
        if isinstance(currentTime, Time):
            return self.isOnShift(currentTime) and not self.isOnBreak(currentTime)
        return False

    def getShiftLength(self):
        return Time().setTimeWithMinutes(self._shiftEnd.getMinutes()
                                         - self._shiftStart.getMinutes())

    def getBreakLength(self):
        return Time().setTimeWithMinutes(self._breakEnd.getMinutes()
                                         - self._breakStart.getMinutes())

    def getTimeUntilBreak(self, currentTime):
        if isinstance(currentTime, Time):
            return Time().setTimeWithMinutes(self._breakStart.getMinutes()
                                             - currentTime.getMinutes())
        return Time()

    def getTimeIntoShift(self, currentTime):
        if isinstance(currentTime, Time):
            return Time().setTimeWithMinutes(currentTime.getMinutes()
                                             - self._shiftStart.getMinutes())
        return Time()

    def getTimeLeftShift(self, currentTime):
        if isinstance(currentTime, Time):
            return Time().setTimeWithMinutes(self._shiftEnd.getMinutes()
                                             - currentTime.getMinutes())
        return Time()

    def getStandsUp(self, currentTime, schedule):
        count = 0
        if isinstance(currentTime, Time) and self.isOnShift(currentTime):
            done = False
            time = currentTime.getMinutes()
            while not done:
                closestSmallerTime = self.getShiftStart().getMinutes()
                for key in self._stands:
                    if (key < time and time - closestSmallerTime > time - key):
                        closestSmallerTime = key
                if (closestSmallerTime == time or
                        self._stands[closestSmallerTime] in schedule.getTotalDownStands()):
                    done = True
                else:
                    time = closestSmallerTime
                    count = count + 1
        return count

    def getPriorStandTime(self, currentTime):
        if isinstance(currentTime, Time):
            closestSmallerTime = self.getShiftStart().getMinutes()
            for key in self._stands:
                if (key < currentTime.getMinutes() and currentTime.getMinutes() -
                        closestSmallerTime > currentTime.getMinutes() - key):
                    closestSmallerTime = key
            return Time().setTimeWithMinutes(closestSmallerTime)
        return Time()

    # Setters
    def setNumber(self, number):
        if isinstance(number, int):
            self._number = number
        return self

    def setShiftStart(self, shiftStart):
        if isinstance(shiftStart, Time):
            self._shiftStart = shiftStart
        return self

    def setShiftEnd(self, shiftEnd):
        if isinstance(shiftEnd, Time):
            self._shiftEnd = shiftEnd
        return self

    def setName(self, name):
        if isinstance(name, str):
            self._name = name
        return self

    def setStands(self, stands):
        if isinstance(stands, dict):
            allNumbers = True
            allStrings = True
            for key, value in stands.items():
                if not isinstance(key, int):
                    allNumbers = False
                if not isinstance(value, str):
                    allStrings = False
            if allStrings and allNumbers:
                self._stands = stands
        return self

    def setBreakStart(self, breakStart):
        if isinstance(breakStart, Time):
            self._breakStart = breakStart
        return self

    def setBreakEnd(self, breakEnd):
        if isinstance(breakEnd, Time):
            self._breakEnd = breakEnd
        return self

    def setRandomChance(self, randomChance):
        if isinstance(randomChance, int):
            self._randomChance = randomChance
        return self

    def setLifeguard(self,
                     number=-1,
                     shiftStart=defaultTime,
                     shiftEnd=defaultTime,
                     name="unnamed",
                     stands=None,
                     breakStart=defaultTime,
                     breakEnd=defaultTime,
                     randomChance=0):
        if isinstance(number, int):
            self._number = number
        else:
            self._number = -1
        if isinstance(shiftStart, Time):
            self._shiftStart = shiftStart
        else:
            self._shiftStart = defaultTime
        if isinstance(shiftEnd, Time):
            self._shiftEnd = shiftEnd
        else:
            self._shiftEnd = defaultTime
        if isinstance(name, str):
            self._name = name
        else:
            self._name = "unnamed"
        if isinstance(stands, dict):
            allNumbers = True
            allStrings = True
            for key, value in stands.items():
                if not isinstance(key, int):
                    allNumbers = False
                if not isinstance(value, str):
                    allStrings = False
            if allStrings and allNumbers:
                self._stands = stands
            else:
                self._stands = {}
        else:
            self._stands = {}
        if isinstance(breakStart, Time):
            self._breakStart = breakStart
        else:
            self._breakStart = defaultTime
        if isinstance(breakEnd, Time):
            self._breakEnd = breakEnd
        else:
            self._breakEnd = defaultTime
        time = self.getShiftStart()
        if len(self._stands) == 0:
            while time.getMinutes() < self._shiftEnd.getMinutes():
                if self.isOnBreak(time):
                    self._stands[time.getMinutes()] = "Y"
                else:
                    self._stands[time.getMinutes()] = "NA"
                time.addMinutes(20)
        if isinstance(randomChance, int):
            self._randomChance = randomChance
        else:
            self._randomChance = 0
        return self

    # Mutators
    def updateBreaksInStands(self):
        time = self.getShiftStart()
        while time.getMinutes() < self._shiftEnd.getMinutes():
            if self.isOnBreak(time):
                self._stands[time.getMinutes()] = "Y"
            time.addMinutes(20)
        return self
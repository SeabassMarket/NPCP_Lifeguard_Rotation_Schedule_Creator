# Creates a time object to make it easier to add and subtract times
class Time:

    # Constructor, builds the time object
    def __init__(self, hour=0, minute=0):
        if isinstance(hour, int) and isinstance(minute, int):
            self._hour = (hour + minute // 60) % 24
            self._minute = minute % 60
        else:
            self._hour = 0
            self._minute = 0

    # Getters
    def getTime(self):
        return Time(self._hour, self._minute)

    def get12Hour(self):
        if self._hour > 12:
            return [self._hour - 12, "PM"]
        return [self._hour, "AM"]

    def get24Hour(self):
        return self._hour

    def getMinute(self):
        return self._minute

    def getMinutes(self):
        return self._hour * 60 + self._minute

    def get24Time(self):
        return "%02d:%02d" % (self._hour, self._minute)

    def get12Time(self):
        return "%02d:%02d %s" % (self.get12Hour()[0], self.getMinute(), self.get12Hour()[1])

    # Setters
    def setHour(self, hour):
        if isinstance(hour, int):
            self._hour = hour % 24
        return self

    def setMinute(self, minute):
        if isinstance(minute, int):
            self._hour = (self._hour + minute // 60) % 24
            self._minute = minute % 60
        return self

    def setTimeWithMinutes(self, minutes):
        if isinstance(minutes, int):
            self._hour = (minutes // 60) % 24
            self._minute = minutes % 60
        return self

    def setTime(self, hour=0, minute=0):
        if isinstance(hour, int) and isinstance(minute, int):
            self._hour = (hour + minute // 60) % 24
            self._minute = minute % 60
        return self

    def set12Time(self, hour=0, minute=0, amOrPm="AM"):
        if isinstance(hour, int) and isinstance(minute, int) and isinstance(amOrPm, str):
            addition = 0
            if amOrPm.upper() == "PM" and hour + minute // 60 < 12:
                addition = 12
            self._hour = (hour + addition + minute // 60) % 24
            self._minute = minute % 60
        return self

    # Mutators
    def addHours(self, hours):
        if isinstance(hours, int):
            self._hour = (self._hour + hours) % 24
        return self

    def addMinutes(self, minutes):
        if isinstance(minutes, int):
            self._hour = (self._hour + (self._minute + minutes) // 60) % 24
            self._minute = (self._minute + minutes) % 60
        return self

    def addTime(self, time):
        if isinstance(time, Time):
            self._hour = (self._hour + time.get24Hour() +
                          ((self._minute + time.getMinute()) // 60)) % 24
            self._minute = (self._minute + time.getMinute()) % 60
        return self
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
    def get12Hour(self):
        if self._hour > 12:
            return [self._hour - 12, "PM"]
        if self._hour == 12:
            return [12, "PM"]
        if self._hour == 0:
            return [12, "AM"]
        return [self._hour, "AM"]

    def getMinutes(self):
        return self._hour * 60 + self._minute

    def get12Time(self):
        return "%02d:%02d %s" % (
            self.get12Hour()[0],
            self._minute,
            self.get12Hour()[1],
        )

    def getStripped12Time(self):
        timeString = self.get12Time()[:5]

        if timeString[0] == "0":
            timeString = timeString[1:]

        return timeString

    def getIsInBetweenInclusive(self, time1, time2):
        if isinstance(time1, Time) and isinstance(time2, Time):
            return time1.getMinutes() <= self.getMinutes() <= time2.getMinutes()
        print("Wrong type, getIsInBetweenInclusive")
        return False

    def getIsInBetweenExclusiveEnd(self, time1, time2):
        if isinstance(time1, Time) and isinstance(time2, Time):
            return time1.getMinutes() <= self.getMinutes() < time2.getMinutes()
        print("Wrong type, getIsInBetweenExclusiveEnd")
        return False

    @staticmethod
    def getTimeBetween(time1, time2):
        if isinstance(time1, Time) and isinstance(time2, Time):
            return abs(time2.getMinutes() - time1.getMinutes())
        return None

    # Setters
    def setTimeWithMinutes(self, minutes):
        if isinstance(minutes, int):
            self._hour = minutes // 60
            self._minute = minutes % 60
        return self

    def set12Time(self, hour=0, minute=0, amOrPm="AM"):
        if (
            isinstance(hour, int)
            and isinstance(minute, int)
            and isinstance(amOrPm, str)
        ):
            addition = 0
            if amOrPm.upper() == "PM" and hour != 12:
                addition = 12
            if amOrPm.upper() == "AM" and hour == 12:
                addition = -12
            self._hour = hour + addition + minute // 60
            self._minute = minute % 60
        return self

    # Comparison
    def equals(self, time):
        return self.getMinutes() == time.getMinutes()

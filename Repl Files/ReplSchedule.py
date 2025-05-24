# Imports classes
from ReplTime import Time


# Creates a class to handle the schedule and displaying it
class Schedule:

    # Construct schedule Object
    def __init__(self,
                 standA=None,
                 standB=None,
                 standC=None,
                 standE=None,
                 standF=None,
                 standG=None,
                 standH=None,
                 standI=None,
                 standJ=None,
                 standK=None,
                 standT=None,
                 standS=None,
                 extraStands=None,
                 downStands=None):
        self.setSchedule(standA,
                         standB,
                         standC,
                         standE,
                         standF,
                         standG,
                         standH,
                         standI,
                         standJ,
                         standK,
                         standT,
                         standS,
                         extraStands,
                         downStands)

    # Getters
    def getReferenceStandA(self):
        return self._standA

    def getStandA(self):
        list = []
        for value in self._standA:
            list1 = []
            for time in value:
                list1.append(time.getTime())
            list.append(list1)
        return list

    def getStandAOpen(self, time):
        open = False
        for list in self._standA:
            if (time.getMinutes() >= list[0].getMinutes() and
                    time.getMinutes() < list[1].getMinutes()):
                open = True
        return open

    def getReferenceStandB(self):
        return self._standB

    def getStandB(self):
        list = []
        for value in self._standB:
            list1 = []
            for time in value:
                list1.append(time.getTime())
            list.append(list1)
        return list

    def getStandBOpen(self, time):
        open = False
        for list in self._standB:
            if (time.getMinutes() >= list[0].getMinutes() and
                    time.getMinutes() < list[1].getMinutes()):
                open = True
        return open

    def getReferenceStandC(self):
        return self._standC

    def getStandC(self):
        list = []
        for value in self._standC:
            list1 = []
            for time in value:
                list1.append(time.getTime())
            list.append(list1)
        return list

    def getStandCOpen(self, time):
        open = False
        for list in self._standC:
            if (time.getMinutes() >= list[0].getMinutes() and
                    time.getMinutes() < list[1].getMinutes()):
                open = True
        return open

    def getReferenceStandE(self):
        return self._standE

    def getStandE(self):
        list = []
        for value in self._standE:
            list1 = []
            for time in value:
                list1.append(time.getTime())
            list.append(list1)
        return list

    def getStandEOpen(self, time):
        open = False
        for list in self._standE:
            if (time.getMinutes() >= list[0].getMinutes() and
                    time.getMinutes() < list[1].getMinutes()):
                open = True
        return open

    def getReferenceStandF(self):
        return self._standF

    def getStandF(self):
        list = []
        for value in self._standF:
            list1 = []
            for time in value:
                list1.append(time.getTime())
            list.append(list1)
        return list

    def getStandFOpen(self, time):
        open = False
        for list in self._standF:
            if (time.getMinutes() >= list[0].getMinutes() and
                    time.getMinutes() < list[1].getMinutes()):
                open = True
        return open

    def getReferenceStandG(self):
        return self._standG

    def getStandG(self):
        list = []
        for value in self._standG:
            list1 = []
            for time in value:
                list1.append(time.getTime())
            list.append(list1)
        return list

    def getStandGOpen(self, time):
        open = False
        for list in self._standG:
            if (time.getMinutes() >= list[0].getMinutes() and
                    time.getMinutes() < list[1].getMinutes()):
                open = True
        return open

    def getReferenceStandH(self):
        return self._standH

    def getStandH(self):
        list = []
        for value in self._standH:
            list1 = []
            for time in value:
                list1.append(time.getTime())
            list.append(list1)
        return list

    def getStandHOpen(self, time):
        open = False
        for list in self._standH:
            if (time.getMinutes() >= list[0].getMinutes() and
                    time.getMinutes() < list[1].getMinutes()):
                open = True
        return open

    def getReferenceStandI(self):
        return self._standI

    def getStandI(self):
        list = []
        for value in self._standI:
            list1 = []
            for time in value:
                list1.append(time.getTime())
            list.append(list1)
        return list

    def getStandIOpen(self, time):
        open = False
        for list in self._standI:
            if (time.getMinutes() >= list[0].getMinutes() and
                    time.getMinutes() < list[1].getMinutes()):
                open = True
        return open

    def getReferenceStandJ(self):
        return self._standJ

    def getStandJ(self):
        list = []
        for value in self._standJ:
            list1 = []
            for time in value:
                list1.append(time.getTime())
            list.append(list1)
        return list

    def getStandJOpen(self, time):
        open = False
        for list in self._standJ:
            if (time.getMinutes() >= list[0].getMinutes() and
                    time.getMinutes() < list[1].getMinutes()):
                open = True
        return open

    def getReferenceStandK(self):
        return self._standK

    def getStandK(self):
        list = []
        for value in self._standK:
            list1 = []
            for time in value:
                list1.append(time.getTime())
            list.append(list1)
        return list

    def getStandKOpen(self, time):
        open = False
        for list in self._standK:
            if (time.getMinutes() >= list[0].getMinutes() and
                    time.getMinutes() < list[1].getMinutes()):
                open = True
        return open

    def getReferenceStandT(self):
        return self._standT

    def getStandT(self):
        list = []
        for value in self._standT:
            list1 = []
            for time in value:
                list1.append(time.getTime())
            list.append(list1)
        return list

    def getStandTOpen(self, time):
        open = False
        for list in self._standT:
            if (time.getMinutes() >= list[0].getMinutes() and
                    time.getMinutes() < list[1].getMinutes()):
                open = True
        return open

    def getReferenceStandS(self):
        return self._standS

    def getStandS(self):
        list = []
        for value in self._standS:
            list1 = []
            for time in value:
                list1.append(time.getTime())
            list.append(list1)
        return list

    def getStandSOpen(self, time):
        open = False
        for list in self._standS:
            if (time.getMinutes() >= list[0].getMinutes() and
                    time.getMinutes() < list[1].getMinutes()):
                open = True
        return open

    def getReferenceExtraStands(self):
        return self._extraStands

    def getExtraStands(self):
        dictionary = {}
        for key in self._extraStands:
            list = []
            for value in self._extraStands[key]:
                list1 = []
                for time in value:
                    list1.append(time.getTime())
                list.append(list1)
            dictionary[key] = list
        return dictionary

    def getExtraStandsOpen(self, time):
        dictionary = {}
        for key in self._extraStands:
            open = False
            for list in self._extraStands[key]:
                if (time.getMinutes() >= list[0].getMinutes() and
                        time.getMinutes() < list[1].getMinutes()):
                    open = True
            dictionary[key] = open
        return dictionary

    def getReferenceDownStands(self):
        return self._downStands

    def getDownStands(self):
        downStandsList = []
        for value in self._downStands:
            if isinstance(value, list):
                downStandsList.append(list(value))
            elif isinstance(value, dict):
                dictionary = {}
                for key in value:
                    list1 = []
                    for item in value[key]:
                        if isinstance(item, int):
                            list1.append(item)
                        elif isinstance(item, list):
                            for i in item:
                                list2 = []
                                list2.append(i.getTime())
                                list1.append(list2)
                    dictionary[key] = list1
                downStandsList.append(dictionary)
        return downStandsList

    def getTotalDownStands(self):
        totalDownStands = []
        for value in self._downStands:
            for item in value:
                totalDownStands.append(item)
        return totalDownStands

    def getOpenStands(self, time):
        dictionary = {}
        if isinstance(time, Time):
            dictionary["A"] = self.getStandAOpen(time)
            dictionary["B"] = self.getStandBOpen(time)
            dictionary["C"] = self.getStandCOpen(time)
            dictionary["E"] = self.getStandEOpen(time)
            dictionary["F"] = self.getStandFOpen(time)
            dictionary["G"] = self.getStandGOpen(time)
            dictionary["H"] = self.getStandHOpen(time)
            dictionary["I"] = self.getStandIOpen(time)
            dictionary["J"] = self.getStandJOpen(time)
            dictionary["K"] = self.getStandKOpen(time)
            dictionary["T"] = self.getStandTOpen(time)
            dictionary["S"] = self.getStandSOpen(time)
            dictionary["Extra Stands"] = self.getExtraStandsOpen(time)
        return dictionary

    def getOnlyOpenStands(self, time):
        list = []
        if isinstance(time, Time):
            dictionary = self.getOpenStands(time)
            for key, value in dictionary.items():
                if isinstance(value, bool) and value:
                    list.append(key)
                elif isinstance(value, dict):
                    for key1 in value:
                        if value[key1]:
                            list.append(key1)
        return list

    def getNumberOpenStands(self, time):
        count = 0
        if isinstance(time, Time):
            dictionary = self.getOpenStands(time)
            for value in dictionary.values():
                if isinstance(value, bool) and value:
                    count = count + 1
                elif isinstance(value, dict):
                    for key in value:
                        if value[key]:
                            count = count + 1
        return count

    def getStandNames(self):
        list = []
        list.append("A")
        list.append("B")
        list.append("C")
        list.append("E")
        list.append("F")
        list.append("G")
        list.append("H")
        list.append("I")
        list.append("J")
        list.append("K")
        list.append("T")
        list.append("S")
        for key in self._extraStands:
            list.append(key)
        return list

    # Setters
    def setStandA(self, standA):
        valid = True
        if isinstance(standA, list):
            for item in standA:
                if isinstance(item, list) and len(item) == 2:
                    for object in item:
                        if not isinstance(object, Time):
                            valid = False
                else:
                    valid = False
        else:
            valid = False
        if valid:
            self._standA = standA
        else:
            self._standA = []
        return self

    def setStandB(self, standB):
        valid = True
        if isinstance(standB, list):
            for item in standB:
                if isinstance(item, list) and len(item) == 2:
                    for object in item:
                        if not isinstance(object, Time):
                            valid = False
                else:
                    valid = False
        else:
            valid = False
        if valid:
            self._standB = standB
        else:
            self._standB = []
        return self

    def setStandC(self, standC):
        valid = True
        if isinstance(standC, list):
            for item in standC:
                if isinstance(item, list) and len(item) == 2:
                    for object in item:
                        if not isinstance(object, Time):
                            valid = False
                else:
                    valid = False
        else:
            valid = False
        if valid:
            self._standC = standC
        else:
            self._standC = []
        return self

    def setStandE(self, standE):
        valid = True
        if isinstance(standE, list):
            for item in standE:
                if isinstance(item, list) and len(item) == 2:
                    for object in item:
                        if not isinstance(object, Time):
                            valid = False
                else:
                    valid = False
        else:
            valid = False
        if valid:
            self._standE = standE
        else:
            self._standE = []
        return self

    def setStandF(self, standF):
        valid = True
        if isinstance(standF, list):
            for item in standF:
                if isinstance(item, list) and len(item) == 2:
                    for object in item:
                        if not isinstance(object, Time):
                            valid = False
                else:
                    valid = False
        else:
            valid = False
        if valid:
            self._standF = standF
        else:
            self._standF = []
        return self

    def setStandG(self, standG):
        valid = True
        if isinstance(standG, list):
            for item in standG:
                if isinstance(item, list) and len(item) == 2:
                    for object in item:
                        if not isinstance(object, Time):
                            valid = False
                else:
                    valid = False
        else:
            valid = False
        if valid:
            self._standG = standG
        else:
            self._standG = []
        return self

    def setStandH(self, standH):
        valid = True
        if isinstance(standH, list):
            for item in standH:
                if isinstance(item, list) and len(item) == 2:
                    for object in item:
                        if not isinstance(object, Time):
                            valid = False
                else:
                    valid = False
        else:
            valid = False
        if valid:
            self._standH = standH
        else:
            self._standH = []
        return self

    def setStandI(self, standI):
        valid = True
        if isinstance(standI, list):
            for item in standI:
                if isinstance(item, list) and len(item) == 2:
                    for object in item:
                        if not isinstance(object, Time):
                            valid = False
                else:
                    valid = False
        else:
            valid = False
        if valid:
            self._standI = standI
        else:
            self._standI = []
        return self

    def setStandJ(self, standJ):
        valid = True
        if isinstance(standJ, list):
            for item in standJ:
                if isinstance(item, list) and len(item) == 2:
                    for object in item:
                        if not isinstance(object, Time):
                            valid = False
                else:
                    valid = False
        else:
            valid = False
        if valid:
            self._standJ = standJ
        else:
            self._standJ = []
        return self

    def setStandK(self, standK):
        valid = True
        if isinstance(standK, list):
            for item in standK:
                if isinstance(item, list) and len(item) == 2:
                    for object in item:
                        if not isinstance(object, Time):
                            valid = False
                else:
                    valid = False
        else:
            valid = False
        if valid:
            self._standK = standK
        else:
            self._standK = []
        return self

    def setStandT(self, standT):
        valid = True
        if isinstance(standT, list):
            for item in standT:
                if isinstance(item, list) and len(item) == 2:
                    for object in item:
                        if not isinstance(object, Time):
                            valid = False
                else:
                    valid = False
        else:
            valid = False
        if valid:
            self._standT = standT
        else:
            self._standT = []
        return self

    def setStandS(self, standS):
        valid = True
        if isinstance(standS, list):
            for item in standS:
                if isinstance(item, list) and len(item) == 2:
                    for object in item:
                        if not isinstance(object, Time):
                            valid = False
                else:
                    valid = False
        else:
            valid = False
        if valid:
            self._standS = standS
        else:
            self._standS = []
        return self

    def setExtraStands(self, extraStands):
        valid = True
        if isinstance(extraStands, dict):
            for key, value in extraStands.items():
                if not isinstance(key, str):
                    valid = False
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, list) and len(item) == 2:
                            for object in item:
                                if not isinstance(object, Time):
                                    valid = False
                        else:
                            valid = False
                else:
                    valid = False
        else:
            valid = False
        if valid:
            self._extraStands = extraStands
        else:
            self._extraStands = {}
        return self

    def setDownStands(self, downStands):
        valid = True
        if isinstance(downStands, list) and len(downStands) == 4:
            for i in range(0, len(downStands)):
                if isinstance(downStands[i], list) and i != 0:
                    for value in downStands[i]:
                        if not isinstance(value, str):
                            valid = False
                elif isinstance(downStands[i], dict) and i == 0:
                    for key, value in downStands[i].items():
                        if not isinstance(key, str):
                            valid = False
                        if isinstance(value, list) and len(value) == 2:
                            if not isinstance(value[0], int):
                                valid = False
                            if isinstance(value[1], list):
                                for item in value[1]:
                                    if not isinstance(item, Time):
                                        valid = False
                            else:
                                valid = False
                        else:
                            valid = False
                else:
                    valid = False
        else:
            valid = False
        if valid:
            self._downStands = downStands
        else:
            self._downStands = [{}, [], [], []]
        return self

    def setSchedule(self,
                    standA=None,
                    standB=None,
                    standC=None,
                    standE=None,
                    standF=None,
                    standG=None,
                    standH=None,
                    standI=None,
                    standJ=None,
                    standK=None,
                    standT=None,
                    standS=None,
                    extraStands=None,
                    downStands=None):
        self.setStandA(standA)
        self.setStandB(standB)
        self.setStandC(standC)
        self.setStandE(standE)
        self.setStandF(standF)
        self.setStandG(standG)
        self.setStandH(standH)
        self.setStandI(standI)
        self.setStandJ(standJ)
        self.setStandK(standK)
        self.setStandT(standT)
        self.setStandS(standS)
        self.setExtraStands(extraStands)
        self.setDownStands(downStands)
        return self
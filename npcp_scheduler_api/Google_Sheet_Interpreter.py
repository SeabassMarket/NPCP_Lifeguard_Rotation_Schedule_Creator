from typing import List
from dataclasses import dataclass

import logging
import traceback

import numpy as np

from CalculateSchedule import CalculaterException
from CalculateSchedule import CalculateSchedule
from Static_API_Info import StaticAPIInfo
from Time import Time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""
============================================================
HELPFUL DATACLASSES
============================================================
"""


@dataclass
class Sheet:
    name: str
    rows: List[List[str]]
    columns: List[List[str]]
    num_rows: int
    num_cols: int


@dataclass
class Spreadsheet:
    name: str
    sheets: List[Sheet]


"""
============================================================
HELPFUL FUNCTIONS
============================================================
"""


def convertDecimal(decimal: float) -> int:
    return round(decimal * 24 * 60)


def generateTimes(sheet: Sheet, start: int) -> list[Time]:
    try:
        firstTime = sheet.columns[0][start]

        if isinstance(firstTime, float):
            firstTime = Time().setTimeWithMinutes(convertDecimal(firstTime))

        elif isinstance(firstTime, str):
            if len(firstTime) < 5:
                firstTime = f"0{firstTime}"
            firstTime = f"{firstTime} AM"
            firstTime = Time().set12Time(
                int(firstTime[:2]), int(firstTime[3:5]), firstTime[6:8]
            )

        else:
            raise TypeError(
                "Column A, row 2 expected to be a valid time format, check template"
            )
    except Exception as e:
        raise Exception(f"Error setting first time in {sheet.name}: {str(e)}")

    times = [firstTime]
    for t in range(1, len(sheet.columns[0])):
        minutes = firstTime.getMinutes() + t * StaticAPIInfo.timeInterval

        thisTime = Time().setTimeWithMinutes(minutes)

        times.append(thisTime)

    return times


def checkDuplicateStands(response):
    categories = [
        "Up Stands",
        "Priority Down Stands",
        "Timely Down Stands",
        "Fill-In Down Stands",
    ]
    seen = set()
    duplicates = set()

    for category in categories:
        data = response.get(category)
        if not data:
            continue

        if category == "Up Stands":
            standNames = data.keys()
        elif category in ("Priority Down Stands", "Fill-In Down Stands"):
            standNames = data.get("stands", [])
        elif category == "Timely Down Stands":
            standNames = data.keys()
        else:
            standNames = []

        for name in standNames:
            if name in seen:
                duplicates.add(name)
            else:
                seen.add(name)

    return list(duplicates)


"""
============================================================
MAIN INTERPRETER CLASS
============================================================
"""


# A class to interpret google sheet information
class SpreadsheetInterpreter:
    def __init__(self, body):
        # Construct sheets for spreadsheet object
        sheets_objs = [
            Sheet(
                name=s["sheet_name"],
                rows=s["values"],
                columns=np.array(s["values"]).T.tolist(),
                num_rows=s["num_rows"],
                num_cols=s["num_cols"],
            )
            for s in body.get("sheets", [])
        ]

        # Set spreadsheet instance variable
        self._spreadsheet = Spreadsheet(
            name=body.get("spreadsheet_name", "Unnamed Spreadsheet"), sheets=sheets_objs
        )

        # Set call instance variable
        call = body.get("call", None)
        if call is None:
            raise TypeError('Variable "call" is none - it was not set in JSON body')
        self._call = call

    @property
    def spreadsheet(self):
        return self._spreadsheet

    def interpret(self):
        if self._call == "preview":
            return self.preview()

        elif self._call == "calculate":
            return self.calculate()

        raise ValueError('Variable "call" not set to a valid value')

    def preview(self):
        response = self.generateData()

        # Iterate through, find time objects, convert them to strings
        for key in response:
            responseData = response[key]

            for responseDataKey in responseData:
                value = responseData[responseDataKey]

                if isinstance(value, dict):
                    times: list[Time] = value.get("times", [])

                    for i in range(len(times)):
                        times[i] = times[i].get12Time()
                elif isinstance(value, Time):
                    responseData[responseDataKey] = value.get12Time()

        # Check for required values
        requiredValues = (
            "Lifeguards",
            "Up Stands",
            "Timely Down Stands",
            "Priority Down Stands",
            "Fill-In Down Stands",
            "Settings",
        )

        for value in requiredValues:
            if value not in response:
                logger.error(f"Missing sheet: {value}")
                raise ValueError(f"Missing sheet: {value}")

        # Check for duplicates
        duplicates = checkDuplicateStands(response)
        if len(duplicates) > 0:
            formatted = ", ".join(f'"{name}"' for name in duplicates)
            raise ValueError(
                f"Duplicate stands found across multiple sheets: {formatted}"
            )

        return response

    def calculate(self):
        response = {}

        calculationInfo = self.preview()

        for key in calculationInfo:
            response[key] = calculationInfo[key]

        data = self.generateData()

        staticAPIInfo = StaticAPIInfo(data)

        try:
            calculator = CalculateSchedule(staticAPIInfo)

            scheduleInfo = calculator.calculateSchedule()

            for key in scheduleInfo:
                response[key] = scheduleInfo[key]

            return response
        except Exception as e:
            logger.error(traceback.format_exc())
            raise CalculaterException(f"Error calculating: {str(e)}")

    def generateData(self):
        response = {}

        # Set up stand data before everything else
        for sheet in self._spreadsheet.sheets:
            responseData: dict[str, dict | list] = {}

            if sheet.name == "Up Stands":
                responseData: dict[str, dict | list] = {}

                if len(sheet.rows) < 2:
                    raise IndexError(f"{sheet.name} sheet has too little rows")

                # Create the times list
                times = generateTimes(sheet, 1)

                # Parse data
                for c in range(1, len(sheet.columns)):
                    column = sheet.columns[c]

                    standName = column[0]

                    if len(standName) > 0 and standName != "EMPTY":
                        possibleTimes = column[1:]

                        timesUp = []
                        for t in range(len(possibleTimes)):
                            slot = possibleTimes[t]

                            if len(slot) > 0:
                                timesUp.append(times[t])

                        if len(timesUp) > 0:
                            responseData[standName] = {"times": timesUp}

            elif sheet.name == "Lifeguards":
                if len(sheet.rows) < 2:
                    raise IndexError(f"{sheet.name} sheet has too little rows")

                # Create the times list
                times = generateTimes(sheet, 1)

                # Parse data
                for c in range(1, len(sheet.columns)):
                    column = sheet.columns[c]

                    def convertLifeguardName(name: str) -> str:
                        for i in range(len(name)):
                            character = name[i]

                            if character.isalpha():
                                return name[i:]

                        return f"Lifeguard {c}"

                    lifeguardName = column[0]

                    if len(lifeguardName) > 0 and lifeguardName != "EMPTY":
                        lifeguardName = convertLifeguardName(lifeguardName)

                        possibleTimes = column[1:]

                        firstSlot = None
                        lastSlot = None
                        for t in range(len(possibleTimes)):
                            if len(possibleTimes[t]) > 0:
                                if firstSlot is None:
                                    firstSlot = t
                                lastSlot = t

                        if firstSlot is None:
                            raise TypeError(
                                f"Error setting lifeguard {lifeguardName}: no start time"
                            )

                        firstTime = times[firstSlot]

                        lastTime = Time().setTimeWithMinutes(
                            times[lastSlot].getMinutes() + StaticAPIInfo.timeInterval
                        )

                        timeRange = [firstTime, lastTime]

                        responseData[lifeguardName] = {"times": timeRange}

            response[sheet.name] = responseData

        # Set other data
        for sheet in self._spreadsheet.sheets:
            responseData: dict[str, dict | object] = {}

            if sheet.name == "Timely Down Stands":
                if len(sheet.rows) < 2:
                    raise IndexError(f"{sheet.name} sheet has too little rows")

                if sheet.rows[1][0] != "Num":
                    raise ValueError(
                        f"{sheet.name} formatting is incorrect. Row two should be Num, check template"
                    )

                # ============================================================
                # AUTOMATIC SU AND CU
                # ============================================================

                # Check data

                upStandsData = response.get("Up Stands")

                if upStandsData is None:
                    raise ValueError(
                        f'{sheet.name} cannot calculate CU and SU: sheet "Up Stands" does not exist'
                    )

                if len(upStandsData) < 1:
                    raise IndexError(
                        f'{sheet.name} cannot calculate CU and SU: sheet "Up Stands" does not have data'
                    )

                lifeguardData = response.get("Lifeguards")

                if lifeguardData is None:
                    raise ValueError(
                        f'{sheet.name} cannot calculate CU and SU: sheet "Lifeguards" does not exist'
                    )

                if len(lifeguardData) < 1:
                    raise IndexError(
                        f'{sheet.name} cannot calculate CU and SU: sheet "Lifeguards" does not have data'
                    )

                # Calculate earliest and latest times of up stands

                earliestStandTime = None
                latestStandTime = None
                for stand in upStandsData:
                    data = upStandsData[stand]

                    standTimes = data["times"]

                    for thisTime in standTimes:
                        if earliestStandTime is None or (
                            isinstance(earliestStandTime, Time)
                            and thisTime.getMinutes() < earliestStandTime.getMinutes()
                        ):
                            earliestStandTime = thisTime

                        if latestStandTime is None or (
                            isinstance(latestStandTime, Time)
                            and thisTime.getMinutes() > latestStandTime.getMinutes()
                        ):
                            latestStandTime = thisTime

                # Create lifeguard objects

                earliestLifeguardTime = None
                latestLifeguardTime = None

                for i in range(len(lifeguardData)):
                    name = list(lifeguardData.keys())[i]

                    shiftTimes = lifeguardData[name]["times"]

                    if earliestLifeguardTime is None or (
                        isinstance(earliestLifeguardTime, Time)
                        and shiftTimes[0].getMinutes()
                        < earliestLifeguardTime.getMinutes()
                    ):
                        earliestLifeguardTime = shiftTimes[0]

                    if latestStandTime is None or (
                        isinstance(latestStandTime, Time)
                        and shiftTimes[1].getMinutes() > latestStandTime.getMinutes()
                    ):
                        latestLifeguardTime = shiftTimes[1]

                # Find times and amount for SU and CU

                suTimes = []

                for t in range(
                    earliestLifeguardTime.getMinutes(),
                    earliestStandTime.getMinutes(),
                    StaticAPIInfo.timeInterval,
                ):
                    suTimes.append(Time().setTimeWithMinutes(t))

                responseData["SU"] = {"num": len(lifeguardData), "times": suTimes}

                cuTimes = []
                for t in range(
                    latestStandTime.getMinutes() + StaticAPIInfo.timeInterval,
                    latestLifeguardTime.getMinutes(),
                    StaticAPIInfo.timeInterval,
                ):
                    cuTimes.append(Time().setTimeWithMinutes(t))

                responseData["CU"] = {"num": len(lifeguardData), "times": cuTimes}

                # ============================================================
                # All other Timely Down Stands
                # ============================================================

                # Create the times list
                times = generateTimes(sheet, 2)

                # Set nums
                nums = sheet.rows[1]

                # Parse data
                for c in range(1, len(sheet.columns)):
                    column = sheet.columns[c]

                    standName = column[0]

                    if len(standName) > 0 and standName != "EMPTY":
                        possibleTimes = column[2:]

                        timesUp = []
                        for t in range(len(possibleTimes)):
                            slot = possibleTimes[t]

                            if len(slot) > 0:
                                timesUp.append(times[t])

                        num = nums[c]

                        responseData[standName] = {"num": num, "times": timesUp}

            elif (
                sheet.name == "Priority Down Stands"
                or sheet.name == "Fill-In Down Stands"
            ):
                if len(sheet.columns) < 1:
                    raise IndexError(f"{sheet.name} sheet has too little columns")

                column = sheet.columns[0]

                stands = []
                for r in range(1, len(column)):
                    stand = column[r]

                    stands.append(stand)

                responseData["stands"] = stands

            elif sheet.name == "Settings":
                if len(sheet.columns) < 2:
                    raise IndexError(f"{sheet.name} sheet has too little columns")

                infoColumn = sheet.columns[1]

                num = 1
                if len(sheet.columns) < num:
                    raise IndexError(
                        f"{sheet.name} sheet has too little values in columns: expected {num}"
                    )

                branchTime = infoColumn[1]

                try:
                    responseData["branch time"] = Time().set12Time(
                        int(branchTime[:2]), int(branchTime[3:5]), branchTime[6:8]
                    )
                except Exception as e:
                    raise Exception(f"Error setting branch time: f{str(e)}")

            if sheet.name != "Up Stands" and sheet.name != "Lifeguards":
                response[sheet.name] = responseData

        return response

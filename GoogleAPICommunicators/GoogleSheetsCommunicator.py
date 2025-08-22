# Import libraries
import os

import gspread
import pandas as pd

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from gspread.exceptions import APIError

from InfoManagers.CalculateSchedule import CalculateSchedule
from InfoManagers.Lifeguard import Lifeguard
from InfoManagers.StaticAppInfo import StaticAppInfo
from InfoManagers.Time import Time


# Helper functions
def rgbToSheets(r, g, b):
    return {"red": r / 255, "green": g / 255, "blue": b / 255}


def colNumToLetter(colNum):
    result = ""
    while colNum > 0:
        colNum -= 1
        result = chr(65 + colNum % 26) + result
        colNum //= 26
    return result


# Helper classes for errors
class GSException(Exception):
    pass


class WorksheetException(Exception):
    pass


# A class to communicate with Google Sheets via their cloud console API
class GSCommunicator:
    def __init__(
        self,
        staticAppInfo: StaticAppInfo,
        calculator: CalculateSchedule,
        rowStart: int = 1,
        columnStart: int = 1,
    ):
        self._staticAppInfo = staticAppInfo
        self._calculator = calculator

        self._rowStart = rowStart
        self._columnStart = columnStart

        self._dataFrame, self._lifeguards, self._scheduleData = self.createDataFrame()

        # Instances variables set by setWorksheet
        self._credentialsFile = None
        self._spreadsheet = None
        self._worksheet = None
        self._sheetsService = None

    def getItem(self, item: str) -> object | None:
        if item == "creds":
            return self._credentialsFile
        elif item == "spreadsheet":
            return self._spreadsheet
        elif item == "worksheet":
            return self._worksheet
        elif item == "service":
            return self._sheetsService

        return None

    def createDataFrame(
        self,
    ) -> tuple[pd.DataFrame, list[Lifeguard], dict[Time, list[str]]]:
        # Create schedule dictionary

        earliestTime, latestTime = self._calculator.calculatePoolOpenTimeRange()

        lifeguards: list[Lifeguard] = self._calculator.getLifeguards()

        scheduleData: dict[Time, list[str]] = {}

        for t in range(
            earliestTime.getMinutes(),
            latestTime.getMinutes(),
            self._staticAppInfo.getTimeInterval(),
        ):
            currentTime = Time().setTimeWithMinutes(t)

            stands = []

            for lifeguard in lifeguards:
                stand = lifeguard.getStand(currentTime)

                if stand == self._staticAppInfo.getEmptyCode():
                    stands.append("")
                else:
                    stands.append(stand)

            scheduleData[currentTime.getStripped12Time()] = stands

        # Create DataFrame
        df = pd.DataFrame.from_dict(scheduleData, orient="index")
        df.index.name = ""

        # Show full DataFrame
        pd.set_option("display.max_columns", None)
        pd.set_option("display.max_rows", None)
        pd.set_option("display.width", None)
        pd.set_option("display.max_colwidth", 10)

        # Replace None with empty strings for cleaner look
        df = df.fillna("")

        # set headers to lifeguards
        df.columns = self._calculator.getLifeguardNames()

        return df, lifeguards, scheduleData

    def setWorksheet(self, spreadsheetName: str, credentialsEnvVar: str):
        try:
            # Get credentials
            self._credentialsFile = os.getenv(credentialsEnvVar)
            gc = gspread.service_account(filename=self._credentialsFile)

            # Open spreadsheet
            self._spreadsheet = gc.open(spreadsheetName)
            self._worksheet = self._spreadsheet.sheet1

            # Set sheetsService
            creds = Credentials.from_service_account_file(
                self._credentialsFile,
                scopes=["https://www.googleapis.com/auth/spreadsheets"],
            )
            self._sheetsService = build("sheets", "v4", credentials=creds)
        except Exception:
            raise WorksheetException("Error setting worksheet")

    def writeScheduleToWorksheet(self):
        if (
            self._credentialsFile is None
            or self._worksheet is None
            or self._spreadsheet is None
            or self._sheetsService is None
        ):
            raise WorksheetException("Worksheet not set")

        try:
            # Clear sheet
            self.clearSheet()

            # Export DataFrame
            self.exportDataFrame()

            # Format sheet
            self.formatSheet()

            # Write colors
            requests = self.getColorRequests()

            # Write request to API
            self._sheetsService.spreadsheets().batchUpdate(
                spreadsheetId=self._spreadsheet.id, body={"requests": requests}
            ).execute()
        except APIError:
            raise GSException(
                "Error while writing to sheet;\n"
                "API quota might have been reached, or writing may have exceeded grid limits"
            )
        except Exception:
            raise Exception()

    def clearSheet(self):
        # Clear formatting
        self._worksheet.clear()

        request = {
            "requests": [
                {"repeatCell": {"range": {"sheetId": 0}, "fields": "userEnteredFormat"}}
            ]
        }
        self._sheetsService.spreadsheets().batchUpdate(
            spreadsheetId=self._spreadsheet.id, body=request
        ).execute()

        self._sheetsService.spreadsheets().batchUpdate(
            spreadsheetId=self._spreadsheet.id,
            body={
                "requests": [
                    {
                        "updateDimensionProperties": {
                            "range": {
                                "sheetId": 0,
                                "dimension": "COLUMNS",
                                "startIndex": 0,
                            },
                            "properties": {"pixelSize": 63},
                            "fields": "pixelSize",
                        }
                    }
                ]
            },
        ).execute()

        self._sheetsService.spreadsheets().batchUpdate(
            spreadsheetId=self._spreadsheet.id,
            body={
                "requests": [
                    {
                        "updateDimensionProperties": {
                            "range": {
                                "sheetId": 0,
                                "dimension": "ROWS",
                                "startIndex": 0,
                            },
                            "properties": {"pixelSize": 20},
                            "fields": "pixelSize",
                        }
                    }
                ]
            },
        ).execute()

    def formatSheet(self):
        # For convenience
        columnStartLetter = colNumToLetter(self._columnStart)

        # Format time columns
        self._sheetsService.spreadsheets().batchUpdate(
            spreadsheetId=self._spreadsheet.id,
            body={
                "requests": [
                    {
                        "updateDimensionProperties": {
                            "range": {
                                "sheetId": 0,
                                "dimension": "COLUMNS",
                                "startIndex": 0,
                                "endIndex": len(self._lifeguards)
                                + self._columnStart
                                + 1,
                            },
                            "properties": {"pixelSize": 35},
                            "fields": "pixelSize",
                        }
                    }
                ]
            },
        ).execute()

        self._worksheet.format(
            f"{columnStartLetter}{self._rowStart + 1}:{columnStartLetter}{len(self._scheduleData) + self._rowStart}",
            {
                "borders": {
                    "right": {"style": "SOLID", "width": 2},
                },
                "horizontalAlignment": "RIGHT",
                "verticalAlignment": "MIDDLE",
            },
        )

        lastColumn = colNumToLetter(len(self._lifeguards) + self._columnStart + 1)
        self._worksheet.format(
            f"{lastColumn}{self._rowStart + 1}:{lastColumn}{len(self._scheduleData) + self._rowStart}",
            {
                "borders": {
                    "left": {"style": "SOLID", "width": 2},
                },
                "horizontalAlignment": "LEFT",
                "verticalAlignment": "MIDDLE",
            },
        )

        # Format stand columns
        self._sheetsService.spreadsheets().batchUpdate(
            spreadsheetId=self._spreadsheet.id,
            body={
                "requests": [
                    {
                        "updateDimensionProperties": {
                            "range": {
                                "sheetId": 0,
                                "dimension": "COLUMNS",
                                "startIndex": self._columnStart,
                                "endIndex": len(self._lifeguards) + self._columnStart,
                            },
                            "properties": {"pixelSize": 25},
                            "fields": "pixelSize",
                        }
                    }
                ]
            },
        ).execute()

        # Format row columns
        self._sheetsService.spreadsheets().batchUpdate(
            spreadsheetId=self._spreadsheet.id,
            body={
                "requests": [
                    {
                        "updateDimensionProperties": {
                            "range": {
                                "sheetId": 0,
                                "dimension": "ROWS",
                                "startIndex": self._rowStart - 1,
                                "endIndex": self._rowStart,
                            },
                            "properties": {"pixelSize": 80},
                            "fields": "pixelSize",
                        }
                    }
                ]
            },
        ).execute()

        self._sheetsService.spreadsheets().batchUpdate(
            spreadsheetId=self._spreadsheet.id,
            body={
                "requests": [
                    {
                        "updateDimensionProperties": {
                            "range": {
                                "sheetId": 0,
                                "dimension": "ROWS",
                                "startIndex": self._rowStart,
                            },
                            "properties": {"pixelSize": 20},
                            "fields": "pixelSize",
                        }
                    }
                ]
            },
        ).execute()

        # Add text tilt and borders
        self._worksheet.format(
            f"{colNumToLetter(self._columnStart + 1)}{self._rowStart}:{colNumToLetter(len(self._lifeguards) + self._columnStart + 1)}{self._rowStart}",
            {
                "borders": {
                    "bottom": {"style": "SOLID", "width": 2},
                    "right": {"style": "SOLID", "width": 1},
                },
                "textRotation": {"angle": 45},
                "horizontalAlignment": "LEFT",
                "verticalAlignment": "BOTTOM",
            },
        )

        self._worksheet.format(
            f"{colNumToLetter(self._columnStart)}{self._rowStart}:{colNumToLetter(self._columnStart)}{self._rowStart}",
            {
                "borders": {
                    "bottom": {"style": "SOLID", "width": 2},
                },
                "textRotation": {"angle": 45},
                "horizontalAlignment": "LEFT",
                "verticalAlignment": "BOTTOM",
            },
        )

        # Add borders for stands
        self._worksheet.format(
            f"{colNumToLetter(self._columnStart + 1)}{self._rowStart + 1}:{colNumToLetter(len(self._lifeguards) + self._columnStart)}{len(self._scheduleData) + self._rowStart}",
            {
                "borders": {
                    "top": {"style": "SOLID", "width": 1},
                    "bottom": {"style": "SOLID", "width": 1},
                    "right": {"style": "SOLID", "width": 1},
                    "left": {"style": "SOLID", "width": 1},
                },
                "horizontalAlignment": "CENTER",
                "verticalAlignment": "MIDDLE",
            },
        )

        # Add borders for bottom bar
        self._worksheet.format(
            f"{columnStartLetter}{len(self._scheduleData) + self._rowStart + 1}:{colNumToLetter(len(self._lifeguards) + self._columnStart + 1)}{len(self._scheduleData) + self._rowStart + 1}",
            {
                "borders": {
                    "top": {"style": "SOLID", "width": 2},
                    "bottom": {"style": "SOLID", "width": 2},
                    "right": {"style": "SOLID", "width": 2},
                    "left": {"style": "SOLID", "width": 2},
                },
                "horizontalAlignment": "CENTER",
                "verticalAlignment": "MIDDLE",
            },
        )

        # Copy and paste times
        data = self._worksheet.get_values(
            f"{columnStartLetter}{self._rowStart + 1}:{columnStartLetter}{len(self._scheduleData) + self._rowStart}"
        )
        self._worksheet.update(
            range_name=f"{colNumToLetter(self._columnStart + 1 + len(self._lifeguards))}{self._rowStart + 1}",
            values=data,
        )

        # Apply font and sizing
        lastColumn = colNumToLetter(len(self._lifeguards) + self._columnStart + 1)
        self._worksheet.format(
            f"{columnStartLetter}:{lastColumn}",
            {"textFormat": {"fontFamily": "Times New Roman", "fontSize": 10}},
        )

    def exportDataFrame(self):
        # Export DataFrame
        df_export = self._dataFrame.reset_index()
        values = [df_export.columns.tolist()] + df_export.values.tolist()
        self._worksheet.update(
            range_name=f"{colNumToLetter(self._columnStart)}{self._rowStart}",
            values=values,
        )

    def getColorRequests(self):
        # Create requests list

        requests = []

        # Add blue columns

        start = 1

        index = start

        ranges: list[dict[str, int]] = []
        while index < start + len(self._lifeguards):
            thisRange = {
                "sheetId": 0,
                "startRowIndex": self._rowStart - 1,
                "startColumnIndex": index + self._columnStart - 1,
                "endColumnIndex": index + self._columnStart,
            }

            index += 2

            ranges.append(thisRange)

        for thisRange in ranges:
            requests.append(
                {
                    "repeatCell": {
                        "range": thisRange,
                        "cell": {
                            "userEnteredFormat": {
                                "backgroundColor": rgbToSheets(0, 204, 255)
                            }
                        },
                        "fields": "userEnteredFormat.backgroundColor",
                    }
                }
            )

        # Add gray boxes

        ranges: list[dict[str, int]] = []
        for i in range(len(self._lifeguards)):

            def findEndOfShift():
                shiftStarted = False

                stands = list(self._scheduleData.values())

                standIndex = 0
                while standIndex < len(stands):
                    stand = stands[standIndex][i]

                    if stand is not None:
                        shiftStarted = True
                    else:
                        if shiftStarted:
                            return standIndex

                    standIndex += 1

                return None

            endOfShift = findEndOfShift()
            if endOfShift is not None:
                thisRange = {
                    "sheetId": 0,
                    "startRowIndex": endOfShift + self._rowStart,
                    "endRowIndex": self._rowStart + len(self._scheduleData),
                    "startColumnIndex": i + self._columnStart,
                    "endColumnIndex": i + self._columnStart + 1,
                }

                ranges.append(thisRange)

        for thisRange in ranges:
            requests.append(
                {
                    "repeatCell": {
                        "range": thisRange,
                        "cell": {
                            "userEnteredFormat": {
                                "backgroundColor": rgbToSheets(153, 153, 153)
                            }
                        },
                        "fields": "userEnteredFormat.backgroundColor",
                    }
                }
            )

        # Add green, yellow, orange, and red boxes
        stands2DArray = list(self._scheduleData.values())

        for i in range(len(self._lifeguards)):
            standIndex = 0
            while standIndex < len(stands2DArray):
                currentStands = stands2DArray[standIndex]

                if standIndex > 0:
                    previousStands = stands2DArray[standIndex - 1]
                else:
                    previousStands = []

                if standIndex + 1 < len(stands2DArray):
                    nextStands = stands2DArray[standIndex + 1]
                else:
                    nextStands = []

                stand = currentStands[i]

                if stand == self._staticAppInfo.getBreakCode():
                    thisRange = {
                        "sheetId": 0,
                        "startRowIndex": standIndex + self._rowStart,
                        "endRowIndex": standIndex + self._rowStart + 2,
                        "startColumnIndex": i + self._columnStart,
                        "endColumnIndex": i + self._columnStart + 1,
                    }

                    requests.append(
                        {
                            "repeatCell": {
                                "range": thisRange,
                                "cell": {
                                    "userEnteredFormat": {
                                        "backgroundColor": rgbToSheets(255, 255, 0)
                                    }
                                },
                                "fields": "userEnteredFormat.backgroundColor",
                            }
                        }
                    )

                    requests.append(
                        {
                            "updateCells": {
                                "range": thisRange,
                                "fields": "userEnteredValue",
                            }
                        }
                    )

                    standIndex += self._staticAppInfo.getBreakInterval() - 1
                elif stand in self._calculator.getUpStandNames():
                    if (
                        stand in currentStands
                        and stand not in previousStands
                        and stand not in nextStands
                    ):
                        thisRange = {
                            "sheetId": 0,
                            "startRowIndex": standIndex + self._rowStart,
                            "endRowIndex": standIndex + self._rowStart + 1,
                            "startColumnIndex": i + self._columnStart,
                            "endColumnIndex": i + self._columnStart + 1,
                        }

                        requests.append(
                            {
                                "repeatCell": {
                                    "range": thisRange,
                                    "cell": {
                                        "userEnteredFormat": {
                                            "backgroundColor": rgbToSheets(255, 127, 0)
                                        }
                                    },
                                    "fields": "userEnteredFormat.backgroundColor",
                                }
                            }
                        )
                    elif stand in currentStands and stand not in previousStands:
                        thisRange = {
                            "sheetId": 0,
                            "startRowIndex": standIndex + self._rowStart,
                            "endRowIndex": standIndex + self._rowStart + 1,
                            "startColumnIndex": i + self._columnStart,
                            "endColumnIndex": i + self._columnStart + 1,
                        }

                        requests.append(
                            {
                                "repeatCell": {
                                    "range": thisRange,
                                    "cell": {
                                        "userEnteredFormat": {
                                            "backgroundColor": rgbToSheets(0, 255, 0)
                                        }
                                    },
                                    "fields": "userEnteredFormat.backgroundColor",
                                }
                            }
                        )
                    elif stand in currentStands and stand not in nextStands:
                        thisRange = {
                            "sheetId": 0,
                            "startRowIndex": standIndex + self._rowStart,
                            "endRowIndex": standIndex + self._rowStart + 1,
                            "startColumnIndex": i + self._columnStart,
                            "endColumnIndex": i + self._columnStart + 1,
                        }

                        requests.append(
                            {
                                "repeatCell": {
                                    "range": thisRange,
                                    "cell": {
                                        "userEnteredFormat": {
                                            "backgroundColor": rgbToSheets(255, 0, 0)
                                        }
                                    },
                                    "fields": "userEnteredFormat.backgroundColor",
                                }
                            }
                        )

                standIndex += 1

        return requests

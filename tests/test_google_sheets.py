# import libraries
import tkinter as tk
import os

import gspread
import pandas as pd

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

from InfoManagers.CalculateSchedule import CalculateSchedule
from InfoManagers.Lifeguard import Lifeguard
from InfoManagers.StaticAppInfo import StaticAppInfo
from InfoManagers.Time import Time

"""THE FIRST PART OF THIS CODE IS JUST HARDCODING INFORMATION"""

# Create static app info
staticAppInfo = StaticAppInfo(tk.Tk())

# Create all the information for the stands
upStands = {
    "E": [Time(hour=11, minute=0), Time(hour=20, minute=0), 1],
    "H": [Time(hour=11, minute=0), Time(hour=20, minute=0), 1],
    "K": [Time(hour=11, minute=0), Time(hour=20, minute=0), 1],
    "A": [Time(hour=12, minute=0), Time(hour=19, minute=0), 1],
    "B": [Time(hour=12, minute=0), Time(hour=19, minute=0), 1],
    "I": [Time(hour=13, minute=0), Time(hour=16, minute=0), 1],
    "T": [Time(hour=13, minute=0), Time(hour=19, minute=0), 1],
    "S": [Time(hour=13, minute=0), Time(hour=19, minute=0), 1],
}
timelyDownStands = {
    "SU": [Time(hour=10, minute=40), Time(hour=11, minute=0), 3],
    "DT": [Time(hour=14, minute=0), Time(hour=14, minute=20), 2],
    "ST": [Time(hour=15, minute=0), Time(hour=15, minute=20), 2],
    "CU": [Time(hour=20, minute=0), Time(hour=21, minute=0), 5],
}
priorityDownStands = {
    "O": [Time(hour=0, minute=0), "end of day", 1],
    "X": [Time(hour=0, minute=0), "end of day", 1],
    "P": [Time(hour=0, minute=0), "end of day", 1],
}
fillInDownStands = {
    "W": [Time(hour=0, minute=0), "end of day"],
}
standData = {
    "up": upStands,
    "timely down": timelyDownStands,
    "priority down": priorityDownStands,
    "fill-in down": fillInDownStands,
}

staticAppInfo.setEventDataSpecific(standData, eventDescriptor="stand")

# Create information for the stands
lifeguardsDict = {
    "1": [Time(hour=10, minute=40), Time(hour=18, minute=40)],
    "2": [Time(hour=10, minute=40), Time(hour=18, minute=40)],
    "3": [Time(hour=10, minute=40), Time(hour=18, minute=40)],
    "4": [Time(hour=11, minute=0), Time(hour=19, minute=0)],
    "5": [Time(hour=11, minute=0), Time(hour=14, minute=0)],
    "6": [Time(hour=11, minute=0), Time(hour=19, minute=0)],
    "7": [Time(hour=12, minute=0), Time(hour=20, minute=0)],
    "8": [Time(hour=11, minute=40), Time(hour=19, minute=40)],
    "9": [Time(hour=13, minute=0), Time(hour=21, minute=0)],
    "10": [Time(hour=13, minute=0), Time(hour=21, minute=0)],
    "11": [Time(hour=13, minute=0), Time(hour=21, minute=0)],
    "12": [Time(hour=13, minute=0), Time(hour=21, minute=0)],
    "13": [Time(hour=13, minute=0), Time(hour=21, minute=0)],
}

lifeguardData = {
    "lifeguard": lifeguardsDict,
}

staticAppInfo.setEventDataSpecific(lifeguardData, eventDescriptor="lifeguard")

"""END OF HARDCODING, BEGINNING OF DEVELOPING ALGORITHM"""

# Calculate Schedule

calculator = CalculateSchedule(staticAppInfo)
calculator.assignBreaks()
calculator.calculateSchedule()

# Create schedule dictionary

earliestTime, latestTime = calculator.calculatePoolOpenTimeRange()

lifeguards: list[Lifeguard] = calculator.getLifeguards()

scheduleData: dict[Time, list[str]] = {}

for t in range(
    earliestTime.getMinutes(), latestTime.getMinutes(), staticAppInfo.getTimeInterval()
):
    currentTime = Time().setTimeWithMinutes(t)

    stands = []

    for lifeguard in lifeguards:
        stand = lifeguard.getStand(currentTime)

        stands.append(stand)

    scheduleData[currentTime.getStripped12Time()] = stands

"""CREATION OF DATA FRAME"""

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
df.columns = calculator.getLifeguardNames()

print(df)

"""OPEN SPREADSHEET"""

# Constants
ROW_START = 1

# Get credentials
credentialsFile = os.getenv("NPCP_GOOGLE_SHEETS_KEY")
gc = gspread.service_account(filename=credentialsFile)

# Open spreadsheet
spreadsheet = gc.open("Lifeguard Schedule")
worksheet = spreadsheet.sheet1

# Clear formatting

creds = Credentials.from_service_account_file(
    credentialsFile, scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
sheets_service = build("sheets", "v4", credentials=creds)

request = {
    "requests": [
        {"repeatCell": {"range": {"sheetId": 0}, "fields": "userEnteredFormat"}}
    ]
}
sheets_service.spreadsheets().batchUpdate(
    spreadsheetId=spreadsheet.id, body=request
).execute()

# Export DataFrame
df_export = df.reset_index()
values = [df_export.columns.tolist()] + df_export.values.tolist()
worksheet.clear()
worksheet.update(range_name=f"A{ROW_START}", values=values)

"""FORMAT INFO"""


# Convert RGB (0-255) to Google Sheets format (0-1)
def rgbToSheets(r, g, b):
    return {"red": r / 255, "green": g / 255, "blue": b / 255}


def colNumToLetter(colNum):
    result = ""
    while colNum > 0:
        colNum -= 1
        result = chr(65 + colNum % 26) + result
        colNum //= 26
    return result


# Format time columns
timeColumnWidth = 33

sheets_service.spreadsheets().batchUpdate(
    spreadsheetId=spreadsheet.id,
    body={
        "requests": [
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": 0,
                        "dimension": "COLUMNS",
                        "startIndex": 0,
                        "endIndex": len(lifeguards) + 2,
                    },
                    "properties": {"pixelSize": timeColumnWidth},
                    "fields": "pixelSize",
                }
            }
        ]
    },
).execute()

worksheet.format(
    f"A",
    {"horizontalAlignment": "RIGHT", "verticalAlignment": "MIDDLE"},
)

worksheet.format(
    f"{colNumToLetter(len(lifeguards) + 2)}",
    {"horizontalAlignment": "LEFT", "verticalAlignment": "MIDDLE"},
)

# Format stand columns
standColumnWidth = 10

sheets_service.spreadsheets().batchUpdate(
    spreadsheetId=spreadsheet.id,
    body={
        "requests": [
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": 0,
                        "dimension": "COLUMNS",
                        "startIndex": 1,
                        "endIndex": len(lifeguards) + 1,
                    },
                    "properties": {"pixelSize": 25},
                    "fields": "pixelSize",
                }
            }
        ]
    },
).execute()

# Format row columns
sheets_service.spreadsheets().batchUpdate(
    spreadsheetId=spreadsheet.id,
    body={
        "requests": [
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": 0,
                        "dimension": "ROWS",
                        "startIndex": ROW_START - 1,
                        "endIndex": ROW_START,
                    },
                    "properties": {"pixelSize": 80},
                    "fields": "pixelSize",
                }
            }
        ]
    },
).execute()

sheets_service.spreadsheets().batchUpdate(
    spreadsheetId=spreadsheet.id,
    body={
        "requests": [
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": 0,
                        "dimension": "ROWS",
                        "startIndex": ROW_START,
                    },
                    "properties": {"pixelSize": 20},
                    "fields": "pixelSize",
                }
            }
        ]
    },
).execute()

# Add text tilt and borders

worksheet.format(
    f"A{ROW_START}:{colNumToLetter(len(lifeguards) + 2)}{ROW_START}",
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

# Add borders for stands
worksheet.format(
    f"B{ROW_START + 1}:{colNumToLetter(len(lifeguards) + 1)}{len(scheduleData) + ROW_START}",
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


# Copy and paste times
data = worksheet.get_values(f"A{ROW_START + 1}:A{len(scheduleData) + ROW_START}")
worksheet.update(
    range_name=f"{colNumToLetter(2 + len(lifeguards))}{ROW_START + 1}", values=data
)

# Apply font and sizing
lastColumn = colNumToLetter(len(lifeguards) + 2)
worksheet.format(
    f"A:{lastColumn}",
    {"textFormat": {"fontFamily": "Times New Roman", "fontSize": 10}},
)

# Create requests list

requests = []

# Add blue columns

start = 1

index = start

ranges: list[dict[str, int]] = []
while index < start + len(lifeguards):
    thisRange = {
        "sheetId": 0,
        "startRowIndex": ROW_START - 1,
        "startColumnIndex": index,
        "endColumnIndex": index + 1,
    }

    index += 2

    ranges.append(thisRange)

for thisRange in ranges:
    requests.append(
        {
            "repeatCell": {
                "range": thisRange,
                "cell": {
                    "userEnteredFormat": {"backgroundColor": rgbToSheets(0, 204, 255)}
                },
                "fields": "userEnteredFormat.backgroundColor",
            }
        }
    )

# Add gray boxes

ranges: list[dict[str, int]] = []
for i in range(len(lifeguards)):

    def findEndOfShift():
        shiftStarted = False

        stands = list(scheduleData.values())

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

    lifeguard = lifeguards[i]

    endOfShift = findEndOfShift()
    if endOfShift is not None:
        thisRange = {
            "sheetId": 0,
            "startRowIndex": endOfShift + ROW_START,
            "endRowIndex": ROW_START + len(scheduleData),
            "startColumnIndex": i + 1,
            "endColumnIndex": i + 2,
        }

        ranges.append(thisRange)

for thisRange in ranges:
    requests.append(
        {
            "repeatCell": {
                "range": thisRange,
                "cell": {
                    "userEnteredFormat": {"backgroundColor": rgbToSheets(153, 153, 153)}
                },
                "fields": "userEnteredFormat.backgroundColor",
            }
        }
    )

# Add green, yellow, orange, and red boxes
start = 2

stands2DArray = list(scheduleData.values())

for i in range(len(lifeguards)):
    colLetter = colNumToLetter(start + i)

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

        if stand == staticAppInfo.getBreakCode():
            thisRange = {
                "sheetId": 0,
                "startRowIndex": standIndex + ROW_START,
                "endRowIndex": standIndex + ROW_START + 2,
                "startColumnIndex": i + 1,
                "endColumnIndex": i + 2,
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
                {"updateCells": {"range": thisRange, "fields": "userEnteredValue"}}
            )

            standIndex += staticAppInfo.getBreakInterval() - 1
        elif stand in calculator.getUpStandNames():
            if (
                stand in currentStands
                and stand not in previousStands
                and stand not in nextStands
            ):
                thisRange = {
                    "sheetId": 0,
                    "startRowIndex": standIndex + ROW_START,
                    "endRowIndex": standIndex + ROW_START + 1,
                    "startColumnIndex": i + 1,
                    "endColumnIndex": i + 2,
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
                    "startRowIndex": standIndex + ROW_START,
                    "endRowIndex": standIndex + ROW_START + 1,
                    "startColumnIndex": i + 1,
                    "endColumnIndex": i + 2,
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
                    "startRowIndex": standIndex + ROW_START,
                    "endRowIndex": standIndex + ROW_START + 1,
                    "startColumnIndex": i + 1,
                    "endColumnIndex": i + 2,
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

# Write request to API
sheets_service.spreadsheets().batchUpdate(
    spreadsheetId=spreadsheet.id, body={"requests": requests}
).execute()

print(f"Schedule uploaded: {spreadsheet.url}")

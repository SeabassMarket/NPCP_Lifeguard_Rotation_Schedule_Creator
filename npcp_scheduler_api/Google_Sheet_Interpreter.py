from typing import List
from dataclasses import dataclass

import numpy as np


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
            raise TypeError("call is none - it was not set in JSON body")
        self._call = call

    @property
    def spreadsheet(self):
        return self._spreadsheet

    def interpret(self):
        if self._call == "preview":
            return self.preview()

        if self._call == "calculate":
            return self.calculate()

        raise ValueError("Call not set to a valid value")

    def preview(self):
        names = []

        for sheet in self._spreadsheet.sheets:
            names.append(sheet.name)

        return names

    def calculate(self):
        return "Sigma"

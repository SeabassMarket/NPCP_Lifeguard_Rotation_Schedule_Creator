# Import Libraries
import tkinter as tk
from tkinter import ttk
from tkinter import font
from StaticAppInfo import StaticAppInfo
from Time import Time

"""This class will house the frames that go into the overall schedule frame.
This will allow for organization and is also useful because each of the
event frames are very similar. By packing these on top of one another,
it decreases dependencies and makes each section more independent"""


class EventFrame:
    def __init__(
        self,
        parentFrame,
        row,
        staticAppInfo,
        labelText="",
        root="",
        titleFont="",
        entryFont="",
        errorFont="",
        eventLabelFont="",
        typeFrame="",
        defaultList="",
        timeEvent=True,
        eventType="",
        eventDescriptor="",
        frameDescriptor="",
        characterLimit=2,
        counter=False,
    ):
        # Create first instance variables
        self._parentFrame = parentFrame
        self._row = row

        # Initialize the counter variable
        if isinstance(counter, bool):
            self._counter = counter
        else:
            self._counter = False

        # Initialize the character limit when adding new events
        if isinstance(characterLimit, int):
            self._characterLimit = characterLimit
        else:
            self._characterLimit = 2

        # Initialize frame descriptor instance variable
        if isinstance(frameDescriptor, str):
            self._frameDescriptor = frameDescriptor
        else:
            self._frameDescriptor = ""

        # Initialize event descriptor instance variable
        if isinstance(eventDescriptor, str):
            self._eventDescriptor = eventDescriptor
        else:
            self._eventDescriptor = ""

        # Initialize event type instance variable
        if isinstance(eventType, str):
            self._eventType = eventType
        else:
            self._eventType = ""

        # Initialize label text if this class is being used as a glorified label
        if isinstance(labelText, str):
            self._labelText = labelText
        else:
            self._labelText = ""

        # Establish that staticAppInfo should be a StaticAppInfo object
        if isinstance(staticAppInfo, StaticAppInfo):
            self._staticAppInfo = staticAppInfo
        else:
            self._staticAppInfo = StaticAppInfo("ERROR")
            print("ERROR, STATIC APP INFO NOT INITIALIZED")

        # Create buttons for possible future and button data
        self._setDefaultButton = ttk.Button()
        self._addButton = ttk.Button()
        self._removeAllButton = ttk.Button()

        # Create entry frame for possible future
        self._entryFrame = tk.Frame()

        # Create event-related data for possible future
        self._events = []
        self._eventWidgets = dict()
        self._eventEntries = dict()
        self._counters = dict()

        # Set the name of the frame to the name given, if nonexistent set the name to "undefined"
        if isinstance(typeFrame, str) and len(typeFrame) > 0:
            self._typeFrame = typeFrame
        else:
            self._typeFrame = "undefined"

        # Create fonts
        if isinstance(titleFont, font.Font):
            self._titleFont = titleFont
        elif isinstance(titleFont, str):
            self._titleFont = staticAppInfo.getFont(titleFont.lower())

        # Create the event frame that's put into the schedule frame
        self._overallEventFrame = tk.Frame(
            self._parentFrame,
            background=self._staticAppInfo.getColor(self._frameDescriptor),
        )

        # Place the overall event frame
        self._overallEventFrame.grid(row=self._row, column=0, sticky="nw")

        # Create the title sub frames within the overall event frame
        self._titleFrame = tk.Frame(
            self._overallEventFrame,
            background=self._staticAppInfo.getColor(self._frameDescriptor),
        )

        # Place the title sub frames
        self._titleFrame.pack(side="top", fill="x", anchor="w")

        # Create and place the title
        if len(eventType) > 0:
            if eventDescriptor == eventType:
                self._title = ttk.Label(
                    self._titleFrame,
                    text="Enter " + eventType.lower() + "s below:",
                    foreground=self._staticAppInfo.getColor("Default"),
                    background=self._staticAppInfo.getColor(self._frameDescriptor),
                    font=self._titleFont,
                )
            else:
                self._title = ttk.Label(
                    self._titleFrame,
                    text='Enter "'
                    + eventType.lower()
                    + '" '
                    + eventDescriptor
                    + "s below:",
                    foreground=self._staticAppInfo.getColor("Default"),
                    background=self._staticAppInfo.getColor(self._frameDescriptor),
                    font=self._titleFont,
                )
        else:
            self._title = ttk.Label(
                self._titleFrame,
                text=labelText,
                foreground=self._staticAppInfo.getColor("Default"),
                background=self._staticAppInfo.getColor(self._frameDescriptor),
                font=self._titleFont,
            )
        self._title.grid(row=0, column=0, sticky="NW", padx=5)

        # Create button stuff if buttons requested
        if isinstance(root, tk.Tk):
            # Instantiate root (already checked in very first if)
            self._root = root

            # Create fonts
            # Check entry font and create default if none given
            if isinstance(entryFont, font.Font):
                self._entryFont = entryFont
            else:
                self._entryFont = staticAppInfo.getFont(entryFont.lower())
            # Check if an error font exists and create default if none is given
            if isinstance(errorFont, font.Font):
                self._errorFont = errorFont
            else:
                self._errorFont = staticAppInfo.getFont(errorFont.lower())
            # Check if an error font exists and create default if none is given
            if isinstance(eventLabelFont, font.Font):
                self._eventLabelFont = eventLabelFont
            else:
                self._eventLabelFont = staticAppInfo.getFont(eventLabelFont.lower())

            # Check if a default list is given
            valid = True
            if isinstance(defaultList, list):
                for string in defaultList:
                    if not isinstance(string, str):
                        valid = False
                    elif len(string) > self._characterLimit:
                        valid = False
            else:
                valid = False
            if valid:
                self._defaultList = defaultList
            else:
                self._defaultList = []
            # Check if it is a timeEvent, if there's no specification it defaults to true
            if isinstance(timeEvent, bool):
                self._timeEvent = timeEvent
            else:
                self._timeEvent = True
            self.buttonFrameSetup()

    def buttonFrameSetup(self):
        # Create buttons in the title frame
        # Set Default
        if self._eventDescriptor == self._eventType:
            self._setDefaultButton = ttk.Button(
                self._titleFrame,
                text="Set Default "
                + self._staticAppInfo.capitalizeTitle(self._eventType)
                + "s",
                command=self.setDefaultEvents,
            )
        else:
            self._setDefaultButton = ttk.Button(
                self._titleFrame,
                text="Set Default "
                + self._staticAppInfo.capitalizeTitle(self._eventType)
                + " "
                + self._staticAppInfo.capitalizeTitle(self._eventDescriptor)
                + "s",
                command=self.setDefaultEvents,
            )
        self._setDefaultButton.grid(row=0, column=1, sticky="w", padx=5)
        self._staticAppInfo.appendButtonToDisable(self._setDefaultButton)

        # Add at beginning
        self._addButton = ttk.Button(
            self._titleFrame,
            text="+",
            command=lambda index=-1: self.addEventPopup(index),
        )
        self._addButton.grid(row=0, column=2, sticky="w", padx=5)
        self._staticAppInfo.appendButtonToDisable(self._addButton)

        # Remove all
        self._removeAllButton = ttk.Button(
            self._titleFrame, text="-", command=self.removeAllEvents
        )
        self._removeAllButton.grid(row=0, column=3, sticky="w", padx=5)
        self._staticAppInfo.appendButtonToDisable(self._removeAllButton)

        # Create and place entry frame
        self._entryFrame = tk.Frame(
            self._overallEventFrame,
            background=self._staticAppInfo.getColor(self._frameDescriptor),
        )
        self._entryFrame.pack(side="top", fill="none", expand=False, anchor="w")

    def setDefaultEvents(self):
        # Re-check against all the other event frames
        otherEvents = self._staticAppInfo.getCopyFullEventsSpecific(
            self._eventDescriptor
        )
        for event in self._events:
            otherEvents.pop(otherEvents.index(event))
        valid = True
        for event in self._defaultList:
            if event in otherEvents:
                valid = False
        if valid:
            self._events = list(self._defaultList)
            self.updateEventEntries()

    # Updates the event entries
    def updateEventEntries(self):
        # Remove all the old previous events  from the full static list (prevents duplicates and messiness)
        self._staticAppInfo.removeEventsFromFullList(
            list(self._eventWidgets.keys()), self._eventDescriptor
        )

        # Find which buttons exist before the process (these will be removed later)
        previousButtons = []
        for key in self._eventWidgets:
            for widget in self._eventWidgets[key]:
                if isinstance(widget, ttk.Button):
                    previousButtons.append(widget)

        # Remove the old buttons from buttons to disable (optimizing storage)
        self._staticAppInfo.removeButtonsFromListToDisable(previousButtons)

        """HERE STARTS THE UPDATING AND CREATION OF NEW WIDGETS"""

        # Runs if this type of event frame has entries
        if self._timeEvent:
            # Reset old data
            self._eventEntries.clear()

        # Clears the counters dictionary if the event frame has counters
        if self._counter:
            # Reset old data
            self._counters.clear()

        # Destroys old widgets
        for key in self._eventWidgets:
            # Runs if this type of event frame has entries (preserve entry fields)
            if self._timeEvent:
                self._eventEntries[key] = [
                    self._eventWidgets[key][1][1].get(),
                    self._eventWidgets[key][2][1].get(),
                ]
            # Run this to preserve the counter fields if those are available
            if self._counter:
                counterIndex = 0
                for i in range(0, len(self._eventWidgets[key])):
                    if (
                        isinstance(self._eventWidgets[key][i], list)
                        and len(self._eventWidgets[key][i]) == 3
                    ):
                        if self._eventWidgets[key][i][2][0] == "1":
                            counterIndex = i
                self._counters[key] = self._eventWidgets[key][counterIndex][1].get()
            # Destroy widgets
            for widget in self._eventWidgets[key]:
                if isinstance(widget, tk.Widget):
                    widget.destroy()
                elif isinstance(widget, list):
                    if len(widget) > 0 and isinstance(widget[0], tk.Widget):
                        widget[0].destroy()

        # Clear dictionary of  event widgets
        self._eventWidgets.clear()

        # Reset frame size
        self._entryFrame.destroy()
        self._entryFrame = tk.Frame(
            self._overallEventFrame,
            background=self._staticAppInfo.getColor(self._frameDescriptor),
        )
        self._entryFrame.pack(side="top", fill="none", expand=False, anchor="w")

        # Create widgets for each letter of event given
        for i in range(0, len(self._events)):
            # Set dictionary values
            # Set the dictionary to an empty list
            self._eventWidgets[self._events[i]] = []
            # Create event label
            eventLabel = ttk.Label(
                self._entryFrame,
                text=self._staticAppInfo.capitalizeTitle(self._eventDescriptor)
                + " "
                + self._events[i]
                + ":",
                foreground=self._staticAppInfo.getColor("Default"),
                background=self._staticAppInfo.getColor(self._frameDescriptor),
                font=self._eventLabelFont,
            )
            self._eventWidgets[self._events[i]].append(eventLabel)
            # Runs if this type of event frame has entries (adds dropdown for times)
            if self._timeEvent:
                for k in range(0, 2):
                    selectedOption = tk.StringVar()
                    options = []
                    for t in range(0, 24 * 60, self._staticAppInfo.getTimeInterval()):
                        options.append(Time().setTimeWithMinutes(t).get12Time())
                    dropdown = ttk.Combobox(
                        self._entryFrame,
                        textvariable=selectedOption,
                        values=options,
                        state="readonly",
                        width=15,
                    )
                    dropdown.current(0)
                    self._eventWidgets[self._events[i]].append(
                        [dropdown, selectedOption, options]
                    )

            # Runs this if the type of event frame has counters
            if self._counter:
                selectedOption = tk.StringVar()
                options = []
                for k in range(1, 26):
                    options.append(str(k))
                dropdown = ttk.Combobox(
                    self._entryFrame,
                    textvariable=selectedOption,
                    values=options,
                    state="readonly",
                    width=5,
                )
                dropdown.current(0)
                self._eventWidgets[self._events[i]].append(
                    [dropdown, selectedOption, options]
                )

            # Create add button
            addButton = ttk.Button(
                self._entryFrame,
                text="+",
                command=lambda index=i: self.addEventPopup(index),
            )
            self._eventWidgets[self._events[i]].append(addButton)
            # Create remove button
            removeButton = ttk.Button(
                self._entryFrame,
                text="-",
                command=lambda index=i: self.removeEventEntry(index),
            )
            self._eventWidgets[self._events[i]].append(removeButton)
            # Create error message
            eventError = ttk.Label(
                self._entryFrame,
                text="ERROR, CHECK FORMATTING (? Button)",
                foreground=self._staticAppInfo.getColor("redError"),
                background=self._staticAppInfo.getColor(self._frameDescriptor),
                font=self._staticAppInfo.getFont("error"),
            )
            self._eventWidgets[self._events[i]].append(eventError)

            # Place widgets (NOTE: the -1 is so the error message isn't placed
            for j in range(0, len(self._eventWidgets[self._events[i]]) - 1):
                if isinstance(self._eventWidgets[self._events[i]][j], tk.Widget):
                    self._eventWidgets[self._events[i]][j].grid(
                        row=i, column=j, sticky="W", padx=5
                    )
                elif isinstance(self._eventWidgets[self._events[i]][j], list):
                    for obj in self._eventWidgets[self._events[i]][j]:
                        if isinstance(obj, tk.Widget):
                            obj.grid(row=i, column=j, sticky="W", padx=5)

        # Runs if this type of event frame has times
        if self._timeEvent:
            # Checking to see if any old data can be put back in the entries
            for eventKey in self._eventWidgets:
                if eventKey in self._eventEntries:
                    values = self._eventWidgets[eventKey][1][2]
                    comboOne = self._eventWidgets[eventKey][1][0]
                    comboOne.current(values.index(self._eventEntries[eventKey][0]))
                    comboTwo = self._eventWidgets[eventKey][2][0]
                    comboTwo.current(values.index(self._eventEntries[eventKey][1]))

        # Runs this if the event frame has counters
        if self._counter:
            for eventKey in self._eventWidgets:
                if eventKey in self._counters:
                    counterIndex = 0
                    for i in range(0, len(self._eventWidgets[eventKey])):
                        if (
                            isinstance(self._eventWidgets[eventKey][i], list)
                            and len(self._eventWidgets[eventKey][i]) == 3
                        ):
                            if self._eventWidgets[eventKey][i][2][0] == "1":
                                counterIndex = i
                    values = self._eventWidgets[eventKey][counterIndex][2]
                    combo = self._eventWidgets[eventKey][counterIndex][0]
                    combo.current(values.index(self._counters[eventKey]))

        """HERE MARKS THE END OF UPDATING AND CREATING THE WIDGETS"""

        # Add the new events to the full static list
        self._staticAppInfo.addEventsToFullListSpecific(
            self._events, self._eventDescriptor
        )

        # Add the new buttons to the static buttons to disable list
        newButtons = []
        for key in self._eventWidgets:
            for widget in self._eventWidgets[key]:
                if isinstance(widget, ttk.Button):
                    newButtons.append(widget)
        self._staticAppInfo.appendButtonListToDisable(newButtons)

    # Creates the popup where the user can add an entry
    def addEventPopup(self, index):
        # Disable buttons
        self._staticAppInfo.disableButtons()

        # Create toplevel popup
        popup = tk.Toplevel()
        popup.geometry("300x200+1000+400")
        popup.title("Add Event")
        popupFrame = tk.Frame(
            popup, background=self._staticAppInfo.getColor(self._frameDescriptor)
        )
        popupFrame.pack(fill=tk.BOTH, expand=True)

        # Create instruction text
        instructionText = ttk.Label(
            popupFrame,
            text="Enter event name:",
            foreground=self._staticAppInfo.getColor("Default"),
            background=self._staticAppInfo.getColor(self._frameDescriptor),
            font=self._staticAppInfo.getFont("Default"),
        )
        instructionText.grid(row=0, column=0, sticky="W")

        # Create event entry
        eventEntry = ttk.Entry(popupFrame, font=self._entryFont)
        eventEntry.grid(row=1, column=0, sticky="W", padx=5)
        # Bind the enter action on the keyboard to adding the entry
        eventEntry.bind(
            "<Return>",
            lambda event,
            i=index,
            entryField=eventEntry,
            body=popup,
            frame=popupFrame: self.addEventEntry(i, entryField, body, frame),
        )

        # Create enter button
        enterButton = ttk.Button(
            popupFrame,
            text="Add",
            command=lambda i=index,
            entryField=eventEntry,
            body=popup,
            frame=popupFrame: self.addEventEntry(i, entryField, body, frame),
        )
        enterButton.grid(row=2, column=0, sticky="W", padx=5, pady=5)

        # Check to see if the popup has been destroyed
        self.checkPopup(popup)

    # Checks to see if the popup has been destroyed so it can reactivate the buttons
    def checkPopup(self, popup):
        # Check to see if popup exists and is an object
        if popup and not popup.winfo_exists():
            # Turns all the buttons back on
            self._staticAppInfo.enableButtons()
            popup = None

        # Re-check
        self._root.after(100, lambda: self.checkPopup(popup))

    # Add an event entry field
    def addEventEntry(self, index, eventEntry, body, frame):
        # If the event entry is not a duplicate and is less or equal to the character limit,
        # Add the event
        if (
            not (
                eventEntry.get()
                in self._staticAppInfo.getCopyFullEventsSpecific(self._eventDescriptor)
            )
            and 0 < len(eventEntry.get()) <= self._characterLimit
            and eventEntry.get().isalnum()
        ):
            self._events.insert(index + 1, eventEntry.get())
            body.destroy()
            self.updateEventEntries()
            self._staticAppInfo.enableButtons()
        # Otherwise display an error message
        else:
            error = ttk.Label(
                frame,
                text="Error, either duplicate\nor more than "
                + str(self._characterLimit)
                + " character(s)\nor no characters\nor invalid characters",
                foreground=self._staticAppInfo.getColor("Error"),
                background=self._staticAppInfo.getColor(self._frameDescriptor),
                font=self._errorFont,
                anchor="w",
            )
            error.grid(
                row=eventEntry.grid_info()["row"] + 2, column=0, padx=5, sticky="NW"
            )

    # Removes all the events from the event frame
    def removeAllEvents(self):
        self._events = []
        self.updateEventEntries()

    # Removes a single event entry
    def removeEventEntry(self, index):
        self._events.pop(index)
        self.updateEventEntries()

    # This function is called by the schedule frame parent object to obtain the data
    # in this event frame
    def submitData(self):
        # Dictionary for all the event times
        eventTimes = dict()

        # Set errors to false
        errors = False

        # If this is an event frame with times
        if self._timeEvent:
            # Initialize some variables for calculations
            rowCount = 0

            # For each list of widgets in the eventWidgets dictionary
            for key in self._eventWidgets:
                # Get widgets
                widgets = self._eventWidgets[key]

                # Event error is initially false
                eventError = False

                # Check to see if the time is formatted correctly
                columnError = len(widgets) - 1

                # Get the times
                time1 = widgets[1][1].get()
                time1 = Time().set12Time(int(time1[0:2]), int(time1[3:5]), time1[6:8])
                time2 = widgets[2][1].get()
                time2 = Time().set12Time(int(time2[0:2]), int(time2[3:5]), time2[6:8])

                # There is an event error if time 2 is not after time 1
                if time1.getMinutes() > time2.getMinutes():
                    eventError = True

                # If there is an event error, turn on errors for the whole function and turn on the warning
                if eventError:
                    errors = True
                    widgets[columnError].grid(
                        row=rowCount, column=columnError, sticky="W", padx=5
                    )
                # If there is no event error, get rid of it
                else:
                    widgets[columnError].grid_forget()
                    eventTimes[key] = [time1, time2]

                # Add the row count so next time we look at the next row (for event error message)
                rowCount += 1

        # If this event frame doesn't have times
        else:
            for event in self._events:
                startTime = Time(hour=0, minute=0)
                endTime = "end of day"
                eventTimes[event] = [startTime, endTime]

        # If this event frame has counters, append the count values
        if self._counter:
            for key in self._eventWidgets:
                counterIndex = 0
                for i in range(0, len(self._eventWidgets[key])):
                    if (
                        isinstance(self._eventWidgets[key][i], list)
                        and len(self._eventWidgets[key][i]) == 3
                    ):
                        if self._eventWidgets[key][i][2][0] == "1":
                            counterIndex = i
                count = self._eventWidgets[key][counterIndex][1].get()
                eventTimes[key].append(count)

        # If there are no errors anywhere in this eventFrame, return the event time dictionary
        if not errors:
            return eventTimes
        # If there are errors, return an error message
        else:
            return "ERROR"

    # Returns the event type string
    def getEventType(self):
        return self._eventType

    @staticmethod
    def placeButtonToSide(button, widget, padx, pady):
        button.place(
            x=widget.winfo_x() + widget.winfo_width() + padx, y=widget.winfo_y() + pady
        )

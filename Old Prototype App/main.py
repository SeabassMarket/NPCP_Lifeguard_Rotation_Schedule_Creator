# Import libraries
import tkinter as tk
from tkinter import ttk
from tkinter import font


class App:
    # Initial run function
    def __init__(self):
        # Root
        self._root = tk.Tk()
        self._root.geometry("1000x1000+800+200")
        self._root.title(
            "New Providence Community Pool Lifeguard Rotation Schedule Maker"
        )

        # Initialization of some sub-frames
        self._scheduleCanvasFrame = tk.Frame(self._root)
        self._scheduleCanvas = tk.Canvas(self._root)
        self._scheduleFrame = tk.Frame(self._root)
        self._scheduleQuestionCanvas = tk.Canvas(self._root)
        self._homeFrame = tk.Frame(self._root)

        # Initialization of schedule initial variables
        # For up stands
        self._upStands = []
        self._upStandWidgets = dict()
        self._upStandEntries = dict()
        self._defaultUpStandButton = ttk.Button()
        self._addUpStandButton = ttk.Button()
        self._removeAllUpStandButton = ttk.Button()

        # For the down stands buttons
        self._secondInstructionText = ttk.Label()
        self._timelyDownStandsLabel = ttk.Label()
        self._timelyDownStandButtons = []
        self._timelyDownStands = []
        self._timelyDownStandEntries = dict()
        self._timelyDownStandWidgets = dict()

        # For the buttons at the bottom of the page
        self._invisibleLabel = ttk.Button()
        self._scheduleButtonsToMoveDown = []

        # Font for entries
        self._entryFont = font.Font(family="Segoe UI", size=11)

        # Font for section headers
        self._headerFont = font.Font(family="Arial", size=30, underline=True)

        # Mother Frame
        self._motherFrame = tk.Frame(self._root)
        self._motherFrame.pack(fill="both", expand=True)

        # Set up home page
        self.setUpHomePage()

        # Set up schedule page
        self.setUpSchedulePage()

        # Set up lifeguard page

        # Concluding code to make the app appear
        self._homeFrame.tkraise()
        self._root.mainloop()
        return

    # Sets up the home page with widgets
    def setUpHomePage(self):
        # Home Frame
        self._homeFrame = tk.Frame(self._motherFrame, background="#08b0dd")
        self._homeFrame.place(relwidth=1, relheight=1)

        # Label for Home Page
        homeText = ttk.Label(
            self._homeFrame,
            text="Home",
            foreground="Black",
            background="#08b0dd",
            font=("Arial", 100),
        )
        homeText.pack(side=tk.TOP, anchor=tk.W, padx=5)

        # Open stand schedule button
        openScheduleButton = ttk.Button(
            self._homeFrame, text="Set Stand Schedule", command=self.openStandSchedule
        )
        openScheduleButton.pack(anchor=tk.W, padx=10)

    # Sets up the schedule page with widgets
    def setUpSchedulePage(self):
        # Create frame just for canvas and scroll bar
        self._scheduleCanvasFrame = tk.Frame(self._motherFrame)
        self._scheduleCanvasFrame.place(relwidth=1, relheight=1)

        # Create canvas and scrollbar in canvas frame
        self._scheduleCanvas = tk.Canvas(
            self._scheduleCanvasFrame, background="#007994"
        )
        scrollbar = ttk.Scrollbar(
            self._scheduleCanvasFrame,
            orient="vertical",
            command=self._scheduleCanvas.yview,
        )

        # Bind canvas and scrollbar together
        self._scheduleCanvas.configure(yscrollcommand=scrollbar.set)

        # Scrollbar and schedule pack
        scrollbar.pack(side="right", fill="y")
        self._scheduleCanvas.pack(side="left", fill="both", expand=True)

        # Create schedule frame in canvas
        self._scheduleFrame = tk.Frame(self._scheduleCanvas, background="#007994")

        # Place schedule frame in window
        self._scheduleCanvas.create_window(
            (0, 0), window=self._scheduleFrame, anchor="nw"
        )

        # Label for schedule page
        scheduleText = ttk.Label(
            self._scheduleFrame,
            text="Schedule     ",
            foreground="Black",
            background="#007994",
            font=("Arial", 100),
        )
        scheduleText.grid(row=0, column=0, columnspan=10, sticky="W")

        # Instruction text
        instructionText = ttk.Label(
            self._scheduleFrame,
            text='Enter "up" stands below:',
            foreground="Black",
            background="#007994",
            font=self._headerFont,
        )
        instructionText.grid(row=1, column=0, columnspan=6, sticky="NW", padx=5)

        # Create button to set default
        self._defaultUpStandButton = ttk.Button(
            self._scheduleFrame,
            text="Set Default Up Stands",
            command=self.setDefaultUpStands,
        )
        self._root.after(
            100,
            lambda: self.placeButtonToSide(
                self._defaultUpStandButton, instructionText, padx=7, pady=14
            ),
        )

        # Create button to add an entry
        self._addUpStandButton = ttk.Button(
            self._scheduleFrame,
            text="+",
            command=lambda index=-1: self.addUpStandPopup(index),
        )
        self._root.after(
            100,
            lambda: self.placeButtonToSide(
                self._addUpStandButton, instructionText, padx=140, pady=14
            ),
        )

        # Create button to remove all entries
        self._removeAllUpStandButton = ttk.Button(
            self._scheduleFrame, text="-", command=self.removeAllUpStands
        )
        self._root.after(
            100,
            lambda: self.placeButtonToSide(
                self._removeAllUpStandButton, instructionText, padx=227, pady=14
            ),
        )

        # Create second instruction text
        self._secondInstructionText = ttk.Label(
            self._scheduleFrame,
            text='Enter "down" stands below:',
            foreground="Black",
            background="#007994",
            font=self._headerFont,
        )

        # Create label for timely down stands section
        self._timelyDownStandsLabel = ttk.Label(
            self._scheduleFrame,
            text="Enter timely down stands:",
            foreground="Black",
            background="#007994",
            font=("Arial", 25),
        )

        # Creates the button to set the default timely down stands
        defaultTimelyDownStandButton = ttk.Button(
            self._scheduleFrame,
            text="Set Default Timely Down Stands",
            command=self.setDefaultTimelyDownStands,
        )
        self._timelyDownStandButtons.append([defaultTimelyDownStandButton, 7, 11])

        # Creates the button to add timely down stands
        addTimelyDownStandButton = ttk.Button(
            self._scheduleFrame, text="+", command=self.addTimelyDownStand
        )
        self._timelyDownStandButtons.append([addTimelyDownStandButton, 195, 11])

        # Creates the button to remove timely down stands
        removeTimelyDownStandButton = ttk.Button(
            self._scheduleFrame, text="-", command=self.removeAllTimelyDownStands
        )
        self._timelyDownStandButtons.append([removeTimelyDownStandButton, 282, 11])

        # Invisible reference for schedule buttons to move down
        self._invisibleLabel = ttk.Label(
            self._scheduleFrame,
            text="",
            foreground="Black",
            background="#007994",
            font=("Arial", 20),
        )

        # Create back button
        backHomeButton = ttk.Button(
            self._scheduleFrame, text="Back Home", command=self.backHome
        )
        self._scheduleButtonsToMoveDown.append([backHomeButton, 0, 7])

        # Create question info button
        questionButton = ttk.Button(
            self._scheduleFrame, text="?", command=self.openScheduleQuestionPopup
        )
        self._scheduleButtonsToMoveDown.append([questionButton, 85, 7])

        # Set locations of schedule buttons to move down
        self._root.after(100, lambda: self.updateScheduleBottomButtons())

        self.instantiateScheduleScrolling()

    # Sets the default for the timely down stands
    def setDefaultTimelyDownStands(self):
        defaultStands = ["DT", "ST", "SU", "CU"]
        overlappingStands = []
        for value in defaultStands:
            if value in self._upStandWidgets:
                overlappingStands.append(value)
        if len(overlappingStands) == 0:
            self._timelyDownStands = list(defaultStands)
            self.updateTimelyDownStands()
        else:
            self.overlappingStandError(overlappingStands)

    # Adds a timely down stand to the beginning
    def addTimelyDownStand(self):
        pass

    # Removes all the timely down stands
    def removeAllTimelyDownStands(self):
        self._timelyDownStands = []
        self.updateTimelyDownStands()

    # Command for the buttons next to each entry to insert a timely down stand entry
    def addTimelyDownStandEntry(self, index):
        pass

    # Command for the buttons next to each entry to remove the timely down stand entry
    def removeTimelyDownStandEntry(self, index):
        # Pop out the stand from the timely down stands list and refresh the entries
        self._timelyDownStands.pop(index)
        self.updateTimelyDownStands()

    # Update the timely down stands
    def updateTimelyDownStands(self):
        # Reset old data
        self._timelyDownStandEntries.clear()

        # Preserve entry fields
        for key in self._timelyDownStandWidgets:
            self._timelyDownStandEntries[key] = self._timelyDownStandWidgets[key][
                1
            ].get()
            for widget in self._timelyDownStandWidgets[key]:
                widget.destroy()

        # Clear dictionary of up stand widgets
        self._timelyDownStandWidgets.clear()

        # Create widgets for each letter of stand given
        for i in range(0, len(self._timelyDownStands)):
            timelyDownStandLabel = ttk.Label(
                self._scheduleFrame,
                text="Stand " + self._timelyDownStands[i] + ":",
                foreground="Black",
                background="#007994",
                font=("Arial", 20),
            )
            timelyDownStandEntry = ttk.Entry(self._scheduleFrame, font=self._entryFont)
            addButton = ttk.Button(
                self._scheduleFrame,
                text="+",
                command=lambda index=i: self.addTimelyDownStandEntry(index),
            )
            removeButton = ttk.Button(
                self._scheduleFrame,
                text="-",
                command=lambda index=i: self.removeTimelyDownStandEntry(index),
            )

            # Set dictionary value
            self._timelyDownStandWidgets[self._timelyDownStands[i]] = [
                timelyDownStandLabel,
                timelyDownStandEntry,
                addButton,
                removeButton,
            ]

        # Place the widgets in the grid
        self.updateTimelyDownStandsGrid()

        # Checking to see if any old data can be put back in the entries
        for key in self._timelyDownStandWidgets:
            if key in self._timelyDownStandEntries:
                self._timelyDownStandWidgets[key][1].insert(
                    0, self._timelyDownStandEntries[key]
                )

        # Move down schedule buttons to move down (like the back home button)
        self.updateScheduleBottomButtons()

        # Refresh scrolling for screen
        self.instantiateScheduleScrolling()

    def updateTimelyDownStandsGrid(self):
        # Place widgets in grid
        for i in range(0, len(self._timelyDownStands)):
            self._timelyDownStandWidgets[self._timelyDownStands[i]][0].grid(
                row=len(self._upStandWidgets) + i + 4, column=0, sticky="W", padx=5
            )
            self._timelyDownStandWidgets[self._timelyDownStands[i]][1].grid(
                row=len(self._upStandWidgets) + i + 4, column=1, sticky="W"
            )
            self._timelyDownStandWidgets[self._timelyDownStands[i]][2].grid(
                row=len(self._upStandWidgets) + i + 4, column=2, sticky="W"
            )
            self._timelyDownStandWidgets[self._timelyDownStands[i]][3].grid(
                row=len(self._upStandWidgets) + i + 4, column=3, sticky="W"
            )

    # Instantiate schedule frame and canvas scrolling
    def instantiateScheduleScrolling(self):
        self._scheduleFrame.update_idletasks()
        self._scheduleCanvas.config(scrollregion=self._scheduleCanvas.bbox("all"))
        self._scheduleCanvas.bind_all("<MouseWheel>", self.onMouseWheelSchedule)

    # Scrolling for schedule page
    def onMouseWheelSchedule(self, event):
        self._scheduleCanvas.yview_scroll(-1 * (event.delta // 120), "units")

    # Opens up the stand schedule page
    def openStandSchedule(self):
        self._scheduleCanvasFrame.tkraise()

    # Update locations of schedule buttons to move down
    def updateScheduleBottomButtons(self):
        self._secondInstructionText.grid(
            row=2 + len(self._upStandWidgets),
            column=0,
            padx=5,
            pady=0,
            sticky="NW",
            columnspan=7,
        )
        self._timelyDownStandsLabel.grid(
            row=3 + len(self._upStandWidgets),
            column=0,
            padx=5,
            pady=0,
            sticky="NW",
            columnspan=6,
        )
        total = 4 + len(self._upStandWidgets) + len(self._timelyDownStandWidgets)
        self._invisibleLabel.grid(row=total, column=0, padx=5, pady=0, sticky="NW")
        self._root.after(20, lambda: self.updatePlaceButtonsBelow())
        self._root.after(20, lambda: self.updateTimelyDownStandButtons())

    # Updates the schedule buttons that have to be moved down to the bottom of everything
    def updatePlaceButtonsBelow(self):
        for button in self._scheduleButtonsToMoveDown:
            self.placeButtonToSide(
                button[0], self._invisibleLabel, button[1], button[2]
            )

    # Updates the buttons for timely down stands
    def updateTimelyDownStandButtons(self):
        for button in self._timelyDownStandButtons:
            self.placeButtonToSide(
                button[0], self._timelyDownStandsLabel, button[1], button[2]
            )

    # Default values for up stands, creates the entries for each
    def setDefaultUpStands(self):
        defaultStands = ["A", "B", "C", "E", "F", "G", "H", "I", "J", "K", "T", "S"]
        overlappingStands = []
        for value in defaultStands:
            if value in self._timelyDownStandWidgets:
                overlappingStands.append(value)
        if len(overlappingStands) == 0:
            self._upStands = list(defaultStands)
            self.updateUpStandEntries()
        else:
            self.overlappingStandError(overlappingStands)

    # Popup for overlapping stands error
    @staticmethod
    def overlappingStandError(overlappingStands):
        # Create popup
        popup = tk.Toplevel()
        popup.geometry("500x200+1000+500")
        popup.title("Overlapping Stands Error")
        popupFrame = tk.Frame(popup, background="#007994")
        popupFrame.pack(fill=tk.BOTH, expand=True)

        # Create error text
        errorText = ttk.Label(
            popupFrame,
            text="Cannot add default stands, the following\n"
            "stands overlap in another section:",
            foreground="#A50000",
            background="#007994",
            font=("Arial", 20),
        )
        errorText.grid(row=0, column=0, padx=5)

        # Create label for overlapping stands making the error
        overlappingStandsString = ""
        for i in range(0, len(overlappingStands)):
            overlappingStandsString += overlappingStands[i]
            if i != len(overlappingStands) - 1:
                overlappingStandsString += ", "

        overlappingStandsLabel = ttk.Label(
            popupFrame,
            text=overlappingStandsString,
            foreground="#A50000",
            background="#007994",
            font=("Arial", 15),
            anchor="w",
        )
        overlappingStandsLabel.grid(row=1, column=0, padx=5, sticky="NW")

    # Update the up stand entries based on the up stands list
    def updateUpStandEntries(self):
        # Reset old data
        self._upStandEntries.clear()

        # Preserve entry fields
        for key in self._upStandWidgets:
            self._upStandEntries[key] = self._upStandWidgets[key][1].get()
            for widget in self._upStandWidgets[key]:
                widget.destroy()

        # Clear dictionary of up stand widgets
        self._upStandWidgets.clear()

        # Create widgets for each letter of stand given
        for i in range(0, len(self._upStands)):
            standLabel = ttk.Label(
                self._scheduleFrame,
                text="Stand " + self._upStands[i] + ":",
                foreground="Black",
                background="#007994",
                font=("Arial", 20),
            )
            standEntry = ttk.Entry(self._scheduleFrame, font=self._entryFont)
            addButton = ttk.Button(
                self._scheduleFrame,
                text="+",
                command=lambda index=i: self.addUpStandPopup(index),
            )
            removeButton = ttk.Button(
                self._scheduleFrame,
                text="-",
                command=lambda index=i: self.removeUpStandEntry(index),
            )

            # Set dictionary value
            self._upStandWidgets[self._upStands[i]] = [
                standLabel,
                standEntry,
                addButton,
                removeButton,
            ]

            # Place buttons
            self._upStandWidgets[self._upStands[i]][0].grid(
                row=i + 2, column=0, sticky="W", padx=5
            )
            self._upStandWidgets[self._upStands[i]][1].grid(
                row=i + 2, column=1, sticky="W"
            )
            self._upStandWidgets[self._upStands[i]][2].grid(
                row=i + 2, column=2, sticky="W"
            )
            self._upStandWidgets[self._upStands[i]][3].grid(
                row=i + 2, column=3, sticky="W"
            )

        # Checking to see if any old data can be put back in the entries
        for key in self._upStandWidgets:
            if key in self._upStandEntries:
                self._upStandWidgets[key][1].insert(0, self._upStandEntries[key])

        # Update the location of the timely down stands grid
        self.updateTimelyDownStandsGrid()

        # Move down schedule buttons to move down (like the back home button)
        self.updateScheduleBottomButtons()

        # Refresh scrolling for screen
        self.instantiateScheduleScrolling()

    # Brings up the home page
    def backHome(self):
        self._homeFrame.tkraise()

    # Brings up information/question popup
    def openScheduleQuestionPopup(self):
        # Create toplevel popup
        popup = tk.Toplevel()
        popup.geometry("500x400+1050+450")
        popup.title("FAQs/Tutorial")

        # Create canvas and scrollbar in canvas frame
        self._scheduleQuestionCanvas = tk.Canvas(popup, background="#007994")
        scrollbar = ttk.Scrollbar(
            popup, orient="vertical", command=self._scheduleQuestionCanvas.yview
        )

        # Bind canvas and scrollbar together
        self._scheduleQuestionCanvas.configure(yscrollcommand=scrollbar.set)

        # Scrollbar and schedule pack
        scrollbar.pack(side="right", fill="y")
        self._scheduleQuestionCanvas.pack(side="left", fill="both", expand=True)

        # Create schedule frame in canvas
        popupFrame = tk.Frame(self._scheduleQuestionCanvas, background="#007994")

        # Place schedule frame in window
        self._scheduleQuestionCanvas.create_window(
            (0, 0), window=popupFrame, anchor="nw"
        )

        # Create label for format information
        formatLabel = ttk.Label(
            popupFrame,
            text="How to enter/format information:",
            foreground="Black",
            background="#007994",
            font=("Arial", 20),
        )
        formatLabel.grid(row=0, column=0, sticky="NW")

        # Create label for format example
        formatExample = ttk.Label(
            popupFrame,
            text='"##:##-##:##", example: "9:00-21:00"',
            foreground="#404040",
            background="#007994",
            font=("Arial", 15),
        )
        formatExample.grid(row=1, column=0, sticky="NW")

        # Create label for format explanation
        formatExplanation = ttk.Label(
            popupFrame,
            text="-->This will set the time from 9:00AM to 9:00PM\n"
            "Use 24-hour time when entering",
            foreground="#404040",
            background="#007994",
            font=("Arial", 15),
            anchor="w",
        )
        formatExplanation.grid(row=2, column=0, sticky="NW")

        # Create the first invisible spacer
        invisibleSpacer1 = ttk.Label(popupFrame, text="", background="#007994")
        invisibleSpacer1.grid(row=3, column=0, pady=5)

        # Create label for the subtract button label
        subtractButtonLabel = ttk.Label(
            popupFrame,
            text='What the "-" buttons do:',
            foreground="Black",
            background="#007994",
            font=("Arial", 20),
        )
        subtractButtonLabel.grid(row=4, column=0, sticky="NW")

        # Create label for the subtract button explanation
        subtractButtonExplanation = ttk.Label(
            popupFrame,
            text='-->The one at the top next to the "Set Default\n'
            'Up Stands" button removes all current stand entry\n'
            "fields (be careful!). The one next to each of the\n"
            "entry fields just removes the one it's next to.",
            foreground="#404040",
            background="#007994",
            font=("Arial", 15),
            anchor="w",
        )
        subtractButtonExplanation.grid(row=5, column=0, sticky="NW")

        # Create the second invisible spacer
        invisibleSpacer2 = ttk.Label(popupFrame, text="", background="#007994")
        invisibleSpacer2.grid(row=6, column=0, pady=5)

        # Create label for the add button label
        addButtonLabel = ttk.Label(
            popupFrame,
            text='What the "+" buttons do:',
            foreground="Black",
            background="#007994",
            font=("Arial", 20),
        )
        addButtonLabel.grid(row=7, column=0, sticky="NW")

        # Create label for the add button explanation
        addButtonExplanation = ttk.Label(
            popupFrame,
            text='-->The one at the top next to the "Set Default\n'
            'Up Stands" brings up a popup to add a stand entry\n'
            "field. Once the user presses the add button on the\n"
            "popup, the entry will be added to the top of the\n"
            "entries. The one next to the entry fields will add\n"
            "the stand entry in the next one.\n"
            "*Note: the order won't affect calculations",
            foreground="#404040",
            background="#007994",
            font=("Arial", 15),
            anchor="w",
        )
        addButtonExplanation.grid(row=8, column=0, sticky="NW")

        # Create the third invisible spacer
        invisibleSpacer3 = ttk.Label(popupFrame, text="", background="#007994")
        invisibleSpacer3.grid(row=9, column=0, pady=5)

        # Create label for difference between up stands and down stands
        standDifferenceLabel = ttk.Label(
            popupFrame,
            text='What the "+" buttons do:',
            foreground="Black",
            background="#007994",
            font=("Arial", 20),
        )
        standDifferenceLabel.grid(row=10, column=0, sticky="NW")

        # Create label for difference between up stands and down stands explanation
        standDifferenceExplanation = ttk.Label(
            popupFrame,
            text='-->The one at the top next to the "Set Default\n'
            'Up Stands" brings up a popup to add a stand entry\n'
            "field. Once the user presses the add button on the\n"
            "popup, the entry will be added to the top of the\n"
            "entries. The one next to the entry fields will add\n"
            "the stand entry in the next one.\n"
            "*Note: the order won't affect calculations",
            foreground="#404040",
            background="#007994",
            font=("Arial", 15),
            anchor="w",
        )
        standDifferenceExplanation.grid(row=11, column=0, sticky="NW")

        # Instantiate scrolling with canvas
        popupFrame.update_idletasks()
        self._scheduleQuestionCanvas.config(
            scrollregion=self._scheduleQuestionCanvas.bbox("all")
        )
        self._scheduleQuestionCanvas.bind_all(
            "<MouseWheel>", self.onMouseWheelScheduleQuestion
        )

    # Scrolling for schedule page
    def onMouseWheelScheduleQuestion(self, event):
        self._scheduleQuestionCanvas.yview_scroll(-1 * (event.delta // 120), "units")

    # Creates the popup where the user can add an entry
    def addUpStandPopup(self, index):
        # Disable buttons
        self.disableScheduleButtons()

        # Create toplevel popup
        popup = tk.Toplevel()
        popup.geometry("300x200+1000+400")
        popup.title("Add Stand")
        popupFrame = tk.Frame(popup, background="#007994")
        popupFrame.pack(fill=tk.BOTH, expand=True)

        # Create instruction text
        instructionText = ttk.Label(
            popupFrame,
            text="Enter stand name:",
            foreground="Black",
            background="#007994",
            font=("Arial", 20),
        )
        instructionText.grid(row=0, column=0, sticky="W")

        # Create stand entry
        standEntry = ttk.Entry(popupFrame, font=self._entryFont)
        standEntry.grid(row=1, column=0, sticky="W", padx=5)
        standEntry.bind(
            "<Return>",
            lambda event,
            i=index,
            entryField=standEntry,
            body=popup,
            frame=popupFrame: self.addUpStandEntry(i, entryField, body, frame),
        )

        # Create enter button
        enterButton = ttk.Button(
            popupFrame,
            text="Add",
            command=lambda i=index,
            entryField=standEntry,
            body=popup,
            frame=popupFrame: self.addUpStandEntry(i, entryField, body, frame),
        )
        enterButton.grid(row=2, column=0, sticky="W", padx=5, pady=5)

        # Check to see if the popup has been destroyed
        self.checkPopup(popup)

    # Checks to see if the popup has been destroyed so it can reactivate the buttons
    def checkPopup(self, popup):
        # Check to see if popup exists and is an object
        if popup and not popup.winfo_exists():
            # Turns all the buttons back on
            self.enableScheduleButtons()
            popup = None

        # Re-check
        self._root.after(500, lambda: self.checkPopup(popup))

    # Add a stand entry field
    def addUpStandEntry(self, index, standEntry, body, frame):
        # If the stand entry is not a duplicate and is less than two characters,
        # Add the stand
        alreadyExists = (
            standEntry.get() in self._timelyDownStandWidgets
            or standEntry.get() in self._upStandWidgets
        )
        if not alreadyExists and len(standEntry.get()) <= 2:
            self._upStands.insert(index + 1, standEntry.get())
            body.destroy()
            self.updateUpStandEntries()
            self.enableScheduleButtons()
        # Otherwise display an error message
        else:
            error = ttk.Label(
                frame,
                text="Error, either duplicate\nor more than 2 characters",
                foreground="#A50000",
                background="#007994",
                font=("Arial", 15),
            )
            error.grid(row=standEntry.grid_info()["row"] + 2, column=0)

    # Remove a stand entry field
    def removeUpStandEntry(self, index):
        # Pop out the stand from the up stands list and refresh the entries
        self._upStands.pop(index)
        self.updateUpStandEntries()

    # Remove all up stand entries
    def removeAllUpStands(self):
        self._upStands = []
        self.updateUpStandEntries()

    # Disables the buttons for the scheduler while something else is going on
    def disableScheduleButtons(self):
        for button in self._scheduleButtonsToMoveDown:
            button[0].config(state=tk.DISABLED)
        self._defaultUpStandButton.config(state=tk.DISABLED)
        self._addUpStandButton.config(state=tk.DISABLED)
        self._removeAllUpStandButton.config(state=tk.DISABLED)
        for value in self._upStandWidgets.values():
            value[2].config(state=tk.DISABLED)
            value[3].config(state=tk.DISABLED)
        for button in self._timelyDownStandButtons:
            button[0].config(state=tk.DISABLED)
        for value in self._timelyDownStandWidgets.values():
            value[2].config(state=tk.DISABLED)
            value[3].config(state=tk.DISABLED)

    # Turns all the buttons back on when they no longer have to be disabled
    def enableScheduleButtons(self):
        for button in self._scheduleButtonsToMoveDown:
            button[0].config(state=tk.NORMAL)
        self._defaultUpStandButton.config(state=tk.NORMAL)
        self._addUpStandButton.config(state=tk.NORMAL)
        self._removeAllUpStandButton.config(state=tk.NORMAL)
        for value in self._upStandWidgets.values():
            value[2].config(state=tk.NORMAL)
            value[3].config(state=tk.NORMAL)
        for button in self._timelyDownStandButtons:
            button[0].config(state=tk.NORMAL)
        for value in self._timelyDownStandWidgets.values():
            value[2].config(state=tk.NORMAL)
            value[3].config(state=tk.NORMAL)

    # Place a button (technically works with any widget) to the side of another widget
    @staticmethod
    def placeButtonToSide(button, widget, padx, pady):
        button.place(
            x=widget.winfo_x() + widget.winfo_width() + padx, y=widget.winfo_y() + pady
        )


if __name__ == "__main__":
    App()

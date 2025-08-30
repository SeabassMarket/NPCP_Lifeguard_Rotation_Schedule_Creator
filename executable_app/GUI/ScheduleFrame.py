# Import libraries
import tkinter as tk
from tkinter import ttk
from .EventFrame import EventFrame
from ..InfoManagers.StaticAppInfo import StaticAppInfo
from ..InfoManagers.Time import Time

"""This class serves more for organization. It will consist of a frame,
with a canvas inside. Attached to this canvas will be a scroll bar.
Finally, inside of the canvas there will be multiple frames, each
holding a different type of stand to input. These frames will be
"StandFrames" because they will all be very similar, so it's convenient
to just turn them into a class. At the bottom is just some buttons to
submit information, view information, FAQs, or go back home"""


class ScheduleFrame:
    # Create frame just for canvas and scroll bar
    def __init__(self, root, motherFrame, homeScreen, staticAppInfo):
        # Set instance variable from variables
        self._root = root
        self._motherFrame = motherFrame
        self._homeFrame = homeScreen
        self._eventDescriptor = "stand"
        self._frameDescriptor = "Schedule"

        # Create static app info object
        if isinstance(staticAppInfo, StaticAppInfo):
            self._staticAppInfo = staticAppInfo
        else:
            self._staticAppInfo = StaticAppInfo("ERROR")
            print("ERROR, STATIC APP INFO NOT INITIALIZED")

        # Create canvas frame
        self._scheduleCanvasFrame = tk.Frame(
            self._motherFrame,
            background=self._staticAppInfo.getColor(self._frameDescriptor),
        )
        self._scheduleCanvasFrame.place(relwidth=1, relheight=1)

        # Create canvas and scrollbar in canvas frame
        self._scheduleCanvas = tk.Canvas(
            self._scheduleCanvasFrame,
            background=self._staticAppInfo.getColor(self._frameDescriptor),
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
        self._scheduleFrame = tk.Frame(
            self._scheduleCanvas,
            background=self._staticAppInfo.getColor(self._frameDescriptor),
        )

        # Place schedule frame in window
        self._scheduleCanvas.create_window(
            (0, 0), window=self._scheduleFrame, anchor="nw"
        )

        """THIS MARKS THE END OF CANVAS CREATION AND BEGINNING OF FRAME CREATION"""

        # Create bottom buttons
        # Frame
        bottomFrame = tk.Frame(
            self._scheduleFrame,
            background=self._staticAppInfo.getColor(self._frameDescriptor),
        )
        # Back button
        self._backButton = ttk.Button(
            bottomFrame, text="Back Home", command=self.backHome
        )
        self._staticAppInfo.appendButtonToDisable(
            self._backButton
        )  # Append to buttons to disable
        # Question button
        self._scheduleQuestionCanvas = tk.Canvas()
        self._questionPopupFrame = tk.Frame()
        self._questionPopup = None
        self._questionButton = ttk.Button(
            bottomFrame, text="?", command=self.openScheduleQuestionPopup
        )
        self._staticAppInfo.appendButtonToDisable(
            self._questionButton
        )  # Append to buttons to disable
        # View button
        self._scheduleViewCanvas = tk.Canvas()
        self._viewPopupFrame = tk.Frame()
        self._viewPopup = None
        self._viewButton = ttk.Button(bottomFrame, text="View", command=self.viewPopup)
        self._staticAppInfo.appendButtonToDisable(
            self._viewButton
        )  # Append to buttons to disable
        # Submit button
        self._submitButton = ttk.Button(
            bottomFrame, text="Submit", command=self.submitSchedule
        )
        self._staticAppInfo.appendButtonToDisable(
            self._submitButton
        )  # Append to buttons to disable

        # Place schedule frame widgets and frames in window
        # Create stand frames list
        self._standFrames = []
        # Big schedule title at the top
        self._titleStandFrame = EventFrame(
            self._scheduleFrame,
            row=0,
            staticAppInfo=self._staticAppInfo,
            labelText="Schedule",
            frameDescriptor=self._frameDescriptor,
            titleFont="title",
        )
        # Up stand frame
        self._upStandFrame = EventFrame(
            self._scheduleFrame,
            row=1,
            root=root,
            staticAppInfo=self._staticAppInfo,
            titleFont="standard",
            entryFont="entry",
            errorFont="error",
            eventLabelFont="default",
            eventType="up",
            eventDescriptor=self._eventDescriptor,
            frameDescriptor=self._frameDescriptor,
            characterLimit=2,
            defaultList=["A", "B", "C", "E", "F", "G", "H", "I", "J", "K", "T", "S"],
        )
        self._standFrames.append(self._upStandFrame)
        # Down stand frame (title)
        self._downStandFrame = EventFrame(
            self._scheduleFrame,
            row=2,
            titleFont="standard",
            staticAppInfo=self._staticAppInfo,
            frameDescriptor=self._frameDescriptor,
            eventDescriptor=self._eventDescriptor,
            eventType="down",
        )
        # Timely down stand frame
        self._timelyDownStandFrame = EventFrame(
            self._scheduleFrame,
            row=3,
            staticAppInfo=self._staticAppInfo,
            root=root,
            titleFont="subtitle",
            entryFont="entry",
            errorFont="error",
            eventLabelFont="default",
            eventType="timely down",
            eventDescriptor=self._eventDescriptor,
            frameDescriptor=self._frameDescriptor,
            characterLimit=2,
            counter=True,
            defaultList=["SU", "DT", "ST", "CU"],
        )
        self._standFrames.append(self._timelyDownStandFrame)
        # Priority down stand frame
        self._priorityDownStandFrame = EventFrame(
            self._scheduleFrame,
            row=4,
            staticAppInfo=self._staticAppInfo,
            root=root,
            titleFont="subtitle",
            entryFont="entry",
            errorFont="error",
            eventLabelFont="default",
            eventType="priority down",
            timeEvent=False,
            eventDescriptor=self._eventDescriptor,
            frameDescriptor=self._frameDescriptor,
            characterLimit=2,
            counter=True,
            defaultList=["O", "X", "P"],
        )
        self._standFrames.append(self._priorityDownStandFrame)
        # Fill-in down stand frame
        self._fillInDownStandFrame = EventFrame(
            self._scheduleFrame,
            row=5,
            staticAppInfo=self._staticAppInfo,
            root=root,
            titleFont="subtitle",
            errorFont="error",
            entryFont="entry",
            eventLabelFont="default",
            eventType="fill-in down",
            defaultList=["W"],
            eventDescriptor=self._eventDescriptor,
            frameDescriptor=self._frameDescriptor,
            characterLimit=2,
            timeEvent=False,
        )
        self._standFrames.append(self._fillInDownStandFrame)

        # Place the bottom rows
        bottomRow = self._scheduleFrame.grid_size()[1]
        bottomFrame.grid(row=bottomRow, column=0, pady=5, sticky="nw")
        self._backButton.grid(row=0, column=0, padx=5, sticky="W")
        self._questionButton.grid(row=0, column=1, padx=5, sticky="W")
        self._viewButton.grid(row=0, column=2, padx=5, sticky="W")
        self._submitButton.grid(row=0, column=3, padx=5, sticky="W")

        """THIS MARKS THE END OF FRAME CREATION AND THE BEGINNING OF CANVAS INSTANTIATION"""

        # Bind entry and exit and create related variables
        self._staticAppInfo.addEnterAndExit(
            name="Schedule Canvas",
            threeValueList=[self._scheduleFrame, self._scheduleCanvas, self._root],
        )
        self._scheduleCanvas.bind("<Enter>", self._staticAppInfo.onEnter)
        # self._scheduleCanvas.bind("<Leave>", self.onLeave)

        # Instantiate scrolling
        self._staticAppInfo.instantiateScrolling()

    # Brings up information/question popup
    def openScheduleQuestionPopup(self):
        # Breaks out of function if the popup already exists
        if self._questionPopup and self._questionPopup.winfo_exists():
            return "ALREADY EXISTS"

        # Create toplevel popup
        self._questionPopup = tk.Toplevel()
        self._questionPopup.geometry("500x500+1050+450")
        self._questionPopup.title("FAQs/Tutorial")

        # Create canvas and scrollbar in popup
        self._scheduleQuestionCanvas = tk.Canvas(
            self._questionPopup,
            background=self._staticAppInfo.getColor(self._frameDescriptor),
        )
        scrollbar = ttk.Scrollbar(
            self._questionPopup,
            orient="vertical",
            command=self._scheduleQuestionCanvas.yview,
        )

        # Bind canvas and scrollbar together
        self._scheduleQuestionCanvas.configure(yscrollcommand=scrollbar.set)

        # Scrollbar and schedule question canvas pack
        scrollbar.pack(side="right", fill="y")
        self._scheduleQuestionCanvas.pack(side="left", fill="both", expand=True)

        # Create popup frame in canvas
        self._questionPopupFrame = tk.Frame(
            self._scheduleQuestionCanvas,
            background=self._staticAppInfo.getColor(self._frameDescriptor),
        )

        # Place popup frame in window
        self._scheduleQuestionCanvas.create_window(
            (0, 0), window=self._questionPopupFrame, anchor="nw"
        )

        """HERE MARKS THE START OF THE TEXT IN THE POPUP"""

        # Create label for format information
        formatLabel = ttk.Label(
            self._questionPopupFrame,
            text="How to enter/format information:",
            foreground=self._staticAppInfo.getColor("Default"),
            background=self._staticAppInfo.getColor(self._frameDescriptor),
            font=self._staticAppInfo.getFont("Default"),
        )
        formatLabel.grid(row=0, column=0, sticky="NW")

        # Create label for format example
        formatExample = ttk.Label(
            self._questionPopupFrame,
            text='"##:## **, ##:## **, #", example: "09:00 AM, 09:00 PM, 1"',
            foreground=self._staticAppInfo.getColor("Subtext"),
            background=self._staticAppInfo.getColor(self._frameDescriptor),
            font=self._staticAppInfo.getFont("SmallDefault"),
        )
        formatExample.grid(row=1, column=0, sticky="NW")

        # Create label for format explanation
        formatExplanation = ttk.Label(
            self._questionPopupFrame,
            text="-->This will set the time from 9:00AM to 9:00PM\n"
            "It will also make it so that there are 1 instance of\n"
            "that stand at the specific given time (at once)\n"
            "Make sure when entering times that the time on the\n"
            "left is the start time and the time on the right is the\n"
            "end time. Otherwise an error message will be\n"
            "displayed if the end time is before the start time.\n"
            "*NOTE* The second time itself is excluded, so\n"
            "9:00AM to 9:00PM means the stand closes at\n"
            "9:00PM. This means that if you want to make a stand\n"
            "last for only one rotation, you need to set the times to\n"
            "something like 2:00PM and 2:20PM.",
            foreground=self._staticAppInfo.getColor("Subtext"),
            background=self._staticAppInfo.getColor(self._frameDescriptor),
            font=self._staticAppInfo.getFont("SmallDefault"),
            anchor="w",
        )
        formatExplanation.grid(row=2, column=0, sticky="NW", padx=5)

        # Create the first invisible spacer
        invisibleSpacer1 = ttk.Label(
            self._questionPopupFrame,
            text="",
            background=self._staticAppInfo.getColor(self._frameDescriptor),
        )
        invisibleSpacer1.grid(row=3, column=0, pady=5, padx=5)

        # Create label for the subtract button label
        subtractButtonLabel = ttk.Label(
            self._questionPopupFrame,
            text='What the "-" buttons do:',
            foreground=self._staticAppInfo.getColor("Default"),
            background=self._staticAppInfo.getColor(self._frameDescriptor),
            font=self._staticAppInfo.getFont("Default"),
        )
        subtractButtonLabel.grid(row=4, column=0, sticky="NW", padx=5)

        # Create label for the subtract button explanation
        subtractButtonExplanation = ttk.Label(
            self._questionPopupFrame,
            text='-->The one at the top next to the "Set Default\n'
            '______ Stands" button removes all current stand\n'
            "entry fields (be careful!). The ones next to each\n"
            "of the entry fields just removes the one it's next to.",
            foreground=self._staticAppInfo.getColor("Subtext"),
            background=self._staticAppInfo.getColor(self._frameDescriptor),
            font=self._staticAppInfo.getFont("SmallDefault"),
            anchor="w",
        )
        subtractButtonExplanation.grid(row=5, column=0, sticky="NW", padx=5)

        # Create the second invisible spacer
        invisibleSpacer2 = ttk.Label(
            self._questionPopupFrame,
            text="",
            background=self._staticAppInfo.getColor(self._frameDescriptor),
        )
        invisibleSpacer2.grid(row=6, column=0, pady=5, padx=5)

        # Create label for the add button label
        addButtonLabel = ttk.Label(
            self._questionPopupFrame,
            text='What the "+" buttons do:',
            foreground=self._staticAppInfo.getColor("Default"),
            background=self._staticAppInfo.getColor(self._frameDescriptor),
            font=self._staticAppInfo.getFont("Default"),
        )
        addButtonLabel.grid(row=7, column=0, sticky="NW", padx=5)

        # Create label for the add button explanation
        addButtonExplanation = ttk.Label(
            self._questionPopupFrame,
            text='-->The one at the top next to the "Set Default\n'
            'Up Stands" brings up a popup to add a stand entry\n'
            "field. Once the user presses the add button on the\n"
            "popup, the entry will be added to the top of the\n"
            "entries. The ones next to the entry fields will add\n"
            "the stand entry in the next one.\n"
            "*Note: the order won't affect calculations",
            foreground=self._staticAppInfo.getColor("Subtext"),
            background=self._staticAppInfo.getColor(self._frameDescriptor),
            font=self._staticAppInfo.getFont("SmallDefault"),
            anchor="w",
        )
        addButtonExplanation.grid(row=8, column=0, sticky="NW", padx=5)

        # Create the third invisible spacer
        invisibleSpacer3 = ttk.Label(
            self._questionPopupFrame,
            text="",
            background=self._staticAppInfo.getColor(self._frameDescriptor),
        )
        invisibleSpacer3.grid(row=9, column=0, pady=5)

        # Create label for difference between up stands and down stands
        standDifferenceLabel = ttk.Label(
            self._questionPopupFrame,
            text="What the stands mean:",
            foreground=self._staticAppInfo.getColor("Default"),
            background=self._staticAppInfo.getColor(self._frameDescriptor),
            font=self._staticAppInfo.getFont("Default"),
        )
        standDifferenceLabel.grid(row=10, column=0, sticky="NW", padx=5)

        # Create label for difference between up stands and down stands explanation
        standDifferenceExplanation = ttk.Label(
            self._questionPopupFrame,
            text="-->The different types of stands signify the\n"
            "difference between up and down stand in\n"
            "calculations. They are as follows:\n"
            "\n"
            "1. The up stands are normal stands like A, B, T,\n"
            'S, stands that are "ups."\n'
            "\n"
            "2. The timely down stands are down stands that are\n"
            "only at certain times in the day. For example,\n"
            "these are things like DT (DiveTest), ST (Swim\n"
            "Test), CU (Cleanup), and SU (Setup).\n"
            "\n"
            "3. The priority down stands are significant\n"
            "down stands that should be prioritized over\n"
            "a simple down like W. These are, in order of\n"
            "significance (yes order affects calculations):\n"
            "O, X, P\n"
            "\n"
            "4. Fill-in down stands are down stands that are\n"
            "supplementary. They fill in all the rest of the\n"
            "spots that aren't needed at the moment. This is\n"
            "mostly just W. This type does not need a time slot\n"
            "\n"
            "IMPORTANT NOTE: If you want to add a stand that\n"
            "you feel fits one of these categories, feel free to\n"
            "add it!",
            foreground=self._staticAppInfo.getColor("Subtext"),
            background=self._staticAppInfo.getColor(self._frameDescriptor),
            font=self._staticAppInfo.getFont("SmallDefault"),
            anchor="w",
        )
        standDifferenceExplanation.grid(row=11, column=0, sticky="NW", padx=5)

        # Create the fourth invisible spacer
        invisibleSpacer4 = ttk.Label(
            self._questionPopupFrame,
            text="",
            background=self._staticAppInfo.getColor(self._frameDescriptor),
        )
        invisibleSpacer4.grid(row=12, column=0, pady=5)

        # Create contact info label
        contactInfoLabel = ttk.Label(
            self._questionPopupFrame,
            text="Submit and View Buttons",
            foreground=self._staticAppInfo.getColor("Default"),
            background=self._staticAppInfo.getColor(self._frameDescriptor),
            font=self._staticAppInfo.getFont("Default"),
        )
        contactInfoLabel.grid(row=13, column=0, sticky="NW", padx=5)

        # Contact info text
        contactInfoText = ttk.Label(
            self._questionPopupFrame,
            text="-->The submit button submits the data in the\n"
            "current fields. However, make sure there are no\n"
            "errors. If there are, very obvious error messages\n"
            "will appear next to the fields with errors. The view\n"
            "button allows you to see what is currently saved.\n"
            "If you exit the schedule page what you see in the\n"
            "view section is what will be used in the lifeguard\n"
            "calculations when you open the calculations page.\n"
            "Remember, you need to fill out the lifeguard page\n"
            "as well to calculate.",
            foreground=self._staticAppInfo.getColor("Subtext"),
            background=self._staticAppInfo.getColor(self._frameDescriptor),
            font=self._staticAppInfo.getFont("SmallDefault"),
            anchor="w",
        )
        contactInfoText.grid(row=14, column=0, sticky="NW", padx=5)

        # Create the fifth invisible spacer
        invisibleSpacer5 = ttk.Label(
            self._questionPopupFrame,
            text="",
            background=self._staticAppInfo.getColor(self._frameDescriptor),
        )
        invisibleSpacer5.grid(row=15, column=0, pady=5)

        # Create contact info label
        brokenDefaultLabel = ttk.Label(
            self._questionPopupFrame,
            text='The Default Button is "Broken"',
            foreground=self._staticAppInfo.getColor("Default"),
            background=self._staticAppInfo.getColor(self._frameDescriptor),
            font=self._staticAppInfo.getFont("Default"),
        )
        brokenDefaultLabel.grid(row=16, column=0, sticky="NW", padx=5)

        # Contact info text
        brokenDefaultText = ttk.Label(
            self._questionPopupFrame,
            text="-->if the default button mysteriously seems\n"
            "to stop working, chances are you are simply\n"
            "creating an error. If one of the default values\n"
            "is found in another stand set, then it won't\n"
            "generate because you can't have duplicate stands.\n"
            'For example, if you add "T" to fill-in stands,\n'
            "then the default button for up stands will not\n"
            'generate because the "T" stand is already taken\n'
            "by the one you added in fill-in. To fix this, simply\n"
            "remove the stand and rename it. Here is a list of the\n"
            "default stands currently coded in:\n"
            "Up: A, B, C, E, F, G, H, I, J, K, T, S\n"
            "Timely Down: SU, DT, ST, CU\n"
            "Priority Down: O, X, P\n"
            "Fill-In: W",
            foreground=self._staticAppInfo.getColor("Subtext"),
            background=self._staticAppInfo.getColor(self._frameDescriptor),
            font=self._staticAppInfo.getFont("SmallDefault"),
            anchor="w",
        )
        brokenDefaultText.grid(row=17, column=0, sticky="NW", padx=5)

        # Create the sixth invisible spacer
        invisibleSpacer5 = ttk.Label(
            self._questionPopupFrame,
            text="",
            background=self._staticAppInfo.getColor(self._frameDescriptor),
        )
        invisibleSpacer5.grid(row=18, column=0, pady=5)

        # Create contact info label
        contactInfoLabel = ttk.Label(
            self._questionPopupFrame,
            text="Contact Information",
            foreground=self._staticAppInfo.getColor("Default"),
            background=self._staticAppInfo.getColor(self._frameDescriptor),
            font=self._staticAppInfo.getFont("Default"),
        )
        contactInfoLabel.grid(row=19, column=0, sticky="NW", padx=5)

        # Contact info text
        contactInfoText = ttk.Label(
            self._questionPopupFrame,
            text="-->If you have any further questions or \n"
            "suggestions for improvement, please contact the\n"
            "head developer, Sebastian Mercado, via the\n"
            "following mediums:\n"
            "Email: simercado07@gmail.com\n"
            "Phone Number: 908-200-5331",
            foreground=self._staticAppInfo.getColor("Subtext"),
            background=self._staticAppInfo.getColor(self._frameDescriptor),
            font=self._staticAppInfo.getFont("SmallDefault"),
            anchor="w",
        )
        contactInfoText.grid(row=20, column=0, sticky="NW", padx=5)

        """HERE MARKS THE END OF """

        # Set entry and exit data
        self._staticAppInfo.addEnterAndExit(
            name="Schedule Question Canvas",
            threeValueList=[
                self._questionPopupFrame,
                self._scheduleQuestionCanvas,
                self._questionPopup,
            ],
        )
        self._scheduleQuestionCanvas.bind("<Enter>", self._staticAppInfo.onEnter)
        # self._scheduleQuestionCanvas.bind("<Leave>", self.onLeave)

        # Instantiate scrolling with canvas
        self._staticAppInfo.instantiateScrolling()

    # Submit and save data, command for submit button
    def submitSchedule(self):
        standData = dict()
        for standFrame in self._standFrames:
            standData[standFrame.getEventType()] = standFrame.submitData()
        errors = False
        for key in standData:
            if standData[key] == "ERROR":
                errors = True
        if not errors:
            self._staticAppInfo.setEventDataSpecific(standData, self._eventDescriptor)

    # Display the current information in the stands data in the static app info
    def viewPopup(self):
        # Breaks out of function if the popup already exists
        if self._viewPopup and self._viewPopup.winfo_exists():
            return "ALREADY EXISTS"

        # Create toplevel popup
        self._viewPopup = tk.Toplevel()
        self._viewPopup.geometry("800x1000+900+300")
        self._viewPopup.title("Schedule View")

        # Create canvas and scrollbar in popup
        self._scheduleViewCanvas = tk.Canvas(
            self._viewPopup,
            background=self._staticAppInfo.getColor(self._frameDescriptor),
        )
        scrollbar = ttk.Scrollbar(
            self._viewPopup, orient="vertical", command=self._scheduleViewCanvas.yview
        )

        # Bind canvas and scrollbar together
        self._scheduleViewCanvas.configure(yscrollcommand=scrollbar.set)

        # Scrollbar and schedule question canvas pack
        scrollbar.pack(side="right", fill="y")
        self._scheduleViewCanvas.pack(side="left", fill="both", expand=True)

        # Create popup frame in canvas
        self._viewPopupFrame = tk.Frame(
            self._scheduleViewCanvas,
            background=self._staticAppInfo.getColor(self._frameDescriptor),
        )

        # Place popup frame in window
        self._scheduleViewCanvas.create_window(
            (0, 0), window=self._viewPopupFrame, anchor="nw"
        )

        """HERE MARKS THE END OF INITIAL CANVAS CREATION AND NOW THE ACTUAL VISUAL WIDGETS"""

        # Create the top frame:
        # Frame to house the text
        topFrame = tk.Frame(
            self._viewPopupFrame,
            background=self._staticAppInfo.getColor(self._frameDescriptor),
        )
        topFrame.pack(side="top", fill="x", anchor="w")
        # Big title at the top
        titleLabel = ttk.Label(
            topFrame,
            text="Schedule:",
            foreground=self._staticAppInfo.getColor("default"),
            background=self._staticAppInfo.getColor(self._frameDescriptor),
            font=self._staticAppInfo.getFont("standard"),
            anchor="w",
        )
        titleLabel.grid(row=0, column=0, sticky="NW", padx=5)
        # Explanation of page
        pageExplanation = ttk.Label(
            topFrame,
            text="-->This window displays the current schedule\n"
            "information saved. If nothing is displayed you\n"
            "have not saved anything yet.",
            foreground=self._staticAppInfo.getColor("subtext"),
            background=self._staticAppInfo.getColor(self._frameDescriptor),
            font=self._staticAppInfo.getFont("default"),
            anchor="w",
        )
        pageExplanation.grid(row=1, column=0, sticky="NW", padx=5)

        # Create a bottom frame to mother the whole schedule view (besides top of course)
        bottomFrame = tk.Frame(
            self._viewPopupFrame,
            background=self._staticAppInfo.getColor(self._frameDescriptor),
        )
        bottomFrame.pack(side="top", fill="x", anchor="w", pady=10)

        # Seperate stand data dictionary into different lists
        eventTypeLabels = []
        standsInfo = []
        invisibleSpacers = []
        standData = self._staticAppInfo.getEventDataSpecific(self._eventDescriptor)
        for key in standData:
            eventTypeLabels.append(
                ttk.Label(
                    bottomFrame,
                    text=self._staticAppInfo.capitalizeTitle(key),
                    foreground=self._staticAppInfo.getColor("default"),
                    background=self._staticAppInfo.getColor(self._frameDescriptor),
                    font=self._staticAppInfo.getFont("default"),
                    anchor="w",
                )
            )
            invisibleSpacers.append(
                ttk.Label(
                    bottomFrame,
                    text="",
                    background=self._staticAppInfo.getColor(self._frameDescriptor),
                )
            )
            # Take the info for each stand and convert it into a string
            # Make a label out of that string, and then take all the labels for this one type of
            # stand and put it into a list. Append this list to the stands info list
            standInfo = []
            for stand in standData[key]:
                if isinstance(standData[key][stand][1], Time):
                    secondTime = standData[key][stand][1].get12Time()
                else:
                    secondTime = "end of day"
                message = (
                    "Stand "
                    + stand
                    + ": "
                    + standData[key][stand][0].get12Time()
                    + " to "
                    + secondTime
                )
                if len(standData[key][stand]) == 3:
                    message += " - " + standData[key][stand][2] + " at a time"
                standInfo.append(
                    ttk.Label(
                        bottomFrame,
                        text=message,
                        foreground=self._staticAppInfo.getColor("subtext"),
                        background=self._staticAppInfo.getColor(self._frameDescriptor),
                        font=self._staticAppInfo.getFont("smallDefault"),
                        anchor="w",
                    )
                )
            standsInfo.append(standInfo)

        # Place all the objects
        for i in range(len(eventTypeLabels)):
            eventTypeLabels[i].pack(side="top", fill="x", anchor="w", padx=5)
            for label in standsInfo[i]:
                label.pack(side="top", fill="x", anchor="w", padx=5, pady=2)
            invisibleSpacers[i].pack(side="top", fill="x", anchor="w")

        """HERE MARKS THE END OF THE ACTUAL VISUAL WIDGETS AND THE FINAL INSTANTIATION OF THE CANVAS"""

        # Set entry and exit data
        self._staticAppInfo.addEnterAndExit(
            name="Schedule View Canvas",
            threeValueList=[
                self._viewPopupFrame,
                self._scheduleViewCanvas,
                self._viewPopup,
            ],
        )
        self._scheduleViewCanvas.bind("<Enter>", self._staticAppInfo.onEnter)
        # self._scheduleViewCanvas.bind("<Leave>", self.onLeave)

        # Instantiate scrolling with canvas
        self._staticAppInfo.instantiateScrolling()

    # Return schedule canvas frame (or overall parent)
    def getScheduleFrame(self):
        return self._scheduleCanvasFrame

    # Returns to home page
    def backHome(self):
        self._homeFrame.tkraise()

    """
    #Keep track of when the mouse has left a widget
    def onLeave(self, event):
        widget = event.widget
    """

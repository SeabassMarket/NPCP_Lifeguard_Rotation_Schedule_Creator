#import libraries
import tkinter as tk
from tkinter import ttk
from EventFrame import EventFrame
from StaticAppInfo import StaticAppInfo
from Time import Time

'''This class is for organization. Only one of these objects will be made.
This effectively acts as the lifeguard page of the app. This will be
similar to the schedule frame, but instead of different types of lifeguard
frames, there will only be one lifeguard frame. This is because all
lifeguards are considered the same. Maybe in the future, add an option
to generate the list automatically by using internet requests to sling.
Also, maybe in the future add an option for gender so that the schedule
can make sure both the girls and boys bathroom gets cleaned.'''
class LifeguardFrame:
    
    #Create the lifeguard canvas and frame
    def __init__(self, root, motherFrame, homeScreen, staticAppInfo):

        # Set instance variable from variables
        self._root = root
        self._motherFrame = motherFrame
        self._homeFrame = homeScreen
        self._frameDescriptor = "lifeguard"

        # Create static app info object
        if isinstance(staticAppInfo, StaticAppInfo):
            self._staticAppInfo = staticAppInfo
        else:
            self._staticAppInfo = StaticAppInfo("ERROR")
            print("ERROR, STATIC APP INFO NOT INITIALIZED")

        #Create variables to store lifeguard related data and widgets
        self._lifeguards = []
        self._lifeguardWidgets = dict()
        self._lifeguardEntries = dict()

        # Create canvas frame
        self._lifeguardCanvasFrame = tk.Frame(self._motherFrame)
        self._lifeguardCanvasFrame.place(relwidth=1, relheight=1)

        # Create canvas and scrollbar in canvas frame
        self._lifeguardCanvas = tk.Canvas(self._lifeguardCanvasFrame, background=self._staticAppInfo.getColor(self._frameDescriptor))
        scrollbar = ttk.Scrollbar(self._lifeguardCanvasFrame,
                                  orient="vertical",
                                  command=self._lifeguardCanvas.yview)

        # Bind canvas and scrollbar together
        self._lifeguardCanvas.configure(yscrollcommand=scrollbar.set)

        # Scrollbar and lifeguard pack
        scrollbar.pack(side="right", fill="y")
        self._lifeguardCanvas.pack(side="left", fill="both", expand=True)

        # Create lifeguard frame in canvas
        self._lifeguardFrame = tk.Frame(self._lifeguardCanvas, background=self._staticAppInfo.getColor(self._frameDescriptor))

        # Place lifeguard frame in window
        self._lifeguardCanvas.create_window((0, 0), window=self._lifeguardFrame, anchor="nw")

        '''THIS MARKS THE END OF CANVAS CREATION AND BEGINNING OF FRAME CREATION'''

        #Title
        self._lifeguardTitle = ttk.Label(self._lifeguardFrame,
                                         text="Lifeguards",
                                         foreground=self._staticAppInfo.getColor("Default"),
                                         background=self._staticAppInfo.getColor(self._frameDescriptor),
                                         font=self._staticAppInfo.getFont("title"))
        self._lifeguardTitle.grid(row=0, column=0, padx=5, sticky = "NW")

        '''
        Create the lifeguard frames using the event frame template
        '''

        #Create and place the middle frame that will house all the lifeguard event frames
        self._middleFrame = tk.Frame(self._lifeguardFrame, background=self._staticAppInfo.getColor(self._frameDescriptor))
        self._middleFrame.grid(row = 1, column= 0, sticky = "NW")

        #Create a list for the lifeguard frames
        self._lifeguardFrames = []

        #Create the lifeguard event frame (there is only one type)
        #First create a real fast default list
        defaultLifeguards = []
        for i in range(1, 16):
            defaultLifeguards.append(str(i))
        #Then make the lifeguard event frame
        self._lifeguardEventFrame = EventFrame(self._middleFrame,
                                        row = 1,
                                        root = root,
                                        staticAppInfo=self._staticAppInfo,
                                        titleFont="standard",
                                        entryFont="entry",
                                        errorFont="error",
                                        eventLabelFont="default",
                                        eventType=self._frameDescriptor,
                                        eventDescriptor=self._frameDescriptor,
                                        frameDescriptor=self._frameDescriptor,
                                        characterLimit=20,
                                        defaultList=defaultLifeguards)
        self._lifeguardFrames.append(self._lifeguardEventFrame)

        '''THIS MARKS THE END OF THE LIFEGUARD EVENT FRAMES AND THE BEGINNING OF THE BOTTOM FRAME'''

        #Bottom buttons
        #Bottom frame
        bottomFrame = tk.Frame(self._lifeguardFrame, background=self._staticAppInfo.getColor(self._frameDescriptor))
        # Back button
        self._backButton = ttk.Button(bottomFrame,
                                      text="Back Home",
                                      command=self.backHome)
        self._staticAppInfo.appendButtonToDisable(self._backButton)  # Append to buttons to disable
        # Question button
        self._scheduleQuestionCanvas = tk.Canvas()
        self._questionPopupFrame = tk.Frame()
        self._questionPopup = None
        self._questionButton = ttk.Button(bottomFrame,
                                      text="?",
                                      command=self.openLifeguardQuestionPopup)
        self._staticAppInfo.appendButtonToDisable(self._questionButton)  # Append to buttons to disable
        # View popup stuff button
        self._scheduleViewCanvas = tk.Canvas()
        self._viewPopupFrame = tk.Frame()
        self._viewPopup = None
        self._viewButton = ttk.Button(bottomFrame,
                                      text="View",
                                      command=self.viewPopup)
        self._staticAppInfo.appendButtonToDisable(self._viewButton)  # Append to buttons to disable
        #Submit button
        self._submitButton = ttk.Button(bottomFrame,
                                      text="Submit",
                                      command=self.submitLifeguards)
        self._staticAppInfo.appendButtonToDisable(self._submitButton)  # Append to buttons to disable

        #Place the bottom rows
        bottomRow = self._lifeguardFrame.grid_size()[1]
        bottomFrame.grid(row = bottomRow, column = 0, pady=5, sticky = "nw")
        self._backButton.grid(row = 0, column = 0, padx=5, sticky = "W")
        self._questionButton.grid(row = 0, column = 1, padx=5, sticky = "W")
        self._viewButton.grid(row = 0, column = 2, padx=5, sticky = "W")
        self._submitButton.grid(row = 0, column = 3, padx=5, sticky = "W")

        '''THIS MARKS THE END OF FRAME CREATION AND THE BEGINNING OF CANVAS INSTANTIATION'''

        #Bind entry and exit and create related variables
        self._staticAppInfo.addEnterAndExit(name="Lifeguard Canvas",
                                            threeValueList=[self._lifeguardFrame, self._lifeguardCanvas, self._root])
        self._lifeguardCanvas.bind("<Enter>", self._staticAppInfo.onEnter)

        #Instantiate scrolling
        self._staticAppInfo.instantiateScrolling()

    #Return lifeguard canvas frame (or overall parent)
    def getLifeguardFrame(self):
        return self._lifeguardCanvasFrame

    #Returns to home page
    def backHome(self):
        self._homeFrame.tkraise()

    #Submits the lifeguard entries
    def submitLifeguards(self):
        lifeguardData = dict()
        for lifeguardFrame in self._lifeguardFrames:
            lifeguardData[lifeguardFrame.getEventType()] = lifeguardFrame.submitData()
        errors = False
        for key in lifeguardData:
            if lifeguardData[key] == "ERROR":
                errors = True
        if not errors:
            self._staticAppInfo.setEventDataSpecific(lifeguardData, self._frameDescriptor)

    #Display the current information in the lifeguard data in the static app info
    def viewPopup(self):

        #Breaks out of function if the popup already exists
        if self._viewPopup and self._viewPopup.winfo_exists():
            return "ALREADY EXISTS"

        #Create toplevel popup
        self._viewPopup = tk.Toplevel()
        self._viewPopup.geometry("800x1000+900+300")
        self._viewPopup.title("Schedule View")

        #Create canvas and scrollbar in popup
        self._scheduleViewCanvas = tk.Canvas(self._viewPopup,
                                                 background=self._staticAppInfo.getColor(self._frameDescriptor))
        scrollbar = ttk.Scrollbar(self._viewPopup,
                                  orient="vertical",
                                  command=self._scheduleViewCanvas.yview)

        #Bind canvas and scrollbar together
        self._scheduleViewCanvas.configure(yscrollcommand=scrollbar.set)

        #Scrollbar and schedule question canvas pack
        scrollbar.pack(side="right", fill="y")
        self._scheduleViewCanvas.pack(side="left", fill="both", expand=True)

        #Create popup frame in canvas
        self._viewPopupFrame = tk.Frame(self._scheduleViewCanvas,
                                            background=self._staticAppInfo.getColor(self._frameDescriptor))

        #Place popup frame in window
        self._scheduleViewCanvas.create_window((0, 0), window=self._viewPopupFrame, anchor ="nw")

        '''HERE MARKS THE END OF INITIAL CANVAS CREATION AND NOW THE ACTUAL VISUAL WIDGETS'''

        #Create the top frame:
        #Frame to house the text
        topFrame = tk.Frame(self._viewPopupFrame, background=self._staticAppInfo.getColor(self._frameDescriptor))
        topFrame.pack(side="top", fill = "x", anchor = "w")
        #Big title at the top
        titleLabel = ttk.Label(topFrame,
                               text="Schedule:",
                               foreground=self._staticAppInfo.getColor("default"),
                               background=self._staticAppInfo.getColor(self._frameDescriptor),
                               font=self._staticAppInfo.getFont("standard"),
                               anchor="w")
        titleLabel.grid(row=0, column=0, sticky="NW", padx = 5)
        #Explanation of page
        pageExplanation = ttk.Label(topFrame,
                                    text="-->This window displays the current schedule\n"
                                         "information saved. If nothing is displayed you\n"
                                         "have not saved anything yet.",
                                    foreground=self._staticAppInfo.getColor("subtext"),
                                    background=self._staticAppInfo.getColor(self._frameDescriptor),
                                    font=self._staticAppInfo.getFont("default"),
                                    anchor="w")
        pageExplanation.grid(row=1, column=0, sticky="NW", padx = 5)

        #Create a bottom frame to mother the whole schedule view (besides top of course)
        bottomFrame = tk.Frame(self._viewPopupFrame, background=self._staticAppInfo.getColor(self._frameDescriptor))
        bottomFrame.pack(side="top", fill = "x", anchor = "w", pady=10)

        #Seperate lifeguard data dictionary into different lists
        eventTypeLabels = []
        lifeguardsInfo = []
        invisibleSpacers = []
        lifeguardData = self._staticAppInfo.getEventDataSpecific(self._frameDescriptor)
        for key in lifeguardData:
            eventTypeLabels.append(ttk.Label(bottomFrame,
                                             text = self._staticAppInfo.capitalizeTitle(key + "s"),
                                             foreground=self._staticAppInfo.getColor("default"),
                                             background=self._staticAppInfo.getColor(self._frameDescriptor),
                                             font=self._staticAppInfo.getFont("default"),
                                             anchor="w"))
            invisibleSpacers.append(ttk.Label(bottomFrame,
                                              text = "",
                                              background=self._staticAppInfo.getColor(self._frameDescriptor)))
            #Take the info for each lifeguard and convert it into a string
            #Make a label out of that string, and then take all the labels for this one type of
            #lifeguard and put it into a list. Append this list to the lifeguards info list
            lifeguardInfo = []
            for lifeguard in lifeguardData[key]:
                if isinstance(lifeguardData[key][lifeguard][1], Time):
                    secondTime = lifeguardData[key][lifeguard][1].get12Time()
                else:
                    secondTime = "end of day"
                message = ("Stand " + lifeguard + ": " +
                           lifeguardData[key][lifeguard][0].get12Time() +
                           " to " +
                           secondTime)
                lifeguardInfo.append(ttk.Label(bottomFrame,
                                           text=message,
                                           foreground=self._staticAppInfo.getColor("subtext"),
                                           background=self._staticAppInfo.getColor(self._frameDescriptor),
                                           font=self._staticAppInfo.getFont("smallDefault"),
                                           anchor="w"))
            lifeguardsInfo.append(lifeguardInfo)

        #Place all the objects
        for i in range(len(eventTypeLabels)):
            eventTypeLabels[i].pack(side="top", fill = "x", anchor = "w", padx = 5)
            for label in lifeguardsInfo[i]:
                label.pack(side="top", fill="x", anchor="w", padx = 5, pady = 2)
            invisibleSpacers[i].pack(side="top", fill = "x", anchor = "w")

        '''HERE MARKS THE END OF THE ACTUAL VISUAL WIDGETS AND THE FINAL INSTANTIATION OF THE CANVAS'''

        #Set entry and exit data
        self._staticAppInfo.addEnterAndExit(name="Lifeguard View Canvas",
                                            threeValueList=[self._viewPopupFrame,
                                                 self._scheduleViewCanvas,
                                                 self._viewPopup])
        self._scheduleViewCanvas.bind("<Enter>", self._staticAppInfo.onEnter)
        #self._scheduleViewCanvas.bind("<Leave>", self.onLeave)

        #Instantiate scrolling with canvas
        self._staticAppInfo.instantiateScrolling()

    #Brings up information/question popup
    def openLifeguardQuestionPopup(self):

        #Breaks out of function if the popup already exists
        if self._questionPopup and self._questionPopup.winfo_exists():
            return "ALREADY EXISTS"

        #Create toplevel popup
        self._questionPopup = tk.Toplevel()
        self._questionPopup.geometry("500x500+1050+450")
        self._questionPopup.title("FAQs/Tutorial")

        #Create canvas and scrollbar in popup
        self._scheduleQuestionCanvas = tk.Canvas(self._questionPopup,
                                                 background=self._staticAppInfo.getColor(self._frameDescriptor))
        scrollbar = ttk.Scrollbar(self._questionPopup,
                                  orient="vertical",
                                  command=self._scheduleQuestionCanvas.yview)

        #Bind canvas and scrollbar together
        self._scheduleQuestionCanvas.configure(yscrollcommand=scrollbar.set)

        #Scrollbar and schedule question canvas pack
        scrollbar.pack(side="right", fill="y")
        self._scheduleQuestionCanvas.pack(side="left", fill="both", expand=True)

        #Create popup frame in canvas
        self._questionPopupFrame = tk.Frame(self._scheduleQuestionCanvas,
                                            background=self._staticAppInfo.getColor(self._frameDescriptor))

        #Place popup frame in window
        self._scheduleQuestionCanvas.create_window((0, 0), window=self._questionPopupFrame, anchor ="nw")

        '''HERE MARKS THE START OF THE TEXT IN THE POPUP'''

        #Create label for format information
        formatLabel = ttk.Label(self._questionPopupFrame,
                               text="How to enter/format information:",
                               foreground=self._staticAppInfo.getColor("Default"),
                               background=self._staticAppInfo.getColor(self._frameDescriptor),
                               font=self._staticAppInfo.getFont("Default"))
        formatLabel.grid(row=0, column=0, sticky="NW")

        #Create label for format example
        formatExample = ttk.Label(self._questionPopupFrame,
                                 text="\"##:## **, ##:## **\", example: \"09:00 AM, 09:00 PM\"",
                                 foreground=self._staticAppInfo.getColor("Subtext"),
                                 background=self._staticAppInfo.getColor(self._frameDescriptor),
                                 font=self._staticAppInfo.getFont("SmallDefault"))
        formatExample.grid(row=1, column=0, sticky="NW")

        #Create label for format explanation
        formatExplanation = ttk.Label(self._questionPopupFrame,
                                     text="-->This will set the time from 9:00AM to 9:00PM\n"
                                          "Make sure when entering times that the time on the\n"
                                          "left is the start time and the time on the right is\n"
                                          "the end time. Otherwise an error message will be\n"
                                          "displayed if the end time is before the start time.",
                                     foreground=self._staticAppInfo.getColor("Subtext"),
                                     background=self._staticAppInfo.getColor(self._frameDescriptor),
                                     font=self._staticAppInfo.getFont("SmallDefault"),
                                     anchor="w")
        formatExplanation.grid(row=2, column=0, sticky="NW", padx = 5)

        #Create the first invisible spacer
        invisibleSpacer1 = ttk.Label(self._questionPopupFrame,
                                     text="",
                                     background=self._staticAppInfo.getColor(self._frameDescriptor))
        invisibleSpacer1.grid(row=3, column=0, pady=5, padx = 5)

        #Create label for the subtract button label
        subtractButtonLabel = ttk.Label(self._questionPopupFrame,
                               text="What the \"-\" buttons do:",
                               foreground=self._staticAppInfo.getColor("Default"),
                               background=self._staticAppInfo.getColor(self._frameDescriptor),
                               font=self._staticAppInfo.getFont("Default"))
        subtractButtonLabel.grid(row=4, column=0, sticky="NW", padx = 5)

        #Create label for the subtract button explanation
        subtractButtonExplanation = ttk.Label(self._questionPopupFrame,
                                     text="-->The one at the top next to the \"Set Default\n"
                                          "______ Stands\" button removes all current stand\n"
                                          "entry fields (be careful!). The ones next to each\n"
                                          "of the entry fields just removes the one it's next to.",
                                     foreground=self._staticAppInfo.getColor("Subtext"),
                                     background=self._staticAppInfo.getColor(self._frameDescriptor),
                                     font=self._staticAppInfo.getFont("SmallDefault"),
                                     anchor="w")
        subtractButtonExplanation.grid(row=5, column=0, sticky="NW", padx = 5)

        #Create the second invisible spacer
        invisibleSpacer2 = ttk.Label(self._questionPopupFrame,
                                     text="",
                                     background=self._staticAppInfo.getColor(self._frameDescriptor))
        invisibleSpacer2.grid(row=6, column=0, pady=5, padx = 5)

        #Create label for the add button label
        addButtonLabel = ttk.Label(self._questionPopupFrame,
                               text="What the \"+\" buttons do:",
                               foreground=self._staticAppInfo.getColor("Default"),
                               background=self._staticAppInfo.getColor(self._frameDescriptor),
                               font=self._staticAppInfo.getFont("Default"))
        addButtonLabel.grid(row=7, column=0, sticky="NW", padx = 5)

        #Create label for the add button explanation
        addButtonExplanation = ttk.Label(self._questionPopupFrame,
                                     text="-->The one at the top next to the \"Set Default\n"
                                          "Up Stands\" brings up a popup to add a stand entry\n"
                                          "field. Once the user presses the add button on the\n"
                                          "popup, the entry will be added to the top of the\n"
                                          "entries. The ones next to the entry fields will add\n"
                                          "the stand entry in the next one.\n"
                                          "*Note: the order won't affect calculations",
                                     foreground=self._staticAppInfo.getColor("Subtext"),
                                     background=self._staticAppInfo.getColor(self._frameDescriptor),
                                     font=self._staticAppInfo.getFont("SmallDefault"),
                                     anchor="w")
        addButtonExplanation.grid(row=8, column=0, sticky="NW", padx = 5)

        #Create the third invisible spacer
        invisibleSpacer3 = ttk.Label(self._questionPopupFrame,
                                     text="",
                                     background=self._staticAppInfo.getColor(self._frameDescriptor))
        invisibleSpacer3.grid(row=9, column=0, pady=5)

        '''HERE MARKS THE END OF '''

        #Set entry and exit data
        self._staticAppInfo.addEnterAndExit(name="Lifeguard Question Canvas",
                                            threeValueList=[self._questionPopupFrame,
                                                     self._scheduleQuestionCanvas,
                                                     self._questionPopup])
        self._scheduleQuestionCanvas.bind("<Enter>", self._staticAppInfo.onEnter)
        #self._scheduleQuestionCanvas.bind("<Leave>", self.onLeave)

        #Instantiate scrolling with canvas
        self._staticAppInfo.instantiateScrolling()
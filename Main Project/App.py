#import libraries
import tkinter as tk
from tkinter import ttk
from tkinter import font
from ScheduleFrame import ScheduleFrame
from LifeguardFrame import LifeguardFrame
from StaticAppInfo import StaticAppInfo

#Mother app structure of the whole program
class App:

    #Initial run function
    def __init__(self):
        #Root
        self._root = tk.Tk()
        self._root.geometry("1200x1000+700+200")
        self._root.title("New Providence Community Pool Lifeguard Rotation Schedule Maker")

        # Mother Frame
        self._motherFrame = tk.Frame(self._root)
        self._motherFrame.pack(fill="both", expand=True)

        #Create static app info
        self._staticAppInfo = StaticAppInfo(self._root)

        #Create colors
        self._staticAppInfo.addColor(name="home", newColor="#08b0dd")
        self._staticAppInfo.addColor(name="schedule", newColor="#007994")
        self._staticAppInfo.addColor(name="default", newColor="#000000")
        self._staticAppInfo.addColor(name="error", newColor="#A50000")
        self._staticAppInfo.addColor(name="subText", newColor="#404040")
        self._staticAppInfo.addColor(name="lifeguard", newColor="#f25555")
        self._staticAppInfo.addColor(name="lifeguard", newColor="#f25555")
        self._staticAppInfo.addColor(name="redError", newColor="#700000")

        #Create fonts:
        self._staticAppInfo.addFont(name="title",
                                    newFont=font.Font(family="Arial", size=100, underline=True))
        self._staticAppInfo.addFont(name="subtitle",
                                    newFont=font.Font(family="Arial", size=20, underline=True))
        self._staticAppInfo.addFont(name="default",
                                    newFont=font.Font(family="Arial", size=20))
        self._staticAppInfo.addFont(name = "entry",
                                    newFont=font.Font(family="Segoe UI", size=11))
        self._staticAppInfo.addFont(name="standard",
                                    newFont=font.Font(family="Arial", size=30, underline=True))
        self._staticAppInfo.addFont(name="error",
                                    newFont=font.Font(family="Arial", size=15))
        self._staticAppInfo.addFont(name="smallDefault",
                                    newFont=font.Font(family="Arial", size=15))

        #Establish time interval
        self._staticAppInfo.setTimeInterval(20)

        # Set up home page
        self._homeFrame = tk.Frame()
        self.setUpHomePage()

        # Set up schedule page
        self._scheduleFrameObject = self.setUpSchedulePage()
        self._scheduleFrame = self._scheduleFrameObject.getScheduleFrame()
        self._staticAppInfo.addTypeEventToDict("stand")
        self._staticAppInfo.addEventDataSpecific("stand")

        # Set up lifeguard page
        self._lifeguardFrameObject = self.setUpLifeguardPage()
        self._lifeguardFrame = self._lifeguardFrameObject.getLifeguardFrame()
        self._staticAppInfo.addTypeEventToDict("lifeguard")
        self._staticAppInfo.addEventDataSpecific("lifeguard")

        # Concluding code to make the app appear
        self._homeFrame.tkraise()
        self._root.mainloop()
        return

    # Sets up the home page with widgets
    def setUpHomePage(self):
        # Home Frame
        self._homeFrame = tk.Frame(self._motherFrame, background=self._staticAppInfo.getColor("Home"))
        self._homeFrame.place(relwidth = 1, relheight = 1)

        # Label for Home Page
        homeText = ttk.Label(self._homeFrame,
                             text="Home",
                             foreground=self._staticAppInfo.getColor("Default"),
                             background=self._staticAppInfo.getColor("Home"),
                             font=self._staticAppInfo.getFont("title"))
        homeText.pack(side=tk.TOP, anchor = tk.W, padx = 5)

        # Open stand schedule button
        openScheduleButton = ttk.Button(self._homeFrame,
                                        text = "Set Stand Schedule",
                                        command = self.openScheduleFrame)
        openScheduleButton.pack(anchor = tk.W, padx = 10)

        # Open lifeguard button
        openLifeguardButton = ttk.Button(self._homeFrame,
                                         text = "Set Lifeguards",
                                         command = self.openLifeguardFrame)
        openLifeguardButton.pack(anchor = tk.W, padx = 10, pady = 5)

        #Open finished schedule button


    #Sets up the schedule page with widgets
    def setUpSchedulePage(self):
        scheduleFrame = ScheduleFrame(self._root,
                                      self._motherFrame,
                                      self._homeFrame,
                                      self._staticAppInfo)
        return scheduleFrame

    # Sets up the schedule page with widgets
    def setUpLifeguardPage(self):
        lifeguardFrame = LifeguardFrame(self._root,
                                        self._motherFrame,
                                        self._homeFrame,
                                        self._staticAppInfo)
        return lifeguardFrame

    #Opens up the schedule frame
    def openScheduleFrame(self):
        self._scheduleFrame.tkraise()

    #Opens up the lifeguard frame
    def openLifeguardFrame(self):
        self._lifeguardFrame.tkraise()

if __name__ == "__main__":
    App()
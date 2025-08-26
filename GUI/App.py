# import libraries
import tkinter as tk
from tkinter import ttk
from tkinter import font

from ScheduleFrame import ScheduleFrame
from LifeguardFrame import LifeguardFrame

from InfoManagers.StaticAppInfo import StaticAppInfo
from InfoManagers.CalculateSchedule import CalculateSchedule, CalculaterException

import webbrowser

from GoogleAPICommunicators.GoogleSheetsCommunicator import (
    GSCommunicator,
    WorksheetException,
    GSException,
)


# Mother app structure of the whole program
class App:
    # Initial run function
    def __init__(self):
        # Root
        self._root = tk.Tk()
        self._root.geometry("1200x1000+700+200")
        self._root.title(
            "New Providence Community Pool Lifeguard Rotation Schedule Maker"
        )

        # Mother Frame
        self._motherFrame = tk.Frame(self._root)
        self._motherFrame.pack(fill="both", expand=True)

        # Create static app info
        self._staticAppInfo = StaticAppInfo(self._root)

        # Create colors
        self._staticAppInfo.addColor(name="home", newColor="#08b0dd")
        self._staticAppInfo.addColor(name="schedule", newColor="#007994")
        self._staticAppInfo.addColor(name="default", newColor="#000000")
        self._staticAppInfo.addColor(name="error", newColor="#A50000")
        self._staticAppInfo.addColor(name="subText", newColor="#404040")
        self._staticAppInfo.addColor(name="lifeguard", newColor="#f25555")
        self._staticAppInfo.addColor(name="lifeguard", newColor="#f25555")
        self._staticAppInfo.addColor(name="redError", newColor="#700000")
        self._staticAppInfo.addColor(name="link", newColor="#00008B")

        # Create fonts:
        self._staticAppInfo.addFont(
            name="title", newFont=font.Font(family="Arial", size=100, underline=True)
        )
        self._staticAppInfo.addFont(
            name="subtitle", newFont=font.Font(family="Arial", size=20, underline=True)
        )
        self._staticAppInfo.addFont(
            name="default", newFont=font.Font(family="Arial", size=20)
        )
        self._staticAppInfo.addFont(
            name="entry", newFont=font.Font(family="Segoe UI", size=11)
        )
        self._staticAppInfo.addFont(
            name="standard", newFont=font.Font(family="Arial", size=30, underline=True)
        )
        self._staticAppInfo.addFont(
            name="error", newFont=font.Font(family="Arial", size=15)
        )
        self._staticAppInfo.addFont(
            name="smallDefault", newFont=font.Font(family="Arial", size=15)
        )

        # Establish time interval
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
        self._homeFrame = tk.Frame(
            self._motherFrame, background=self._staticAppInfo.getColor("Home")
        )
        self._homeFrame.place(relwidth=1, relheight=1)

        # Label for Home Page
        homeText = ttk.Label(
            self._homeFrame,
            text="Home",
            foreground=self._staticAppInfo.getColor("Default"),
            background=self._staticAppInfo.getColor("Home"),
            font=self._staticAppInfo.getFont("title"),
        )
        homeText.pack(side=tk.TOP, anchor=tk.W, padx=5)

        # Buttons list
        buttons = []

        # Open stand schedule button
        openScheduleButton = ttk.Button(
            self._homeFrame, text="Set Stand Schedule", command=self.openScheduleFrame
        )
        openScheduleButton.pack(anchor=tk.W, padx=10, pady=5)
        buttons.append(openScheduleButton)

        # Open lifeguard button
        openLifeguardButton = ttk.Button(
            self._homeFrame, text="Set Lifeguards", command=self.openLifeguardFrame
        )
        openLifeguardButton.pack(anchor=tk.W, padx=10, pady=5)
        buttons.append(openLifeguardButton)

        # Open finished schedule button
        calculateScheduleButton = ttk.Button(
            self._homeFrame,
            text="Calculate Schedule",
            command=self.openCalculatedScheduleFrame,
        )
        calculateScheduleButton.pack(anchor=tk.W, padx=10, pady=5)
        buttons.append(calculateScheduleButton)

        # Add buttons to the list of buttons to disable
        self._staticAppInfo.appendButtonListToDisable(buttons)

    # Sets up the schedule page with widgets
    def setUpSchedulePage(self):
        scheduleFrame = ScheduleFrame(
            self._root, self._motherFrame, self._homeFrame, self._staticAppInfo
        )
        return scheduleFrame

    # Sets up the schedule page with widgets
    def setUpLifeguardPage(self):
        lifeguardFrame = LifeguardFrame(
            self._root, self._motherFrame, self._homeFrame, self._staticAppInfo
        )
        return lifeguardFrame

    # Opens up the schedule frame
    def openScheduleFrame(self):
        self._scheduleFrame.tkraise()

    # Opens up the lifeguard frame
    def openLifeguardFrame(self):
        self._lifeguardFrame.tkraise()

    # Opens up the lifeguard frame
    def openCalculatedScheduleFrame(self):
        # Disable buttons
        self._staticAppInfo.disableButtons()

        # Create a new popup window
        popup = tk.Toplevel(self._root)
        popup.title("Calculate schedule")
        popup.geometry("500x400+900+400")

        popupFrame = tk.Frame(popup, background=self._staticAppInfo.getColor("Home"))
        popupFrame.pack(fill=tk.BOTH, expand=True)

        # Label
        label = tk.Label(
            popupFrame,
            text="Calculate Schedule:",
            background=self._staticAppInfo.getColor("Home"),
            font=self._staticAppInfo.getFont("Default"),
        )
        label.pack(pady=3, padx=5, anchor="w")

        # Create event entry
        entry = ttk.Entry(popupFrame, font=self._staticAppInfo.getFont("entry"))
        entry.pack(pady=3, padx=5, anchor="w")
        # Bind the enter action on the keyboard to adding the entry
        entry.bind(
            "<Return>",
            lambda event,
            i=popupFrame,
            entryField=entry,
            body=popupFrame,
            frame=popupFrame: on_submit,
        )

        # Function when submit is clicked
        def on_submit():
            try:
                submit_btn.config(state=tk.DISABLED)

                userInput = entry.get()

                link.configure(text="")
                errorText.configure(
                    text="Calculating schedule...",
                    foreground=self._staticAppInfo.getColor("subtext"),
                )
                self._root.update()

                calculator = CalculateSchedule(self._staticAppInfo)
                calculator.calculateSchedule()

                errorText.configure(
                    text="Writing schedule to spreadsheet...",
                    foreground=self._staticAppInfo.getColor("subtext"),
                )
                self._root.update()

                gs = GSCommunicator(self._staticAppInfo, calculator)
                gs.setWorksheet(userInput, "NPCP_GOOGLE_SHEETS_KEY")
                gs.writeScheduleToWorksheet()

                errorText.configure(
                    text=f"Done! Spreadsheet uploaded:\n",
                    foreground=self._staticAppInfo.getColor("subtext"),
                )
                link.configure(text="Click here!")
                link.bind(
                    "<Button-1>",
                    lambda e: webbrowser.open(gs.getItem("spreadsheet").url),
                )
                self._root.update()
            except CalculaterException as e:
                errMessage = str(e)
                errorText.configure(
                    text=f"Error while calculating:\n{errMessage}",
                    foreground=self._staticAppInfo.getColor("Error"),
                )
            except WorksheetException as e:
                errMessage = str(e)
                errorText.configure(
                    text=f"Error while setting spreadsheet:\n{errMessage}",
                    foreground=self._staticAppInfo.getColor("Error"),
                )
            except GSException as e:
                errMessage = str(e)
                errorText.configure(
                    text=f"Error while attempting to connect/write\n"
                    f"to spreadsheet:\n{errMessage}",
                    foreground=self._staticAppInfo.getColor("Error"),
                )

            submit_btn.config(state=tk.NORMAL)

        # Submit button
        submit_btn = tk.Button(popupFrame, text="Submit", command=on_submit)
        submit_btn.pack(pady=3, padx=5, anchor="w")

        # Create error text
        errorText = ttk.Label(
            popupFrame,
            text="",
            foreground=self._staticAppInfo.getColor("subtext"),
            background=self._staticAppInfo.getColor("home"),
            font=self._staticAppInfo.getFont("error"),
            anchor="w",
        )
        errorText.pack(pady=3, padx=5, anchor="w")

        # Create link
        link = ttk.Label(
            popupFrame,
            text="",
            foreground=self._staticAppInfo.getColor("link"),
            background=self._staticAppInfo.getColor("home"),
            font=self._staticAppInfo.getFont("subtext"),
            cursor="hand2",
        )
        link.pack(pady=3, padx=5, anchor="w")

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


if __name__ == "__main__":
    App()

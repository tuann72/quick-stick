import customtkinter as ctk  # Import customtkinter as ctk abbreviation
import tkinter as tk
from customtkinter import CTkImage  # Import CTkImage
from PIL import Image

TITLEBAR_FG_COLOR = "#fff170"
TEXTBOX_FG_COLOR = "#fffea1"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        minImg = CTkImage(Image.open("assets/min.png"), size=(10, 10))
        maxImg = CTkImage(Image.open("assets/max.png"), size=(10, 10))
        closeImg = CTkImage(Image.open("assets/close.png"), size=(10, 10))

        self.maximized = False

        # Sets the title of the window
        self.title("Quick Stick")

        # Creates starting layout size
        self.geometry("300x200")

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # self.overrideredirect(True)

        self.titleBar = ctk.CTkFrame(
            self, fg_color=TITLEBAR_FG_COLOR, height=15, corner_radius=0
        )
        self.titleBar.grid(row=0, column=0, sticky="ew")

        # Binds the titleBar to move window which holding right-mouse button
        self.titleBar.bind("<Button-1>", self.on_drag_start)
        self.titleBar.bind("<B1-Motion>", self.move_window)

        # Creates a label for the sticky note shown in the title bar
        self.titleBarLabel = ctk.CTkLabel(
            self.titleBar,
            height=14,
            text="",
            font=("Times", 14),
        )
        self.titleBarLabel.pack(side="left", padx=2, pady=2)

        # Create buttons to minimize, maximize, and close the window
        self.minBtn = BtnOptionModule(self.titleBar, minImg, self.min_window)
        self.maxBtn = BtnOptionModule(self.titleBar, maxImg, self.max_window)
        self.closeBtn = BtnOptionModule(self.titleBar, closeImg, self.close_window)

        self.closeBtn.pack(side="right", padx=2)
        self.maxBtn.pack(side="right", padx=2)
        self.minBtn.pack(side="right", padx=2)

        # Creating a textbox to hold user input
        self.textbox = ctk.CTkTextbox(
            self,
            font=("Times", 18),
            fg_color=TEXTBOX_FG_COLOR,
            width=325,
            corner_radius=0,
        )
        self.textbox.grid(row=1, column=0, sticky="nsew")
        self.textbox.bind("<KeyRelease>", self.update_title)
        # self.textbox.bind("<Button-1>", self.focus_text)

    # Records the initial position of the mouse
    def on_drag_start(self, event):
        # Records inital x position on the screen when clicked
        self.drag_start_x = event.x
        # Records the inital y position on the screen when clicked
        self.drag_start_y = event.y

    # Moves the window based on the difference between the mouse inital and final position
    def move_window(self, event):
        # winfo-rootx, x-coord of the top-left corner of the window relative to the screen
        # event.x, x-coord of the mouse relative to the widget
        new_x = self.winfo_rootx() + event.x - self.drag_start_x
        new_y = self.winfo_rooty() + event.y - self.drag_start_y
        self.geometry(f"+{new_x}+{new_y}")

    # Command for close button to close window
    def close_window(self):
        self.destroy()

    # Command for max button to maxmize window
    def max_window(self):
        # If already maximized we return it to original size
        if self.maximized:
            self.geometry("300x200")
            self.maximized = False
        else:
            # Sets screen to max size and moves window to the top left
            self.geometry(
                f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+{0}+{0}"
            )
            self.maximized = True

    # Command for min button to minimize window
    def min_window(self):
        self.iconify()

    # Updates the title bar's label which correlates to the first line of the textbox
    def update_title(self, event):
        # we get the last index of the 1st line
        endIndex = int(self.textbox.index("1.end").split(".")[1])

        # format the end index to apply to the get function
        endIndexFormat = f"1.0 + {endIndex} chars"

        # use the get function with the start and end index to get the text from the textbox
        self.text = self.textbox.get("1.0", endIndexFormat).strip()

        # Set the title bar label to be the text we obtained
        self.titleBarLabel.configure(text=self.text)


class BtnOptionModule(ctk.CTkButton):
    def __init__(self, master, icon, command=None):
        super().__init__(
            master,
            image=icon,
            border_spacing=0,
            text="",
            command=command,
            width=20,
            height=20,
            corner_radius=0,
            fg_color="transparent",
            hover_color="#e3e3e3",
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()

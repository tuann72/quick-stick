import customtkinter as ctk  # Import customtkinter as ctk abbreviation
import tkinter as tk
from customtkinter import CTkImage  # Import CTkImage
from PIL import Image, ImageDraw
from pystray import MenuItem as item
import pystray

from settings import (
    TITLE_BAR_COLOR_LIST,
    TEXTBOX_COLOR_LIST,
    BUTTON_HOVER_COLOR_LIST,
    TITLE_BAR_SIZE,
)

COLOR_CYCLE = 0
TITLE_BAR_COLOR = TITLE_BAR_COLOR_LIST[COLOR_CYCLE]
TEXTBOX_COLOR = TEXTBOX_COLOR_LIST[COLOR_CYCLE]
BUTTON_HOVER_COLOR = BUTTON_HOVER_COLOR_LIST[COLOR_CYCLE]


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        minImg = CTkImage(Image.open("assets/min.png"), size=(12, 12))
        maxImg = CTkImage(Image.open("assets/max.png"), size=(12, 12))
        closeImg = CTkImage(Image.open("assets/close.png"), size=(12, 12))

        self.maximized = False
        self.minimized = False
        self.titleBarLabelStr = ""

        # Sets the title of the window
        self.title("Quick Stick")

        # Creates starting layout size
        self.geometry("300x200")

        # Changes background color
        self.configure(fg_color=TEXTBOX_COLOR)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.columnconfigure(0, weight=1)

        self.overrideredirect(True)

        self.titleBar = ctk.CTkFrame(
            self, fg_color=TITLE_BAR_COLOR, height=TITLE_BAR_SIZE, corner_radius=0
        )
        self.titleBar.grid(row=0, column=0, sticky="ew")

        # Binds the titleBar to move window which holding right-mouse button
        self.titleBar.bind("<Button-1>", self.on_drag_start)
        self.titleBar.bind("<B1-Motion>", self.move_window)

        # Creates a label for the sticky note shown in the title bar
        # We are using a textbox widget because the normal label cuts off smaller font text
        self.titleBarLabel = ctk.CTkTextbox(
            self.titleBar,
            width=240,
            height=TITLE_BAR_SIZE,
            text_color="black",
            font=("Helvetica", 10),
            fg_color=TITLE_BAR_COLOR,
            corner_radius=0,
            state="disabled",
            wrap="none",
            activate_scrollbars=False,
        )
        self.titleBarLabel.pack(side="left", fill="y")

        self.titleBarLabel.bind("<Button-1>", self.on_drag_start)
        self.titleBarLabel.bind("<B1-Motion>", self.move_window)

        # Create buttons to minimize, maximize, and close the window
        self.minBtn = BtnOptionModule(self.titleBar, minImg, self.min_window)
        self.maxBtn = BtnOptionModule(self.titleBar, maxImg, self.max_window)
        self.closeBtn = BtnOptionModule(self.titleBar, closeImg, self.close_window)

        # Packs the buttons to the right side of the title bar
        self.closeBtn.pack(side="right")
        self.maxBtn.pack(side="right")
        self.minBtn.pack(side="right")

        # Creating a textbox to hold user input
        self.textbox = ctk.CTkTextbox(
            self,
            font=("Helvetica", 16),
            fg_color=TEXTBOX_COLOR,
            text_color="black",
            width=325,
            corner_radius=0,
        )
        self.textbox.grid(row=1, column=0, sticky="nsew")
        self.textbox.bind("<KeyRelease>", self.update_title)

        # Create a button for the bottom right to resize window
        self.resizeBtn = ctk.CTkButton(
            self,
            text="",
            width=8,
            height=8,
            corner_radius=0,
            fg_color=TEXTBOX_COLOR,
            hover_color=BUTTON_HOVER_COLOR,
        )
        self.resizeBtn.grid(row=2, column=0, sticky="e")
        self.resizeBtn.bind("<Button-1>", self.on_drag_start)
        self.resizeBtn.bind("<B1-Motion>", self.resize_window)

        # Set up system tray icon
        self.tray_icon = pystray.Icon(
            "icon", Image.open("assets/icon.ico"), "Quick-Stick", self.create_menu()
        )
        self.tray_icon.run_detached()

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

    # Resizes window when the bottom right button is selected and dragged
    def resize_window(self, event):
        new_x_size = self.winfo_width() + event.x - self.drag_start_x
        new_y_size = self.winfo_height() + event.y - self.drag_start_y
        if new_x_size >= 300 and new_y_size >= 60:
            self.geometry(f"{new_x_size}x{new_y_size}")

    # Command for close button to close window
    def close_window(self):
        # Closes window
        self.destroy()
        if self.tray_icon:
            self.tray_icon.stop()  # Stop the tray icon

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
        self.withdraw()
        self.tray_icon.visible = True  # Show the tray icon

    # Restores the window back to the screen
    def restore(self):
        self.deiconify()  # Show the window
        self.update_idletasks()  # Ensure the window is restored with the correct geometry
        self.tray_icon.visible = False  # Hide the tray icon

    # Create menu options for system tray icon
    def create_menu(self):
        # Creates two options, a restore option and a quit option.
        return (item("Restore", self.restore), item("Quit", self.close_window))

    # Command for collapse button to collapse window
    def collapse_window(self):
        if self.minimized:
            self.geometry("300x200")

            # Set the title bar label to be the text we obtained
            self.titleBarLabel.configure(state="normal")
            self.titleBarLabel.delete("1.0", "end")
            self.titleBarLabel.insert("1.0", "")
            self.titleBarLabel.configure(state="disabled")

            # Set the state of minimized to be False
            self.minimized = False
        else:
            self.geometry(f"{self.winfo_width()}x{TITLE_BAR_SIZE}")

            # Set the title bar label to be the text we obtained
            self.titleBarLabel.configure(state="normal")
            self.titleBarLabel.delete("1.0", "end")
            self.titleBarLabel.insert("1.0", self.titleBarLabelStr)
            self.titleBarLabel.configure(state="disabled")

            # Set the state of minimized to be true
            self.minimized = True

    # Updates the title bar's label which correlates to the first line of the textbox
    def update_title(self, event):
        # we get the last index of the 1st line
        endIndex = int(self.textbox.index("1.end").split(".")[1])

        # format the end index to apply to the get function
        endIndexFormat = f"1.0 + {endIndex} chars"

        # use the get function with the start and end index to get the text from the textbox
        self.titleBarLabelStr = self.textbox.get("1.0", endIndexFormat).strip()


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
            hover_color=BUTTON_HOVER_COLOR,
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()

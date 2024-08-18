import customtkinter as ctk  # Import customtkinter as ctk abbreviation
from customtkinter import CTkImage  # Import CTkImage
from PIL import Image

TITLEBAR_FG_COLOR = "#fff170"
TEXTBOX_FG_COLOR = "#fffea1"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Sets the title of the window
        self.title("Quick Stick")

        # Creates starting layout size
        self.geometry("325x225")

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # self.overrideredirect(True)

        minImg = CTkImage(Image.open("assets/min.png"), size=(10, 10))
        maxImg = CTkImage(Image.open("assets/max.png"), size=(10, 10))
        closeImg = CTkImage(Image.open("assets/close.png"), size=(10, 10))

        self.titleBar = ctk.CTkFrame(
            self, fg_color=TITLEBAR_FG_COLOR, height=15, corner_radius=0
        )
        self.titleBar.grid(row=0, column=0, sticky="ew")

        self.titleBarLabel = ctk.CTkLabel(
            self.titleBar,
            height=14,
            text="gjp",
            font=("Times", 14),
        )
        self.titleBarLabel.pack(side="left", padx=12, pady=2)

        self.minBtn = BtnOptionModule(self.titleBar, minImg, self.min_window)
        self.maxBtn = BtnOptionModule(self.titleBar, maxImg, self.max_window)
        self.closeBtn = BtnOptionModule(self.titleBar, closeImg, self.close_window)

        self.closeBtn.pack(side="right", padx=2)
        self.maxBtn.pack(side="right", padx=2)
        self.minBtn.pack(side="right", padx=2)

        # Creating a textbox to hold user input
        self.textbox = ctk.CTkTextbox(
            self, fg_color=TEXTBOX_FG_COLOR, width=325, corner_radius=0
        )
        self.textbox.grid(row=1, column=0, sticky="nsew")

    def close_window(self):
        self.destroy()

    def max_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+{0}+{0}")

    def min_window(self):
        self.iconify()


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

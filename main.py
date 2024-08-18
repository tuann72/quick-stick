import customtkinter as ctk  # Import customtkinter as ctk abbreviation

from customtkinter import CTkImage

from PIL import Image


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Sets the title of the window
        self.title("Quick Stick")

        # Creates starting layout size
        self.geometry("325x225")

        # Configures a grids' rows and columns
        self.grid_rowconfigure(0, weight=0)  # Set for button options to be fixed size
        self.grid_rowconfigure(1, weight=1)  # Set for textbox to be resizable

        self.grid_columnconfigure(0, weight=1)  # Single column to contain all items

        self.btnFrame = TextOptionFrame(self)
        self.btnFrame.grid(
            row=0,
            column=0,
        )

        # Creating a textbox to hold user input
        self.textbox = ctk.CTkTextbox(self, width=325, corner_radius=0)
        self.textbox.grid(row=1, column=0, sticky="nsew")


class TextOptionFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        boldImg = CTkImage(Image.open("assets/bold.png"))
        fontImg = CTkImage(Image.open("assets/font.png"))
        italicImg = CTkImage(Image.open("assets/italic.png"))

        # Creating a frame to hold all button options
        self.btnFrame = ctk.CTkFrame(self, fg_color="red", height=10, corner_radius=0)
        self.btnFrame.grid(row=0, column=0)

        self.fontBtn = BtnOptionModule(self.btnFrame, fontImg)
        self.fontBtn.pack(side="left", padx="5")

        self.boldBtn = BtnOptionModule(self.btnFrame, boldImg)
        self.boldBtn.pack(side="left", padx="5")

        self.italicBtn = BtnOptionModule(self.btnFrame, italicImg)
        self.italicBtn.pack(side="left", padx="5")


class BtnOptionModule(ctk.CTkButton):
    def __init__(self, master, icon, command=None):
        super().__init__(
            master, image=icon, text="", command=command, width=20, height=20
        )


app = App()
app.mainloop()

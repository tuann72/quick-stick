import customtkinter as ctk  # Import customtkinter as ctk abbreviation
from customtkinter import CTkImage  # Import CTkImage
from PIL import Image

ctk.set_appearance_mode("dark")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        boldImg = CTkImage(Image.open("assets/bold.png"))
        fontImg = CTkImage(Image.open("assets/font.png"))
        italicImg = CTkImage(Image.open("assets/italic.png"))

        # Sets the title of the window
        self.title("Quick Stick")

        # Creates starting layout size
        self.geometry("325x225")

        # Configures a grids' rows and columns
        self.grid_rowconfigure(0, weight=0)  # Set for button options to be fixed size
        self.grid_rowconfigure(1, weight=1)  # Set for textbox to be resizable

        self.grid_columnconfigure(0, weight=1)  # Single column to contain all items

        # self.btnFrame = TextOptionFrame(self)
        self.btnFrame = ctk.CTkFrame(self, height=10, corner_radius=0, fg_color="red")
        self.btnFrame.grid(row=0, column=0, sticky="ew")

        # Center the frame in the window
        self.btnFrame.grid_columnconfigure(0, weight=1)
        self.btnFrame.grid_columnconfigure(1, weight=1)
        self.btnFrame.grid_columnconfigure(2, weight=1)

        self.fontBtn = BtnOptionModule(self.btnFrame, fontImg)
        self.boldBtn = BtnOptionModule(self.btnFrame, boldImg)
        self.italicBtn = BtnOptionModule(self.btnFrame, italicImg)

        ##### Fix Padding Issue

        self.fontBtn.grid(row=0, column=0, padx=1)
        self.boldBtn.grid(row=0, column=1, padx=1)
        self.italicBtn.grid(row=0, column=2, padx=1)

        # Creating a textbox to hold user input
        self.textbox = ctk.CTkTextbox(self, width=325, corner_radius=0)
        self.textbox.grid(row=1, column=0, sticky="nsew")


class BtnOptionModule(ctk.CTkButton):
    def __init__(self, master, icon, command=None):
        super().__init__(
            master, image=icon, text="", command=command, width=20, height=20
        )


app = App()
app.mainloop()

import customtkinter as ctk  # Import customtkinter as ctk abbreviation


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

        # Creating a frame to hold all button options
        self.btnFrame = ctk.CTkFrame(self, fg_color="red", height=40, corner_radius=0)
        self.btnFrame.grid(row=0, column=0, sticky="nsew")

        self.btn = ctk.CTkButton(self.btnFrame, text="Button", width=20, height=20)
        self.btn.grid(row=0, column=0, padx=10)

        # Creating a textbox to hold user input
        self.textbox = ctk.CTkTextbox(self, width=325, corner_radius=0)
        self.textbox.grid(row=1, column=0, sticky="nsew")


app = App()
app.mainloop()

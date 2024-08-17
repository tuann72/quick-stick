import customtkinter as ctk                          # Import customtkinter as ctk abbreviation
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("325x225")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.textbox = ctk.CTkTextbox(self, width=325, corner_radius=0)
        self.textbox.grid(row=0, column=0, sticky="nsew")


app = App()
app.mainloop()
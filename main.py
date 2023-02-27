from utils.file_operations import get_appdata_logs, get_programdata_logs

import customtkinter


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("500x300")
        self.title("small example app")
        self.minsize(300, 200)

        # create 2x2 grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.textbox = customtkinter.CTkTextbox(master=self)
        self.textbox.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="nsew")

        self.button = customtkinter.CTkButton(master=self, command=self.button_callback, text="Fetch logs")
        self.button.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

    def button_callback(self):
        self.textbox.insert("insert", "Fetching programdata logs: \n")
        self.textbox.insert("insert", get_programdata_logs() + "\n\n")
        self.textbox.insert("insert", "Fetching appdata logs: \n")
        self.textbox.insert("insert", get_appdata_logs() + "\n")


if __name__ == "__main__":
    app = App()
    app.mainloop()


from utils.file_operations import get_anydesk_logs
from os import getenv

import customtkinter

app_data_path = getenv('APPDATA')
app_data_filename = f'{app_data_path}/AnyDesk/ad.trace'
program_data_path = getenv('PROGRAMDATA')
program_data_filename = f'{program_data_path}/AnyDesk/ad_svc.trace'


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("500x300")
        self.title("AnyGrabber")
        self.minsize(300, 200)

        # create 2x2 grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.textbox = customtkinter.CTkTextbox(master=self)

        self.textbox.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="nsew")

        self.button = customtkinter.CTkButton(master=self, command=self.button_callback, text="Fetch logs")
        self.button.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

    def button_callback(self):
        self.textbox.delete("0.0", "end")  # delete all text
        log_entries = get_anydesk_logs(app_data_filename)
        self.textbox.insert("insert", "Fetching appdata logs: \n")
        for entry in log_entries:
            self.textbox.insert("insert", entry + "\n\n")
        log_entries = get_anydesk_logs(program_data_filename)
        self.textbox.insert("insert", "Fetching programdata logs: \n")
        for entry in log_entries:
            self.textbox.insert("insert", entry + "\n\n")
        self.textbox.configure(state="disabled")


if __name__ == "__main__":
    app = App()
    app.mainloop()

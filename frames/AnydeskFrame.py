import customtkinter
import tkinter
import os

from utils.file_operations import get_anydesk_logs

app_data_path = os.getenv('APPDATA')
app_data_filename = f'{app_data_path}/AnyDesk/ad.trace'
program_data_path = os.getenv('PROGRAMDATA')
program_data_filename = f'{program_data_path}/AnyDesk/ad_svc.trace'


class AnydeskFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create checkbox and switch frame
        self.checkbox_var = tkinter.BooleanVar()
        self.checkbox_var2 = tkinter.BooleanVar()

        self.checkbox_slider_frame = customtkinter.CTkFrame(master=self)
        self.checkbox_slider_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, variable=self.checkbox_var,
                                                    onvalue=True, offvalue=False)
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, variable=self.checkbox_var2,
                                                    onvalue=True, offvalue=False)
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")

        self.button = customtkinter.CTkButton(self, command=self.button_callback,
                                              text="Fetch logs")

        self.button.grid(row=1, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="ew")

        self.textbox = customtkinter.CTkTextbox(self)
        self.textbox.grid(row=2, column=0, padx=20, pady=20, sticky='nsew')

    def button_callback(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")  # delete all text

        if self.checkbox_var.get():
            log_entries = get_anydesk_logs(app_data_filename)
            self.textbox.insert("insert", "Fetching appdata logs: \n")
            for entry in log_entries:
                self.textbox.insert("insert", entry + "\n\n")
        if self.checkbox_var2.get():
            log_entries = get_anydesk_logs(program_data_filename)
            self.textbox.insert("insert", "Fetching programdata logs: \n")
            for entry in log_entries:
                self.textbox.insert("insert", entry + "\n\n")
        self.textbox.configure(state="disabled")

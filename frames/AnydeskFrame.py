import customtkinter
import tkinter
import os

from utils.file_operations import get_anydesk_logs

# Define paths to AnyDesk log files (ad.trace and ad_svc.trace)
app_data_path = os.getenv('APPDATA')
app_data_filename = f'{app_data_path}/AnyDesk/ad.trace'
program_data_path = os.getenv('PROGRAMDATA')
program_data_filename = f'{program_data_path}/AnyDesk/ad_svc.trace'


class AnydeskFrame(customtkinter.CTkFrame):
    """A frame that contains widgets for fetching AnyDesk logs and displaying them in a textbox.
    """

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
        """A callback function that calls functions that print output generated by log fetching functions to textbox
        when appropriate switch is selected

        Clears texbox contents after it gets invoked, and disables textbox editing after fetching data"""
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")  # delete all text
        if self.checkbox_var.get():
            self.print_logs(log_filename_with_path=app_data_filename)
        if self.checkbox_var2.get():
            self.print_logs(log_filename_with_path=program_data_filename)
        self.textbox.configure(state="disabled")

    def print_logs(self, log_filename_with_path: str):
        """A function that calls get_anydesk_logs function and prints output to textbox

        Shows a message if no logs are found in a file or if file doesn't exist

        :param log_filename_with_path: a path to a file that contains Anydesk logs
        """
        log_entries = get_anydesk_logs(log_filename_with_path)
        if log_entries is not None:
            self.textbox.insert("insert", f'Fetching logs from {log_filename_with_path}: \n')
            if len(log_entries) < 1:
                self.textbox.insert("insert", "No IP logs found inside file!")
            else:
                for entry in log_entries:
                    self.textbox.insert("insert", entry + "\n\n")
        else:
            self.textbox.insert("insert", f'Logs not found in {log_filename_with_path} \n')

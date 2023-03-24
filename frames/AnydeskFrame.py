import os
import threading
import tkinter
from collections import deque

import customtkinter

from utils.file_operations import get_anydesk_logs, create_timestamped_directory, copy_and_generate_checksum, \
    create_folders_from_path, generate_txt_report, generate_csv_report

# Define paths to AnyDesk log files (ad.trace and ad_svc.trace)
app_data_path = os.getenv('APPDATA')
program_data_path = os.getenv('PROGRAMDATA')

# Means of communication, between the gui & update threads:
message_queue = deque()
search_finished = False

report_folder_path: str = ""


def find_files(filename: str | list, search_path) -> int:
    """A function that searches for files in a given path and returns a list of paths to found files"""
    # Walking top-down from the root
    number_of_found_files = 0
    for root, dir, files in os.walk(search_path):
        if type(filename) == list:
            for name in filename:
                if name in files:
                    message_queue.append(os.path.join(root, name))
                    number_of_found_files += 1
        else:
            if filename in files:
                message_queue.append(os.path.join(root, filename))
                number_of_found_files += 1
    return number_of_found_files


class AnydeskFrame(customtkinter.CTkFrame):
    """A frame that contains widgets for fetching AnyDesk logs and displaying them in a textbox.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # create checkbox and switch frame
        self.fetch_appdata_logs_switch = tkinter.BooleanVar(value=True)
        self.fetch_programdata_logs_switch = tkinter.BooleanVar(value=True)
        self.find_files_switch = tkinter.BooleanVar(value=False)

        self.checkbox_slider_frame = customtkinter.CTkFrame(master=self)
        self.checkbox_slider_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.checkbox_slider_frame_label = customtkinter.CTkLabel(master=self.checkbox_slider_frame,
                                                                  text_color=("#333", "#ccc"),
                                                                  text="Choose where to search for logs:",
                                                                  font=customtkinter.CTkFont(size=15, weight="bold"))
        self.checkbox_slider_frame_label.grid(row=0, column=0, columnspan=3, sticky="n")
        self.checkbox_fetch_appdata_logs = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,
                                                                     variable=self.fetch_appdata_logs_switch,
                                                                     text_color=("#333", "#ccc"),
                                                                     onvalue=True, offvalue=False, text="AppData")
        self.checkbox_fetch_appdata_logs.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_fetch_programdata_logs = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,
                                                                         variable=self.fetch_programdata_logs_switch,
                                                                         onvalue=True, offvalue=False,
                                                                         text_color=("#333", "#ccc"),
                                                                         text="ProgramData")
        self.checkbox_fetch_programdata_logs.grid(row=1, column=1, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_find_logs = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,
                                                            variable=self.find_files_switch,
                                                            text_color=("#333", "#ccc"),
                                                            onvalue=True, offvalue=False, text="Search custom location "
                                                                                               "for logs",
                                                            command=self.toggle_checkboxes)
        self.checkbox_find_logs.grid(row=1, column=2, pady=20, padx=20, sticky="n")

        self.textbox = customtkinter.CTkTextbox(self)
        self.textbox.grid(row=2, column=0, padx=20, pady=20, sticky='nsew')
        self.textbox.configure(text_color=("#333", "#ccc"))

        self.fetch_logs_button = customtkinter.CTkButton(self,
                                                         command=self.button_callback,
                                                         text_color=("#eee", "#ccc"),
                                                         text="Fetch logs")

        self.fetch_logs_button.grid(row=1, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="ew")

    def button_callback(self):
        """A callback function that calls functions that print output generated by log fetching functions to textbox
        when appropriate switch is selected

        Clears texbox contents after it gets invoked, and disables textbox editing after fetching data"""
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")  # delete all text
        global report_folder_path
        report_folder_path = create_timestamped_directory()
        if self.fetch_appdata_logs_switch.get():
            threading.Thread(target=self.search_filesystem_callback, args=[app_data_path], daemon=True).start()
        if self.fetch_programdata_logs_switch.get():
            threading.Thread(target=self.search_filesystem_callback, args=[program_data_path], daemon=True).start()
        if self.checkbox_find_logs.get():
            search_location = customtkinter.filedialog.askdirectory()
            threading.Thread(target=self.search_filesystem_callback, args=[search_location], daemon=True).start()

    def print_logs(self, log_filename_with_path: str):
        """A function that calls get_anydesk_logs function and prints output to textbox

        get_anydesk_logs searches through a file and returns a list of IP addresses that were found in it
        print_logs inserts result into textbox and shows a message if no logs are found in a file or if file doesn't 
        exist. It also displays a message if file is empty or no IP addresses were found in it.

        :param log_filename_with_path: a path to a file that contains Anydesk logs
        """
        log_entries = get_anydesk_logs(log_filename_with_path)
        if log_entries is not None:
            self.textbox.insert("insert", f'Fetching logs from {log_filename_with_path}: \n\n')
            if len(log_entries) < 1:
                self.textbox.insert("insert", "No IP logs found inside file!")
            else:
                for entry in log_entries:
                    self.textbox.insert("insert", entry + " - " + log_entries[entry] + "\n\n")
        else:
            self.textbox.insert("insert", f'Logs not found in {log_filename_with_path} \n')

    def search_filesystem_callback(self, search_location: str):
        """A callback function that calls find_files function and prints output to textbox

        It's a wrapper that is responsible for displaying a progressbar while find_files is running, disabling
        checkboxes and buttons while searching for files and enabling them after search is finished.
        It calls update_textbox function to update textbox contents while find_files is running.
        It cleans up after itself by destroying progressbar and enabling buttons and checkboxes after search is finished.
        """
        global search_finished
        self.textbox.insert("insert", f'---- Searching for files in:\n{search_location}\nit may take a while! ----\n\n')
        self.fetch_logs_button.configure(state="disabled")
        self.checkbox_fetch_appdata_logs.configure(state="disabled")
        self.checkbox_fetch_programdata_logs.configure(state="disabled")
        self.checkbox_find_logs.configure(state="disabled")
        progressbar = customtkinter.CTkProgressBar(master=self, mode="indeterminate", indeterminate_speed=1.15)
        progressbar.grid(row=4, column=0, pady=20, padx=20, sticky="ew")
        progressbar.start()
        search_finished = False
        self.generate_and_present_search_results()
        number_of_found_files = find_files(["ad.trace", "ad_svc.trace"], search_location)
        search_finished = True
        progressbar.stop()
        progressbar.destroy()
        self.fetch_logs_button.configure(state="normal")
        self.checkbox_fetch_appdata_logs.configure(state="normal")
        self.checkbox_fetch_programdata_logs.configure(state="normal")
        self.checkbox_find_logs.configure(state="normal")
        if number_of_found_files == 0:
            self.after(500,
                       func=self.textbox.insert("insert", f'\n---- No files were found in {search_location}! ----\n\n'))
        else:
            self.after(500, self.textbox.insert("insert", "\n---- Searching for files finished! ----\n\n"))

    def generate_and_present_search_results(self, write_header=True):
        """A function that updates the textbox with new logs found by the search function

        It is called recursively every 2 seconds by the gui thread, and it checks if the search function has finished
        searching
        """

        try:
            found_file = message_queue.popleft()
            destination_path = create_folders_from_path(found_file, report_folder_path)
            copy_and_generate_checksum(found_file, destination_path)
            self.print_logs(found_file)
            log_entries = get_anydesk_logs(found_file)
            generate_txt_report(report_folder_path, write_header, log_entries, found_file)
            generate_csv_report(report_folder_path, write_header, log_entries, found_file)
        except IndexError:
            pass
        if not search_finished:
            self.after(500, self.generate_and_present_search_results, False)

    def toggle_checkboxes(self):
        """A function that disables checkboxes if "Search filesystem for logs" checkbox is selected"""
        if self.checkbox_find_logs.get():
            self.fetch_appdata_logs_switch.set(False)
            self.fetch_programdata_logs_switch.set(False)
            self.checkbox_fetch_appdata_logs.configure(state="disabled")
            self.checkbox_fetch_programdata_logs.configure(state="disabled")
        else:
            self.checkbox_fetch_appdata_logs.configure(state="normal")
            self.checkbox_fetch_programdata_logs.configure(state="normal")

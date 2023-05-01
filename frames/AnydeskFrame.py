import os
import threading
import tkinter
import customtkinter
from collections import deque
from utils.locale_utils import change_frame_locale

from utils.file_operations import get_anydesk_logs, create_timestamped_directory, copy_and_generate_checksum, \
    create_folders_from_path, generate_txt_report, generate_csv_report

_ = change_frame_locale('HomeFrame')

# Define paths to AnyDesk log files (ad.trace and ad_svc.trace)
app_data_path = os.getenv('APPDATA')
program_data_path = os.getenv('PROGRAMDATA')

# Means of communication, between the gui & update threads:
message_queue = deque()
search_finished: bool = False
write_header: bool = True
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
    """A frame that contains widgets for fetching AnyDesk logs and displaying them in a textbox."""

    def change_locale(self, master, locale):
        global _
        _ = change_frame_locale("HomeFrame", locale)
        self.checkbox_frame_label.configure(text=_("Choose where to search for logs:"))
        self.checkbox_search_for_logs_in_location.configure(text=_("Search custom location "
                                                                   "for logs"))
        self.fetch_logs_button.configure(text=_("Fetch logs"))
        self.open_report_button.configure(text=_("Open report"))

    def __init__(self, master, **kwargs):
        """Initialize the frame and its widgets."""
        super().__init__(master, **kwargs)

        # configure grid of frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # set switches responsible for fetching logs from specific locations
        # switches are used to determine the state of checkboxes
        self.switch_fetch_appdata_logs = tkinter.BooleanVar(value=True)
        self.switch_fetch_programdata_logs = tkinter.BooleanVar(value=True)
        self.switch_search_for_logs_in_location = tkinter.BooleanVar(value=False)

        # Checkbox frame responsible for selecting where to search for logs
        self.checkbox_frame = customtkinter.CTkFrame(master=self)
        self.checkbox_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.checkbox_frame_label = customtkinter.CTkLabel(master=self.checkbox_frame,
                                                           text_color=("#333", "#ccc"),
                                                           text=_("Choose where to search for logs:"),
                                                           font=customtkinter.CTkFont(size=15, weight="bold"))
        self.checkbox_frame_label.grid(row=0, column=0, columnspan=3, sticky="n")

        # Checkboxes responsible for selecting where to search for logs
        # Checkbox for searching for logs in AppData
        self.checkbox_fetch_appdata_logs = customtkinter.CTkCheckBox(master=self.checkbox_frame,
                                                                     variable=self.switch_fetch_appdata_logs,
                                                                     text_color=("#333", "#ccc"),
                                                                     onvalue=True, offvalue=False, text="AppData",
                                                                     command=lambda: self.turn_off_switches([
                                                                         self.switch_search_for_logs_in_location]))
        self.checkbox_fetch_appdata_logs.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")

        # Checkbox for searching for logs in ProgramData
        self.checkbox_fetch_programdata_logs = customtkinter.CTkCheckBox(master=self.checkbox_frame,
                                                                         variable=self.switch_fetch_programdata_logs,
                                                                         onvalue=True, offvalue=False,
                                                                         text_color=("#333", "#ccc"),
                                                                         text="ProgramData",
                                                                         command=lambda: self.turn_off_switches([
                                                                             self.switch_search_for_logs_in_location]))
        self.checkbox_fetch_programdata_logs.grid(row=1, column=1, pady=(20, 0), padx=20, sticky="n")

        # Checkbox for searching for logs in custom location
        self.checkbox_search_for_logs_in_location = customtkinter.CTkCheckBox(master=self.checkbox_frame,
                                                                              variable=self.switch_search_for_logs_in_location,
                                                                              text_color=("#333", "#ccc"),
                                                                              onvalue=True, offvalue=False,
                                                                              text=_("Search custom location "
                                                                                     "for logs"),
                                                                              command=lambda: self.turn_off_switches([
                                                                                  self.switch_fetch_programdata_logs,
                                                                                  self.switch_fetch_appdata_logs]))
        self.checkbox_search_for_logs_in_location.grid(row=1, column=2, pady=20, padx=20, sticky="n")

        # Textbox where output of log fetching functions is displayed
        self.textbox = customtkinter.CTkTextbox(self)
        self.textbox.grid(row=2, column=0, padx=20, pady=20, sticky='nsew')
        self.textbox.configure(text_color=("#333", "#ccc"))

        # Button that starts fetching logs
        self.fetch_logs_button = customtkinter.CTkButton(self,
                                                         command=self.fetch_logs_button_callback,
                                                         text_color=("#eee", "#ccc"),
                                                         text=_("Fetch logs"))

        self.fetch_logs_button.grid(row=1, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="ew")

        # Button that opens a folder with report
        self.open_report_button = customtkinter.CTkButton(self,
                                                          command=self.open_report_folder,
                                                          text_color=("#eee", "#ccc"),
                                                          text=_("Open report"))
        self.open_report_button.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        # Hide the button until logs are fetched
        self.open_report_button.grid_remove()

    def fetch_logs_button_callback(self):
        """A callback function that calls functions that print output generated by log fetching functions to textbox
        when appropriate switch is selected

        Clears texbox contents after it gets invoked, and disables textbox editing after fetching data"""
        global write_header
        write_header = True
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")

        # Create a timestamped directory for storing logs and reports
        global report_folder_path
        report_folder_path = create_timestamped_directory()

        # Run a thread for each switch that is turned on
        # Threads are used to prevent the GUI from freezing
        if self.switch_fetch_appdata_logs.get():
            threading.Thread(target=self.search_filesystem_callback, args=[app_data_path], daemon=True).start()
        if self.switch_fetch_programdata_logs.get():
            threading.Thread(target=self.search_filesystem_callback, args=[program_data_path], daemon=True).start()
        if self.checkbox_search_for_logs_in_location.get():
            search_location = customtkinter.filedialog.askdirectory()
            threading.Thread(target=self.search_filesystem_callback, args=[search_location], daemon=True).start()

    def print_logs_to_textbox(self, log_filename_with_path: str):
        """A function that calls get_anydesk_logs function and prints output to textbox

        get_anydesk_logs searches through a file and returns a list of IP addresses that were found in it
        print_logs inserts result into textbox and shows a message if no logs are found in a file or if file doesn't 
        exist. It also displays a message if file is empty or no IP addresses were found in it.

        :param log_filename_with_path: a path to a file that contains Anydesk logs
        """
        log_entries = get_anydesk_logs(log_filename_with_path)
        if log_entries is not None:
            self.textbox.insert("insert", '{} {}: \n\n'.format(_('Fetching logs from'), log_filename_with_path))
            if len(log_entries) < 1:
                self.textbox.insert("insert", '{} \n\n'.format(_('No IP logs found inside file!'))
                                    )
            else:
                for entry in log_entries:
                    self.textbox.insert("insert", entry + " - " + log_entries[entry] + "\n\n")
        else:
            self.textbox.insert("insert", '{} {} \n'.format(_('Logs not found in'), log_filename_with_path)
                                )

    def search_filesystem_callback(self, search_location: str):
        """A callback function that calls find_files function and prints output to textbox

        It's a wrapper that is responsible for displaying a progressbar while find_files is running, disabling
        checkboxes and buttons while searching for files and enabling them after search is finished.
        It calls update_textbox function to update textbox contents while find_files is running.
        It cleans up after itself by destroying progressbar and enabling buttons and checkboxes after search is finished.
        """
        global search_finished, write_header
        self.open_report_button.grid_remove()
        self.textbox.insert("insert",
                            '---- {}: \n\n{}\n\n{}! ----\n\n\n'.format(_('Searching for files in'), search_location,
                                                                       _('it may take a while'))
                            )

        # Disable buttons and checkboxes while searching for files
        self.toggle_checkboxes_and_buttons_state([
            self.fetch_logs_button,
            self.checkbox_fetch_appdata_logs,
            self.checkbox_fetch_programdata_logs,
            self.checkbox_search_for_logs_in_location
        ])

        # Create a progressbar and start it while searching for files
        progressbar = customtkinter.CTkProgressBar(master=self, mode="indeterminate", indeterminate_speed=1.15)
        progressbar.grid(row=4, column=0, pady=20, padx=20, sticky="ew")
        progressbar.start()

        # Set search_finished to False while searching for files
        # This is used to prevent update_textbox function from updating textbox contents after search is finished
        # The generate_and_present_search_results function is called recursively until search is finished
        search_finished = False
        self.generate_and_present_search_results()
        number_of_found_files = find_files(["ad.trace", "ad_svc.trace"], search_location)
        search_finished = True

        # Stop progressbar and destroy it after search is finished
        progressbar.stop()
        progressbar.destroy()

        # Enable buttons and checkboxes after search is finished
        self.toggle_checkboxes_and_buttons_state([
            self.fetch_logs_button,
            self.checkbox_fetch_appdata_logs,
            self.checkbox_fetch_programdata_logs,
            self.checkbox_search_for_logs_in_location
        ])

        # Display a message if no files were found in search location
        # Generate a report with a message if no files were found in search location
        if number_of_found_files == 0:
            self.open_report_button.grid()
            self.textbox.insert("insert", '\n---- {} {}! ----\n\n'.format(_('No files were found in'), search_location))
            with open(os.path.join(report_folder_path, "report.txt"), "a") as report_file:
                report_file.write('---- {} {} ----\n\n'.format(_('No files were found in'), search_location))
        # Display a message if search is finished
        else:
            self.open_report_button.grid()
            self.textbox.insert("insert", '---- {}! ----'.format(_('Searching for files finished')))

    def generate_and_present_search_results(self):
        """A function that updates the textbox with new logs found by the search function

        It is called recursively every 2 seconds by the gui thread, and it checks if the search function has finished
        searching
        """
        global write_header
        try:
            found_file = message_queue.popleft()
            destination_path = create_folders_from_path(found_file, report_folder_path)
            copy_and_generate_checksum(found_file, destination_path)
            self.print_logs_to_textbox(found_file)
            log_entries = get_anydesk_logs(found_file)
            generate_txt_report(report_folder_path, write_header, log_entries, found_file)
            generate_csv_report(report_folder_path, write_header, log_entries, found_file)
            write_header = False
        except IndexError:
            pass
        if not search_finished:
            self.after(200, self.generate_and_present_search_results)

    @staticmethod
    def turn_off_switches(switches_list: list[tkinter.BooleanVar]):
        """A function that turns off switches passed as a parameter

        It is needed because switches that correspond to checkboxes responsible for searching default location should
        be turned off when user selects a custom location to search for logs This prevents the program from searching
        for logs in default locations when user selects a custom location to search for logs Without this the program
        would search default location twice - once for default location search and second time when doing a full
        location search. This would result in duplicate entries in the report file.

        :param switches_list: a list of switches that should be turned off
        """
        for switch in switches_list:
            switch.set(False)

    @staticmethod
    def toggle_checkboxes_and_buttons_state(
            checkboxes_and_buttons_list: list[customtkinter.CTkCheckBox | customtkinter.CTkButton]):
        """A function that enables or disables checkboxes and buttons passed as a parameter

        :param checkboxes_and_buttons_list: a list of checkboxes and buttons that should be enabled or disabled
        """
        for checkbox_or_button in checkboxes_and_buttons_list:
            if checkbox_or_button.cget('state') == "normal":
                checkbox_or_button.configure(state="disabled")
            else:
                checkbox_or_button.configure(state="normal")

    @staticmethod
    def open_report_folder():
        """A function that opens the folder where the report file is located"""
        try:
            os.startfile(report_folder_path)
        except FileNotFoundError:
            print(_("Report folder not found!"))

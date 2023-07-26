import os
import threading
import tkinter
import fnmatch
from collections import deque
from typing import Literal

from CTkMessagebox import CTkMessagebox
from PIL import Image
from utils.event_utils import myEvent
from utils.sound_utils import play_message_beep

import customtkinter

import global_state
from utils.file_operations import get_anydesk_logs, create_timestamped_directory, copy_and_generate_checksum, \
    create_folders_from_path, generate_txt_report, generate_csv_report
from utils.locale_utils import _

# Define paths to AnyDesk log files (ad.trace and ad_svc.trace)
app_data_path = os.getenv('APPDATA')
program_data_path = os.getenv('PROGRAMDATA')

# Means of communication, between the gui & update threads:
message_queue = deque()
search_finished: bool = False
write_header: bool = True
report_folder_path: str = ""
stop_searching: bool = False

# Images for buttons
image_path = os.path.join(os.getcwd(), "assets")
fetch_logs_image = customtkinter.CTkImage(
    light_image=Image.open(os.path.join(image_path, "search_light.png")),
    dark_image=Image.open(os.path.join(image_path, "search_dark.png")),
    size=(20, 20))
open_report_image = customtkinter.CTkImage(
    light_image=Image.open(os.path.join(image_path, "open_report_light.png")),
    dark_image=Image.open(os.path.join(image_path, "open_report_dark.png")),
    size=(20, 20))


class AnydeskFrame(customtkinter.CTkFrame):
    """A frame that contains widgets for fetching AnyDesk logs and displaying them in a textbox."""

    def __init__(self, master, **kwargs):
        """Initialize the frame and its widgets."""
        super().__init__(master, **kwargs)
        self.worker_threads_started = customtkinter.IntVar(value=0)
        self.worker_threads_finished = customtkinter.IntVar(value=0)
        self.found_file_event = myEvent()
        self.found_file_event.registerCallback(self.on_file_found)
        self.finished_searching_event = myEvent()
        self.finished_searching_event.registerCallback(self.on_finished_searching)

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
        self.checkbox_frame.grid_columnconfigure(0, weight=1)
        self.checkbox_frame.grid_columnconfigure(1, weight=1)
        self.checkbox_frame.grid_columnconfigure(2, weight=1)
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
                                                                              text=_("Custom location"),
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
                                                         text=_("Fetch logs"), image=fetch_logs_image
                                                         )

        self.fetch_logs_button.grid(row=1, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="ew")

        # Create a progressbar that gets shown when fetching logs
        self.progressbar = customtkinter.CTkProgressBar(master=self, mode="indeterminate", indeterminate_speed=1.15)
        self.progressbar.grid(row=4, column=0, pady=20, padx=20, sticky="ew")
        self.progressbar.grid_remove()

        # Button that opens a folder with report
        self.open_report_button = customtkinter.CTkButton(self,
                                                          command=self.open_report_folder,
                                                          text_color=("#eee", "#ccc"),
                                                          text=_("Open report"),
                                                          image=open_report_image)
        self.open_report_button.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        # Hide the button until logs are fetched
        self.open_report_button.grid_remove()

    def find_files(self, search_path: str, filename: str = "*.trace"):
        """A function that searches for files in a given path and returns a list of paths to found files

        :param search_path: path to the search location
        :param filename: filename to check when searching for files
        """

        self.textbox.insert("insert",
                            '---- {}: \n\n{}\n\n{}! ----\n\n\n'.format(_('Searching for files in'), search_path,
                                                                       _('it may take a while'))
                            )

        # Walking top-down from the root
        number_of_found_files = 0
        for root, dir, files in os.walk(search_path):
            if stop_searching:
                break
            # If prevents from searching in the REPORTS folder and AnyGrabber folder
            # It prevents the app from recursively searching for files and logs inside itself
            if "AnyGrabber" in dir:
                del dir[dir.index("AnyGrabber")]
            elif "REPORTS" in dir:
                del dir[dir.index("REPORTS")]
            else:
                for file in files:
                    if stop_searching:
                        break
                    if fnmatch.fnmatch(file, filename):
                        message_queue.append(os.path.join(root, file))
                        self.found_file_event.call()
                        number_of_found_files += 1

        # Display a message if no files were found in search location
        # Generate a report with a message if no files were found in search location
        if number_of_found_files == 0:
            self.open_report_button.grid()
            self.textbox.insert("insert", '\n---- {} {}! ----\n\n'.format(_('No files were found in'), search_path))
            with open(os.path.join(report_folder_path, "report.txt"), "a") as report_file:
                report_file.write('---- {} {} ----\n\n'.format(_('No files were found in'), search_path))

        self.worker_threads_finished.set(self.worker_threads_finished.get() + 1)
        if self.worker_threads_finished.get() == self.worker_threads_started.get() or stop_searching:
            self.finished_searching_event.call()

    def fetch_logs_button_callback(self):
        """A callback function that calls functions that print output generated by log fetching functions to textbox
        when appropriate switch is selected"""

        # Clears texbox contents after it gets invoked, and disables textbox editing after fetching data
        self.worker_threads_started.set(0)
        self.worker_threads_finished.set(0)
        global write_header
        write_header = True
        # This flag is set to true when stop button is pressed
        # on subsequent searches it should be set to false in order to allow seaching again
        global stop_searching
        stop_searching = False

        # Run a thread for each switch that is turned on
        # Threads are used to prevent the GUI from freezing
        threads = []
        if self.switch_fetch_appdata_logs.get():
            t1 = threading.Thread(target=self.find_files, args=[app_data_path],
                                  daemon=True)
            threads.append(t1)
            self.worker_threads_started.set(self.worker_threads_started.get() + 1)
        if self.switch_fetch_programdata_logs.get():
            t2 = threading.Thread(target=self.find_files,
                                  args=[program_data_path],
                                  daemon=True)
            threads.append(t2)
            self.worker_threads_started.set(self.worker_threads_started.get() + 1)
        if self.checkbox_search_for_logs_in_location.get():
            search_location = customtkinter.filedialog.askdirectory()
            t3 = threading.Thread(target=self.find_files, args=[search_location],
                                  daemon=True)
            threads.append(t3)
            self.worker_threads_started.set(self.worker_threads_started.get() + 1)

        if threads:
            self.textbox.configure(state="normal")
            self.textbox.delete("0.0", "end")

            # Disable buttons and checkboxes while searching for files
            self.switch_checkboxes_and_buttons_state([
                self.checkbox_fetch_appdata_logs,
                self.checkbox_fetch_programdata_logs,
                self.checkbox_search_for_logs_in_location
            ], state="disabled")

            self.open_report_button.grid_remove()

            # Update fetch button to allow stopping of search
            # When search is in progress
            self.fetch_logs_button.configure(text=_("Stop fetching"), command=self.stop_threads,
                                             fg_color=("#f59e0b", "#d97706"),
                                             hover_color=("#d97706", "#b45309"), text_color="#fff")

            self.progressbar.grid()
            self.progressbar.start()

            # Create a timestamped directory for storing logs and reports
            global report_folder_path
            report_folder_path = create_timestamped_directory()

            # Start threads
            for x in threads:
                x.start()
        else:
            play_message_beep()
            CTkMessagebox(title=_("Select option"), message=_("Please select at least one option."), option_focus=1)

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

    def on_file_found(self):
        """A function that
        1. Creates folders from a path to a file if it not already exists
        2. Copies a file to a destination folder
        3. Generates a checksum for a file
        4. Prints logs to textbox
        5. Generates a report in txt and csv format
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

    def stop_threads(self):
        """A function that stops all threads and clears message queue, calls on_finished_searching function"""
        global stop_searching
        stop_searching = True
        message_queue.clear()

    def on_finished_searching(self):
        """A function that is called when all threads are finished, it stops and removes progressbar
        and enables all checkboxes and buttons previously disabled.
        It also sets flag that list of reports needs to be refreshed"""

        # Stop progressbar and destroy it after search is finished
        self.progressbar.stop()
        self.progressbar.grid_remove()

        # Update fetch button to allow fetching of logs
        # After search finishes
        self.fetch_logs_button.configure(self,
                                         command=self.fetch_logs_button_callback,
                                         fg_color=("#3B8ED0", "#1F6AA5"),
                                         hover_color=("#36719F", "#144870"),
                                         text_color=("#eee", "#ccc"),
                                         text=_("Fetch logs"),
                                         image=fetch_logs_image
                                         )

        self.open_report_button.grid()
        if stop_searching:
            self.textbox.insert("insert", '\n---- {}! ----\n\n'.format(_('Search stopped')))
        else:
            self.textbox.insert("insert", '---- {}! ----'.format(_('Searching for files finished')))

        # Enable buttons and checkboxes after search is finished
        self.switch_checkboxes_and_buttons_state([
            self.checkbox_fetch_appdata_logs,
            self.checkbox_fetch_programdata_logs,
            self.checkbox_search_for_logs_in_location
        ], state="normal")

        global_state.refresh_reports_list = True
        play_message_beep()

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
    def switch_checkboxes_and_buttons_state(
            checkboxes_and_buttons_list: list[customtkinter.CTkCheckBox | customtkinter.CTkButton],
            state: Literal["normal", "disabled"]):
        """A function that enables or disables checkboxes and buttons passed as a parameter


        :param checkboxes_and_buttons_list: a list of checkboxes and buttons that should be enabled or disabled
        :param state: state to set
        """
        for checkbox_or_button in checkboxes_and_buttons_list:
            checkbox_or_button.configure(state=state)

    @staticmethod
    def open_report_folder():
        """A function that opens the folder where the report file is located"""
        try:
            os.startfile(report_folder_path)
        except FileNotFoundError:
            play_message_beep()
            CTkMessagebox(title=_("Report folder not found!"), message=_("Report folder not found!"), option_focus=1)

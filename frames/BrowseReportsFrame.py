import os
import customtkinter
from typing import Literal
import csv
from utils.file_operations import split_filename


def get_reports_folder_list():
    try:
        return os.listdir(os.path.join(os.getcwd(), "reports"))
    except FileNotFoundError:
        os.mkdir(os.path.join(os.getcwd(), "reports"))
        return os.listdir(os.path.join(os.getcwd(), "reports"))


def refresh(self):
    for widget in self.winfo_children():
        widget.destroy()
    d = {}
    for report in get_reports_folder_list():
        d[report] = Report_Frame(self, report_name=report,
                                 report_path=os.path.join(os.getcwd(), "reports", report))
    self.label = customtkinter.CTkLabel(self, text="Reports List",
                                        text_color=("#333", "#ccc"),
                                        font=customtkinter.CTkFont(size=15, weight="bold"))
    self.label.grid(row=0, column=0, padx=20)
    add_widgets(d, rowstart=1, columnstart=0, orientation="vertical")


def get_report_details(report_path):
    number_of_rows = 0
    found_files = set()
    try:
        with open(os.path.join(report_path, 'report.csv'), 'r') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if not row[0] == "No Anydesk logs found!":
                    number_of_rows += 1
                found_files.add(row[2])
    except FileNotFoundError:
        pass

    return {"number_of_rows": number_of_rows, "number_of_files": len(found_files)}


class Report_Frame(customtkinter.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master)
        self.report_name = kwargs.get("report_name")
        self.report_path = kwargs.get("report_path")
        report_name_details = split_filename(self.report_name)
        report_details = get_report_details(report_path=self.report_path)
        self.grid_columnconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(self, text=report_name_details["date"] + " - " +
                                                       report_name_details["time"] + " - " + report_name_details[
                                                           "computer_name"],
                                            text_color=("#333", "#ccc")
                                            )
        self.label.grid(row=0, column=0, sticky="ew", padx=20, pady=[10, 0])
        self.label2 = customtkinter.CTkLabel(self, text="Files: " + str(report_details["number_of_files"]) + " - " +
                                                        "IP Addresses: " + str(report_details["number_of_rows"]),
                                             text_color=("#333", "#ccc")
                                             )
        self.label2.grid(row=0, column=1, sticky="ew", padx=20, pady=[10, 0])

        self.report_button = Report_Button(self, report_name=self.report_name,
                                           report_path=os.path.join(os.getcwd(), "reports", self.report_path))


class Report_Button(customtkinter.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(master)

        self.report_name = kwargs.get("report_name")
        self.report_path = kwargs.get("report_path")

        self.configure(text='Open Report', command=self.open_report, fg_color=("gray75", "gray25"), text_color=(
            "#333", "#ccc"), hover_color=("#6ca9d4", "#1c3b50"))
        self.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=10)

    def open_report(self):
        os.startfile(self.report_path)


def add_widgets(d, rowstart: int = 0, columnstart: int = 0, orientation: Literal["vertical", "horizontal"] =
"vertical"):
    for i, (key, value) in enumerate(d.items()):
        if orientation == "vertical":
            value.grid(row=rowstart + i, column=columnstart, sticky="ew", padx=20, pady=10)
        elif orientation == "horizontal":
            value.grid(row=rowstart + i, column=columnstart + i, sticky="ew", padx=20, pady=10)


class Reports_List(customtkinter.CTkScrollableFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.configure(fg_color="transparent")
        # add widgets onto the frame...
        refresh(self)


class BrowseReportsFrame(customtkinter.CTkFrame):
    """Browse Reports frame class."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.navigation_panel = Reports_List(self)

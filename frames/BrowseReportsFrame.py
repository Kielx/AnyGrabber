import os
import customtkinter
from typing import Literal


def get_reports_folder_list():
    try:
        return os.listdir(os.path.join(os.getcwd(), "reports"))
    except FileNotFoundError:
        os.mkdir(os.path.join(os.getcwd(), "reports"))
        return os.listdir(os.path.join(os.getcwd(), "reports"))


def refresh(navigation_panel):
    for widget in navigation_panel.winfo_children():
        widget.destroy()
    d = {}
    for report in get_reports_folder_list():
        d[report] = Report_Button(navigation_panel, report_name=report,
                                  report_path=os.path.join(os.getcwd(), "reports", report))

    navigation_panel.label = customtkinter.CTkLabel(navigation_panel, text="Reports List",
                                                    text_color=("#333", "#ccc"),
                                                    font=customtkinter.CTkFont(size=15, weight="bold"))
    navigation_panel.label.grid(row=0, column=0, padx=20)
    add_widgets(d, rowstart=1, columnstart=0, orientation="vertical")


class Report_Button(customtkinter.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(master)

        self.report_name = kwargs.get("report_name")
        self.report_path = kwargs.get("report_path")

        self.configure(text=self.report_name, command=self.open_report)

    def open_report(self):
        os.startfile(self.report_path)


def add_widgets(d, rowstart: int = 0, columnstart: int = 0, orientation: Literal["vertical", "horizontal"] =
"vertical"):
    for i, (key, value) in enumerate(d.items()):
        if orientation == "vertical":
            value.grid(row=rowstart + i, column=columnstart, sticky="ew", padx=20, pady=10)
        elif orientation == "horizontal":
            value.grid(row=rowstart + i, column=columnstart + i, sticky="ew", padx=20, pady=10)


class Navigation_Panel(customtkinter.CTkScrollableFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        # add widgets onto the frame...
        refresh(self)


class BrowseReportsFrame(customtkinter.CTkFrame):
    """Browse Reports frame class."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.navigation_panel = Navigation_Panel(self)

        self.refresh_button = customtkinter.CTkButton(self, text="Refresh",
                                                      command=lambda: refresh(self.navigation_panel))
        self.refresh_button.grid(row=1, column=0, sticky="ew", padx=20, pady=10)

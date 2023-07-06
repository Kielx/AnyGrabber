import csv
import os
from CTkMessagebox import CTkMessagebox
import customtkinter
from PIL import Image

from utils.file_operations import split_computer_datetime_dirname, get_reports_folder_list
from utils.widget_utils import add_widgets
from utils.locale_utils import _


class BrowseReportsFrame(customtkinter.CTkScrollableFrame):
    """Browse Reports frame class holding the list of generated reports."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.configure(fg_color="transparent")
        # add widgets onto the frame...
        refresh(self)


class Report_Frame(customtkinter.CTkFrame):
    """A class representing a single report in the list of reports.
    It shows the date, time and computer name of the report.
    It also shows the number of files and IP addresses found in the report.
    Button located in frame opens the report folder.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master)
        self.report_name = kwargs.get("report_name")
        self.report_path = kwargs.get("report_path")

        # Images for buttons
        image_path = os.path.join(os.getcwd(), "assets")
        self.open_report_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "open_report_light.png")),
            dark_image=Image.open(os.path.join(image_path, "open_report_dark.png")),
            size=(20, 20))
        self.delete_report_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "delete_report_light.png")),
            dark_image=Image.open(os.path.join(image_path, "delete_report_dark.png")),
            size=(20, 20))

        report_name_details = split_computer_datetime_dirname(self.report_name)
        report_details = get_report_file_and_ip_numbers(report_path=self.report_path)
        self.grid_columnconfigure(0, weight=1)

        if report_name_details:
            self.label = customtkinter.CTkLabel(self, text=report_name_details["date"] + " - " +
                                                           report_name_details["time"] + " - " + report_name_details[
                                                               "computer_name"],
                                                text_color=("#333", "#ccc")
                                                )
        else:
            self.label = customtkinter.CTkLabel(self, text=self.report_name,
                                                text_color=("#333", "#ccc")
                                                )
        self.label.grid(row=0, column=0, sticky="ew", padx=20, pady=[10, 0])
        self.label2 = customtkinter.CTkLabel(self, text=_("Files: ") + str(report_details["number_of_files"]) + " - " +
                                                        _("IP Addresses: ") + str(
            report_details["number_of_ip_addresses"]),
                                             text_color=("#333", "#ccc")
                                             )
        self.label2.grid(row=0, column=1, sticky="ew", padx=20, pady=[10, 0])

        self.report_button = Report_Button(self, report_name=self.report_name,
                                           report_path=os.path.join(os.getcwd(), "REPORTS", self.report_path))
        self.delete_report_button = Delete_Report_Button(master=self, report_name=self.report_name,
                                                         report_path=os.path.join(os.getcwd(), "REPORTS",
                                                                                  self.report_path))


class Report_Button(customtkinter.CTkButton):
    """A class representing a button that opens the report folder."""

    def __init__(self, master, **kwargs):
        super().__init__(master)

        self.report_name = kwargs.get("report_name")
        self.report_path = kwargs.get("report_path")

        self.configure(text=_('Open Report folder'), command=self.open_report, text_color=(
            "#eee", "#ccc"),
                       image=self.master.open_report_image)
        self.grid(row=1, column=0, columnspan=1, sticky="ew", padx=10, pady=10)

    def open_report(self):
        os.startfile(self.report_path)


class Delete_Report_Button(customtkinter.CTkButton):
    """A class representing a button that deletes the report folder."""

    def __init__(self, master, **kwargs):
        super().__init__(master)

        self.report_name = kwargs.get("report_name")
        self.report_path = kwargs.get("report_path")

        self.configure(text=_('Delete Report'), command=self.confirm_delete, text_color=("#eee", "#ccc"),
                       fg_color=("#ef4444", "#b91c1c"),
                       hover_color=("#dc2626", "#991b1b"),
                       image=self.master.delete_report_image)
        self.grid(row=1, column=1, columnspan=1, sticky="ew", padx=10, pady=10)

    def confirm_delete(self):
        # get yes/no answers
        msg = CTkMessagebox(title=_('Delete Report' + "?"),
                            message=_('Do you really want to delete the selected report?'),
                            icon="warning", option_1=_('Cancel'), option_2=_('Delete'), cancel_button="cross")
        msg.button_2.configure(text_color="#eee", fg_color=("#ef4444", "#b91c1c"),
                               hover_color=("#dc2626", "#991b1b"))
        response = msg.get()

        if response == _('Delete'):
            Delete_Report_Button.delete_report(self)
        else:
            pass

    def delete_report(self):
        import shutil
        shutil.rmtree(self.report_path)
        # refresh browse reports frame
        refresh(self.master.master)


def refresh(browse_reports_frame_instance: customtkinter.CTkScrollableFrame):
    """Function that refreshes the browse reports frame.
    It deletes all widgets from the frame and adds new widgets.
    It is used when new report is created so that the list of reports is updated.

    :param browse_reports_frame_instance: browse reports frame instance that will be refreshed with new data
    """
    # delete all widgets from frame
    for widget in browse_reports_frame_instance.winfo_children():
        widget.destroy()

    reports_list = {}
    # Get new list of reports and add dict entries representing a pair of: name of report and a frame with report
    # details
    for report in get_reports_folder_list():
        reports_list[report] = Report_Frame(browse_reports_frame_instance, report_name=report,
                                            report_path=os.path.join(os.getcwd(), "REPORTS", report))

    # Add a top label to the list of reports
    browse_reports_frame_instance.label = customtkinter.CTkLabel(browse_reports_frame_instance, text=_("Reports List"),
                                                                 text_color=("#333", "#ccc"),
                                                                 font=customtkinter.CTkFont(size=15, weight="bold"))
    browse_reports_frame_instance.label.grid(row=0, column=0, padx=20)
    # Add all reports to the frame
    add_widgets(reports_list, rowstart=1, columnstart=0, orientation="vertical")


def get_report_file_and_ip_numbers(report_path):
    """Function that returns the number of files and IP addresses found in the report by analyzing the report.csv file.

    :param report_path: path to the report folder
    :return: dict with number of files and IP addresses found in the report
    """

    number_of_ip_addresses = 0
    found_files = set()
    try:
        with open(os.path.join(report_path, 'report.csv'), 'r') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if not row[0] == "No Anydesk logs found!":
                    number_of_ip_addresses += 1
                found_files.add(row[2])
    except FileNotFoundError:
        pass

    return {"number_of_ip_addresses": number_of_ip_addresses, "number_of_files": len(found_files)}

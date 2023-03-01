import tkinter
import os
import customtkinter
from utils.file_operations import get_anydesk_logs
from PIL import Image

app_data_path = os.getenv('APPDATA')
app_data_filename = f'{app_data_path}/AnyDesk/ad.trace'
program_data_path = os.getenv('PROGRAMDATA')
program_data_filename = f'{program_data_path}/AnyDesk/ad_svc.trace'


def change_appearance_mode_event(new_appearance_mode):
    customtkinter.set_appearance_mode(new_appearance_mode)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")),
                                                 size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")),
                                                       size=(500, 150))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")),
                                                 size=(20, 20))
        self.anydesk_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "anydesk_light.png")),
            dark_image=Image.open(os.path.join(image_path, "anydesk_dark.png")),
            size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  AnyGrabber",
                                                             image=self.logo_image,
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                                   text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="AnyDesk",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.anydesk_image, anchor="w",
                                                      command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame,
                                                                values=["Light", "Dark", "System"],
                                                                command=change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="",
                                                                   image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        # create second frame
        self.anydesk_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.anydesk_frame.grid_columnconfigure(0, weight=1)
        self.anydesk_frame.grid_rowconfigure(0, weight=1)

        # create checkbox and switch frame
        self.checkbox_var = tkinter.BooleanVar()
        self.checkbox_var2 = tkinter.BooleanVar()

        self.checkbox_slider_frame = customtkinter.CTkFrame(master=self.anydesk_frame)
        self.checkbox_slider_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, variable=self.checkbox_var,
                                                    onvalue=True, offvalue=False)
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, variable=self.checkbox_var2,
                                                    onvalue=True, offvalue=False)
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")

        self.button = customtkinter.CTkButton(self.anydesk_frame, command=self.button_callback,
                                              text="Fetch logs")

        self.button.grid(row=1, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="ew")

        self.textbox = customtkinter.CTkTextbox(self.anydesk_frame)
        self.textbox.grid(row=2, column=0, padx=20, pady=20, sticky='nsew')

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.anydesk_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.anydesk_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

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


if __name__ == "__main__":
    app = App()
    app.mainloop()

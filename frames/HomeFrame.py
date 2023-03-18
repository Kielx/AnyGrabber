import customtkinter
import os
from PIL import Image

# load images with light and dark mode image
image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../assets")

home_screen_description = "Welcome to AnyGrabber - the program designed to help you extract, secure and " \
                          "present AnyDesk logs from system with ease. \n\n" \
                          "Whether you're dealing with cases of fraud or just need to keep track of AnyDesk " \
                          "activity on your computer, AnyGrabber provides" \
                          " a simple and intuitive solution for all your logging needs.\n\n" \
                          "To get started, simply select the AnyDesk option from the main menu. Then pick default " \
                          "locations for your AnyDesk logs, or select the 'Browse' option to specify a custom " \
                          "location. \n\n" \
                          "AnyGrabber will automatically search your system for AnyDesk" \
                          " logs and extract date, time and IP address of each session. \n\n"


class HomeFrame(customtkinter.CTkFrame):
    """Home frame class."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.any_grabber_logo = customtkinter.CTkImage(Image.open(os.path.join(image_path, "AnyGrabberLogo.png")),
                                                       size=(200, 144))

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.home_frame_large_image_label = customtkinter.CTkLabel(self, text="",
                                                                   image=self.any_grabber_logo)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.textbox = customtkinter.CTkTextbox(master=self, width=200, corner_radius=0, wrap="word")
        self.textbox.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.textbox.insert("0.0", home_screen_description)
        self.textbox.configure(state="disabled", fg_color='transparent', text_color=("#333", "#ccc"))

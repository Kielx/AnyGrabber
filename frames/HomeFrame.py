import customtkinter
import os
from PIL import Image
from utils.locale_utils import _

# load images with light and dark mode image
image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../assets")


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
        self.textbox.insert("0.0", _("welcome screen\n"))
        self.textbox.configure(state="disabled", fg_color='transparent', text_color=("#333", "#ccc"))

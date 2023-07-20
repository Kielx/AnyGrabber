import os
import customtkinter
from CTkMessagebox import CTkMessagebox
from PIL import Image

from frames.AnydeskFrame import AnydeskFrame
from frames.BrowseReportsFrame import BrowseReportsFrame, refresh
from frames.HomeFrame import HomeFrame
from utils.locale_utils import _, default_locale, language_mappings, appearance_mode_mappings
from utils.config_utils import update_config, get_config_parameter_value
from utils.sound_utils import play_message_beep
import global_state


def change_appearance_mode_event(new_appearance_mode):
    """Change appearance mode event handler for appearance mode menu.
    @param new_appearance_mode: new appearance mode - human-readable value with translation from appearance mode menu list.

    This function is called when user changes appearance mode in appearance mode menu.
    Appearance modes in menu are presented as a set of options that user can choose from,
    they are human readable and translated to user's language. Therefore they need to be converted
    to their internal representation (light, dark, system) before they can be used.
    For that purpose we use bidirectional dictionary (bidict) that maps human readable values to internal values that are stored in locale_utils..
    """
    customtkinter.set_appearance_mode(appearance_mode_mappings.inverse[new_appearance_mode])
    update_config("appearance_mode", appearance_mode_mappings.inverse[new_appearance_mode])


def change_language_event(new_language):
    """Change appearance mode event handler for appearance mode menu.
    @param new_language: new language - human-readable value with translation from language menu list.

    This function is called when user changes language mode in language mode menu.
    Languages in menu are presented as a set of options that user can choose from,
    they are human-readable and translated to user's language. Therefore, they need to be converted
    to their internal representation (pl-PL, en-US and so on) before they can be used.
    For that purpose we use bidirectional dictionary (bidict) that maps human-readable values to internal values that are stored in locale_utils.
    """
    update_config("locale", language_mappings.inverse[new_language])
    # Display message that restart is required to apply changes only if default locale is changed.
    if language_mappings.inverse[new_language] != default_locale:
        play_message_beep()
        CTkMessagebox(title=_("Restart required"), message=_("Please restart the application to apply changes."),
                      option_focus=1)


class App(customtkinter.CTk):
    """Main application class."""

    def __init__(self):
        super().__init__()
        self.appearance_mode_variable = customtkinter.StringVar(
            value=appearance_mode_mappings[get_config_parameter_value("appearance_mode")])
        customtkinter.set_appearance_mode(get_config_parameter_value("appearance_mode"))
        self.geometry("720x520+0+0")
        self.title("AnyGrabber")
        self.iconbitmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "AnyGrabberIcon.ico"))

        self.minsize(750, 450)

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")

        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "AnyGrabberLogo.png")),
                                                 size=(52, 38))

        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")),
                                                 size=(20, 20))
        self.anydesk_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "anydesk_light.png")),
            dark_image=Image.open(os.path.join(image_path, "anydesk_dark.png")),
            size=(20, 20))

        self.browse_reports_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "browse_reports_light.png")),
            dark_image=Image.open(os.path.join(image_path, "browse_reports_dark.png")),
            size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text_color=("#333", "#ccc"),
                                                             text=" AnyGrabber",
                                                             image=self.logo_image,
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                                   text=_("Home"),
                                                   fg_color="transparent", text_color=("#333", "#ccc"),
                                                   hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="AnyDesk",
                                                      fg_color="transparent", text_color=("#333", "#ccc"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.anydesk_image, anchor="w",
                                                      command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.browse_reports_frame_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                                   border_spacing=10, text=_("Browse Reports"),
                                                                   fg_color="transparent", text_color=("#333", "#ccc"),
                                                                   hover_color=("gray70", "gray30"),
                                                                   image=self.browse_reports_image, anchor="w",
                                                                   command=self.browse_reports_frame_button_event)
        self.browse_reports_frame_button.grid(row=5, column=0, sticky="ew")

        self.appearance_mode_label = customtkinter.CTkLabel(self.navigation_frame, text_color=("#333", "#ccc"),
                                                            text=_("Theme"))
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=[5, 0], sticky="n")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame,
                                                                text_color=("#eee", "#ccc"),
                                                                values=[appearance for appearance in
                                                                        appearance_mode_mappings.values()],
                                                                command=change_appearance_mode_event,
                                                                variable=self.appearance_mode_variable)
        self.appearance_mode_menu.grid(row=7, column=0, padx=20, pady=[0, 10], sticky="s")

        self.lanuage_label = customtkinter.CTkLabel(self.navigation_frame, text_color=("#333", "#ccc"),
                                                    text=_("Language"))
        self.lanuage_label.grid(row=8, column=0, padx=20, pady=0, sticky="n")

        self.language_menu = customtkinter.CTkOptionMenu(self.navigation_frame,
                                                         text_color=("#eee", "#ccc"),
                                                         values=[lang for lang in language_mappings.values()],
                                                         command=change_language_event)
        self.language_menu.grid(row=9, column=0, padx=20, pady=[0, 20], sticky="s")

        self.language_menu.set(language_mappings[default_locale])

        # create home frame
        self.home_frame = HomeFrame(self, corner_radius=0, fg_color="transparent")

        # create anydesk frame
        self.anydesk_frame = AnydeskFrame(self, corner_radius=0, fg_color="transparent")

        # create browse reports frame
        self.browse_reports_frame = BrowseReportsFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        """Function that highlights selected button and shows selected frame."""

        # Define the mappings between name and button/frame
        frame_mappings = {
            "home": (self.home_button, self.home_frame),
            "anydesk_frame": (self.frame_2_button, self.anydesk_frame),
            "browse_reports_frame": (self.browse_reports_frame_button, self.browse_reports_frame)
        }

        # Iterate over the mappings and update button colors
        for frame_name, (button, frame) in frame_mappings.items():
            button.configure(fg_color=("gray75", "gray25") if name == frame_name else "transparent")

        # Iterate over the mappings and show/hide frames
        for frame_name, (_, frame) in frame_mappings.items():
            if name == frame_name:
                frame.grid(row=0, column=1, sticky="nsew")
            else:
                frame.grid_forget()

    def home_button_event(self):
        """Home button event handler."""
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        """Frame 2 button event handler."""
        self.select_frame_by_name("anydesk_frame")

    def browse_reports_frame_button_event(self):
        """Browse Reports button event handler."""
        self.select_frame_by_name("browse_reports_frame")
        if global_state.refresh_reports_list:
            refresh(browse_reports_frame_instance=self.browse_reports_frame)
            global_state.refresh_reports_list = False


if __name__ == "__main__":
    app = App()
    app.mainloop()

import os
import customtkinter
from PIL import Image

from frames.AnydeskFrame import AnydeskFrame
from frames.HomeFrame import HomeFrame

customtkinter.set_appearance_mode("System")


def change_appearance_mode_event(new_appearance_mode):
    """Change appearance mode event handler for appearance mode menu."""
    customtkinter.set_appearance_mode(new_appearance_mode)


class App(customtkinter.CTk):
    """Main application class."""

    def __init__(self):
        super().__init__()

        self.geometry("720x450+0+0")
        self.title("AnyGrabber - Grabber for AnyDesk logs")
        self.minsize(720, 450)

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")

        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")),
                                                 size=(26, 26))

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
        self.appearance_mode_menu.set("System")

        # create home frame
        self.home_frame = HomeFrame(self, corner_radius=0, fg_color="transparent")

        # create anydesk frame
        self.anydesk_frame = AnydeskFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        """Function that highlights selected button and shows selected frame."""
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "anydesk_frame" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "anydesk_frame":
            self.anydesk_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.anydesk_frame.grid_forget()

    def home_button_event(self):
        """Home button event handler."""
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        """Frame 2 button event handler."""
        self.select_frame_by_name("anydesk_frame")


if __name__ == "__main__":
    app = App()
    app.mainloop()

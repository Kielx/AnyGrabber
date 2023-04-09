import customtkinter


class BrowseReportsFrame(customtkinter.CTkFrame):
    """Home frame class."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

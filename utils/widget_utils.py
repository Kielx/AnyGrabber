from typing import Literal


def add_widgets(widget_dict, rowstart: int = 0, columnstart: int = 0, orientation: Literal["vertical", "horizontal"] =
"vertical"):
    """ A function that adds widgets to a frame.
    :param widget_dict: A dictionary containing the widgets to be added.
    :param rowstart: The row number where the widgets will be added.
    :param columnstart: The column number where the widgets will be added.
    :param orientation: The orientation of the widgets. "vertical" or "horizontal".
    """

    for i, (key, value) in enumerate(widget_dict.items()):
        if orientation == "vertical":
            value.grid(row=rowstart + i, column=columnstart, sticky="ew", padx=20, pady=10)
        elif orientation == "horizontal":
            value.grid(row=rowstart + i, column=columnstart + i, sticky="ew", padx=20, pady=10)

from typing import Literal


def add_widgets(d, rowstart: int = 0, columnstart: int = 0, orientation: Literal["vertical", "horizontal"] =
"vertical"):
    for i, (key, value) in enumerate(d.items()):
        if orientation == "vertical":
            value.grid(row=rowstart + i, column=columnstart, sticky="ew", padx=20, pady=10)
        elif orientation == "horizontal":
            value.grid(row=rowstart + i, column=columnstart + i, sticky="ew", padx=20, pady=10)

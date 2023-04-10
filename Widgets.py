from typing import Literal

from DesignSettings import DesignSettings
import tkinter as tk


class DeckText(tk.Text):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg=DesignSettings.BG_COLOR,
                       fg=DesignSettings.FG_COLOR,
                       font=("Courier", 12),
                       wrap="word")


class Button(tk.Button):
    def __init__(self, master, text, command, state: Literal["normal", "active", "disabled"] = "normal", width=10):
        super().__init__(master, text=text, command=command, state=state, width=width)
        self.configure(
            bg=DesignSettings.BUTTON_BG_COLOR_INACTIVE,
            fg=DesignSettings.BUTTON_FG_COLOR_INACTIVE,
            activebackground=DesignSettings.BUTTON_BG_COLOR_ACTIVE,
            activeforeground=DesignSettings.BUTTON_FG_COLOR_ACTIVE,
            disabledforeground=DesignSettings.BUTTON_FG_COLOR_DISABLED,
            font=DesignSettings.SMALL_FONT, width=width
        )


class Label(tk.Label):
    def __init__(self, master, text, **kwargs):
        super().__init__(master, text=text, **kwargs)
        self.configure(bg=DesignSettings.BG_COLOR,
                       fg=DesignSettings.FG_COLOR,
                       font=DesignSettings.FONT)

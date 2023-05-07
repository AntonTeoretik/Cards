from tkinter import font
from typing import Literal

from DesignSettings import DesignSettings
import tkinter as tk


class DeckText(tk.Text):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg=DesignSettings.BG_COLOR,
                       fg=DesignSettings.FG_COLOR,
                       # state="disabled",
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

    def adjust_font_size(self):
        label = self
        label_font = font.Font(font=label['font'])
        text_size = label_font.measure("a" + label['text'] + "a")

        if text_size > label.winfo_width():
            print(label.winfo_width())

            new_font_size = label_font['size'] * label.winfo_width() // text_size

            new_font = (label_font['family'], new_font_size, label_font['weight'])
            label.configure(font=new_font)

    def reset_font_size(self):
        self.configure(font=DesignSettings.FONT)

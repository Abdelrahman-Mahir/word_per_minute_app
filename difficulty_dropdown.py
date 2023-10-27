# Import module
from tkinter import *
import tkinter.ttk as ttk


class DifficultDropDown(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dropdown menu options
        self.options = [
            "Easy😪",
            "Medium😲",
            "Hard🥶",
            "Hell😈",
        ]
        # datatype of menu text
        self.clicked = StringVar()

        # initial menu text
        self.clicked.set("Easy😪")
        self.drop = ttk.Combobox(self, textvariable=self.clicked, values=self.options)
        self.drop.grid(row=1,column=3)






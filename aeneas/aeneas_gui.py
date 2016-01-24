import tkinter as tk
from collections import OrderedDict

class Aeneas_Holder(tk.Tk):
    WIDTH = 300
    HEIGHT = 300

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.GUI = tk.Frame(width = self.WIDTH, height = self.HEIGHT)
        self.GUI.pack(side = "top", fill = "both", expand = True)



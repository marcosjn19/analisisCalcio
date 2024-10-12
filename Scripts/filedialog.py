import tkinter as tk
from tkinter import filedialog as fd

class filedialog(tk.Tk):
    @classmethod
    def askopenfilename(cls, *args, **kwargs):
        root = cls()
        root.wm_withdraw()
        files = fd.askopenfilename(*args, **kwargs)
        root.destroy()
        return files
import tkinter as form
from tkinter import ttk
from globalData import STRGS
#=========================================================================================
class GuiMatrixInput(form.Toplevel):
    """Here user provide all data to the matrix """

    def __init__(self, master, mach, itin):
        form.Toplevel.__init__(self, master)

        self.title("Enter input data")
        self.resizable(True, True)
        #TODO: return focus on destroy to main frame...
import tkinter as form
from tkinter import ttk
from globalData import STRGS
#=========================================================================================
class GuiMain(form.Frame):
    """ Main form to manage all the program and options """

    def __init__(self, master):
        form.Frame.__init__(self, master)

        master.title(STRGS['TITLE_PROGRAM'])
        #center window in the middle of the screen
        master.geometry("%dx%d+%d+%d" % (400,400, int(master.winfo_screenwidth() / 2 - 400 / 2), int(master.winfo_screenheight() / 2 - 400 / 2)))
        master.resizable(False, False)

        #first label frame
        frMachines = ttk.LabelFrame(master, text=STRGS['MACHS'])
        frMachines.grid(column = 0, row =0, padx=5, pady=5)
    #TODO: here will be main gui to control everything
import tkinter as form
from tkinter import ttk
#=========================================================================================
class GuiTaskNew(form.Toplevel):
    """Form for adding new Task in itinerary"""

    def __init__(self, master):
        form.Toplevel.__init__(self, master)

        self.title("New task in itinerary")
        self.geometry("%dx%d+%d+%d" % (200,150, int(self.winfo_screenwidth() / 2 - 200 / 2), int(self.winfo_screenheight() / 2 - 150 / 2)))
        self.resizable(False, False)

        frTaskNew = ttk.LabelFrame(self, text="New task")
        frTaskNew.grid(column=0, row=0, padx=5, pady=5)

        ttk.Label(frTaskNew, text="Name").grid(column=0, row=0, padx=3, pady=3, sticky=form.W)
        ttk.Label(frTaskNew, text="Duration").grid(column=0, row=1, padx=3, pady=3, sticky=form.W)
        ttk.Label(frTaskNew, text="Machine").grid(column=0, row=2, padx=3, pady=3, sticky=form.W)

        self.taskName = form.StringVar()
        self.entTaskName = ttk.Entry(frTaskNew, textvariable=self.taskName, width=17)
        self.entTaskName.grid(column=1, row=0, padx=3, pady=3)
        self.entTaskName.focus()

        self.taskDuration = form.DoubleVar()
        self.entTaskDuration = ttk.Entry(frTaskNew, textvariable=self.taskDuration, width=17)
        self.entTaskDuration.grid(column=1, row=1, padx=3, pady=3)

        ttk.Button(self, text="Save", width=30, command=self.saveNewTask).grid(column=0, row=1, pady=5, padx=5)
        
        #set to be on top, hijack all comands and pause anything until close 
        self.transient(master)
        self.grab_set()
        master.wait_window(self)

        #TODO: checking values for correctness
        #TODO: cant create new task if no machines available


    def saveNewTask(self):
        pass
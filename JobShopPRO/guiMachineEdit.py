import tkinter as form
from tkinter import ttk
from globalData import machinesList
from clMachine import Machine
#=========================================================================================
class GuiMachineEdit(form.Toplevel):
    """Form that edit value of selected machine"""

    def __init__(self, master, Aindex):
        form.Toplevel.__init__(self, master)
        self.editedItemIndex = Aindex
        self.title("Edit " + str(machinesList[self.editedItemIndex].ID) + " machine")
        #center window in the middle of the screen
        self.geometry("%dx%d+%d+%d" % (250,100, int(self.winfo_screenwidth() / 2 - 250 / 2), int(self.winfo_screenheight() / 2 - 100 / 2)))
        self.resizable(False, False)

        frMachineEdit = ttk.LabelFrame(self, text="Edit value")
        frMachineEdit.grid(column = 0,  columnspan=2, row =0, padx=10, pady=10, sticky=form.NSEW)

        ttk.Label(frMachineEdit, text="Enter new value: ").grid(column=0, row=0, padx=3, pady=3, sticky = form.W)

        #Entry and value in it - Two keys are also binded with commands
        self.editedValue = form.StringVar()
        self.editedValue.set(machinesList[self.editedItemIndex].ID)
        self.entNewValue = ttk.Entry(frMachineEdit, textvariable=self.editedValue)
        self.entNewValue.grid(column=1, row=0, padx=3, pady=3)
        self.entNewValue.focus()
        self.entNewValue.bind('<Return>', self.closeAndSave)
        self.entNewValue.bind('<Escape>', self.closeAndCancel)

        ttk.Button(self, text="OK", width=12, command=self.closeAndSave).grid(column=0, row=1, padx=5, pady=5)
        ttk.Button(self, text="Cancel", width=12, command=self.closeAndCancel).grid(column=1, row=1, padx=5, pady=5)

        #set to be on top, hijack all comands and pause anything until close 
        self.transient(master)
        self.grab_set()
        master.wait_window(self)
        

    def closeAndSave(self, event=None):
        """close and save new value edited in machine list"""
        print("saved")
        global machinesList
        machinesList[self.editedItemIndex].ID = self.editedValue.get()
        self.destroy()    
        
    def closeAndCancel(self, event=None):
        """close and cancel editing values"""
        print("canceld")
        self.destroy()

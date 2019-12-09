import tkinter as form
from tkinter import ttk
from tkinter import messagebox as msg
from globalData import machinesList, STRGS
from clMachine import Machine
#=========================================================================================
class GuiMachineEdit(form.Toplevel):
    """Form that edit value of selected machine"""

    def __init__(self, master, aIndex):
        form.Toplevel.__init__(self, master)

        self.editedItemIndex = aIndex
        self.title(STRGS['EDIT'] + " " + str(machinesList[self.editedItemIndex].name))
        #center window in the middle of the screen
        self.geometry("%dx%d+%d+%d" % (350,130, int(self.winfo_screenwidth() / 2 - 350 / 2), int(self.winfo_screenheight() / 2 - 130 / 2)))
        self.resizable(False, False)

        frMachineEdit = ttk.LabelFrame(self, text=STRGS['EDIT'])
        frMachineEdit.grid(column = 0,  columnspan=2, row =0, padx=10, pady=10, sticky=form.NSEW)

        ttk.Label(frMachineEdit, text=STRGS['ENTER_NEW_VAL']).grid(column=0, row=0, padx=3, pady=3, sticky = form.W)

        #Entry and value in it - Two keys are also binded with commands
        self.editedValue = form.StringVar()
        self.editedValue.set(machinesList[self.editedItemIndex].name)
        self.entNewValue = ttk.Entry(frMachineEdit, textvariable=self.editedValue)
        self.entNewValue.grid(column=1, row=0, padx=3, pady=3)
        self.entNewValue.focus()
        self.entNewValue.bind('<Return>', self.closeAndSave)
        self.entNewValue.bind('<Escape>', self.closeAndCancel)

        ttk.Button(self, text=STRGS['OK'], width=12, command=self.closeAndSave).grid(column=0, row=1, padx=5, pady=5)
        ttk.Button(self, text=STRGS['CANCEL'], width=12, command=self.closeAndCancel).grid(column=1, row=1, padx=5, pady=5)

        #set to be on top, hijack all comands and pause anything until close
        self.transient(master)
        self.grab_set()
        
    def closeAndSave(self, event=None):
        """Close and save new value edited in machine list"""
        global machinesList
        for index, machObj in enumerate(machinesList):
            if machObj.name == self.editedValue.get() and self.editedItemIndex != index:        #prevent form being unable to edit the same item
                msg.showerror(STRGS['ERR_ILLEGAL'], machObj.name + STRGS['ERR_EXIST_DIFF_NAME'])
                return
        machinesList[self.editedItemIndex].name = self.editedValue.get()
        self.destroy()    
        
    def closeAndCancel(self, event=None):
        """Close and cancel editing values"""
        self.destroy()

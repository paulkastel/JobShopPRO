import tkinter as form
from tkinter import ttk
from tkinter import messagebox as msg
from clMachine import Machine
from globalData import *
import guiMachineEdit
#=========================================================================================
class GuiMachine(form.Frame):
    """Form to manage all machines"""

    def __init__(self, master):
        form.Frame.__init__(self, master)

        self.master = master
        self.master.title(STRGS['MACHS'])
        #center window in the middle of the screen
        self.master.geometry("%dx%d+%d+%d" % (590,450, int(master.winfo_screenwidth() / 2 - 590 / 2), int(master.winfo_screenheight() / 2 - 450 / 2)))
        self.master.resizable(False, False)

        #first label frame
        frMachines = ttk.LabelFrame(master, text=STRGS['MACHS'])
        frMachines.grid(column = 0, row =0, padx=8, pady=8)
        
        scrollbar = ttk.Scrollbar(frMachines)
        self.lboxMachineList = form.Listbox(frMachines, width=30, height=20, yscrollcommand=scrollbar.set, selectmode=form.SINGLE)
        self.lboxMachineList.grid(columnspan=3, column=0, row=0, padx=3, pady=3)
        global machinesList
        for mach in machinesList:
            self.lboxMachineList.insert(form.END, mach.name)
        self.lboxMachineList.bind("<ButtonRelease-1>", self.showDetailsMachine)
        scrollbar.config(command=self.lboxMachineList.yview)

        ttk.Button(frMachines, text=STRGS['ADD'], width=7, command=self.addNewMachine).grid(column =0, row=1, padx=2, pady=2)
        ttk.Button(frMachines, text=STRGS['EDIT'], width=7, command=self.editSelectedMachine).grid(column =1, row=1, padx=2, pady=2)
        ttk.Button(frMachines, text=STRGS['DELETE'], width=7, command=self.deleteSelectedMachine).grid(column =2, row=1, padx=2, pady=2)
        
        #second label frame
        frMachineDetail = ttk.LabelFrame(master, text=STRGS['MACH_DETAILS'])
        frMachineDetail.grid(column = 1, row =0, padx=5, pady=5, sticky=form.NW)

        ttk.Label(frMachineDetail, text=STRGS['NAME']).grid(column =0, row=0, padx=5, pady=5)
        self.lblProperties = ttk.Label(frMachineDetail, width=19)
        self.lblProperties.grid(column =1, row=0, padx=5, pady=5)

        ttk.Button(master, text=STRGS['OK'], width=20, command=self.saveAndClose).grid(column=1, row=0, padx=3, pady=3, sticky=form.S)

        #set this window to be on top
        self.master.grab_set()
        self.master.focus()

    def addNewMachine(self):
        """Add new machine to machine list and listbox in form"""
        newMachine = Machine("M" + str(len(self.lboxMachineList.get(0, form.END)) + 1))
        global machinesList
        machinesList.append(newMachine)
        self.lboxMachineList.insert(form.END, newMachine.name)
        self.lboxMachineList.selection_clear(0, form.END)
        self.lboxMachineList.select_set(form.END)
        self.showDetailsMachine(None)

    def showDetailsMachine(self, event):
        """Show secondary informations about choosen machine in label"""
        try:
            global machinesList
            index = self.lboxMachineList.curselection()[0]
            selectedValue = machinesList[index].name
            self.lblProperties.configure(text= selectedValue)
        except IndexError:
            self.lblProperties.configure(text="")

    def deleteSelectedMachine(self):
        """Delete selected object from machine list"""
        try:
            index = self.lboxMachineList.curselection()[0]
            global itinerariesList
            for itinObj in itinerariesList:
                for taskObj in itinObj.tasksList:
                    if taskObj.machine.name == self.lboxMachineList.get(form.ANCHOR):
                        msg.showerror(STRGS['ERR_ILLEGAL'], taskObj.machine.name + " is used in " + taskObj.name + " in " + itinObj.name + " \nand cannot be deleted")
                        return
            self.lboxMachineList.delete(index)
            global machinesList
            machinesList.pop(index)
            self.lboxMachineList.select_set(index - 1)
            self.showDetailsMachine(None)
        except IndexError:
            pass

    def editSelectedMachine(self):
        """Start gui dialog to edit details about machine"""
        try:
            global machinesList
            index = self.lboxMachineList.curselection()[0]
            global itinerariesList
            for itinObj in itinerariesList:
                for taskObj in itinObj.tasksList:
                    if taskObj.machine.name == self.lboxMachineList.get(self.lboxMachineList.curselection()):
                        msg.showwarning(STRGS['WARN'], taskObj.machine.name + STRGS['MSG_WARN_MACH_IN_USE'])
                        break
            guiMachineEdit.GuiMachineEdit(self, index).wait_window()

            #reload gui list and show updates
            self.lboxMachineList.delete(0, form.END)
            for mach in machinesList:
                self.lboxMachineList.insert(form.END, mach.name)
            
            self.lboxMachineList.selection_set(index)
            self.showDetailsMachine(self)
        except IndexError:
            pass

    def saveAndClose(self):
        """Close this window"""
        self.master.destroy()
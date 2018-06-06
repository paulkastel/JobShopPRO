import tkinter as form
from tkinter import ttk
from clMachine import Machine
from globalData import machinesList
import guiMachineEdit
#=========================================================================================
class GuiMachine(form.Frame):
    """ Form to manage all machines """

    def __init__(self, master):
        form.Frame.__init__(self, master)
       
        master.title("Machines")
        #center window in the middle of the screen
        master.geometry("%dx%d+%d+%d" % (400,400, int(master.winfo_screenwidth() / 2 - 400 / 2), int(master.winfo_screenheight() / 2 - 400 / 2)))
        master.resizable(False, False)

        #first label frame
        frMachines = ttk.LabelFrame(master, text="Machines")
        frMachines.grid(column = 0, row =0, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(frMachines)
        self.lboxMachineList = form.Listbox(frMachines, width=30, height=20, yscrollcommand=scrollbar.set)
        self.lboxMachineList.grid(columnspan=3, column=0, row=0, padx=3, pady=3)
        self.lboxMachineList.bind("<ButtonRelease-1>", self.showDetailsMachine)
        scrollbar.config(command=self.lboxMachineList.yview)

        ttk.Button(frMachines, text="Add", width=7, command=self.addNewMachine).grid(column =0, row=1, padx=2, pady=2)
        ttk.Button(frMachines, text="Edit", width=7, command=self.editSelectedMachine).grid(column =1, row=1, padx=2, pady=2)
        ttk.Button(frMachines, text="Delete", width=7, command=self.deleteSelectedMachine).grid(column =2, row=1, padx=2, pady=2)
        
        #second label frame
        frMachineDetail = ttk.LabelFrame(master, text="Machine Detail")
        frMachineDetail.grid(column = 1, row =0, padx=5, pady=5, sticky=form.NW)

        ttk.Label(frMachineDetail, text="ID: ").grid(column =0, row=0, padx=5, pady=5)
        self.lblProperties = ttk.Label(frMachineDetail)
        self.lblProperties.grid(column =1, row=0, padx=5, pady=5)

        master.grab_set()
        master.focus()

    def addNewMachine(self):
        """Add new machine to machine list and listbox in form"""
        newMachine = Machine("M" + str(len(self.lboxMachineList.get(0, form.END))))
        global machinesList
        machinesList.append(newMachine)
        self.lboxMachineList.insert(form.END, newMachine.ID)

    def showDetailsMachine(self, event):
        """Show secondary informations about choosen machine in label"""
        try:
            global machinesList
            index = self.lboxMachineList.curselection()[0]
            selectedValue = machinesList[index].ID
            self.lblProperties.configure(text= selectedValue)
        except IndexError:
            pass

    def deleteSelectedMachine(self):
        """ Delete selected object from machine list """
        try:
            index = self.lboxMachineList.curselection()[0]
            self.lboxMachineList.delete(index)
            global machinesList
            machinesList.pop(index)
        except IndexError:
            pass

    def editSelectedMachine(self):
        """ start gui dialog to edit details about machine """
        try:
            global machinesList
            index = self.lboxMachineList.curselection()[0]
            guiMachineEdit.GuiMachineEdit(self, index)

            #reload gui list and show updates
            self.lboxMachineList.delete(0, form.END)
            for mach in machinesList:
                self.lboxMachineList.insert(form.END, mach.ID)
        except IndexError:
            pass

        #TODO: export to xml file
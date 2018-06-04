import tkinter as form
from tkinter import ttk
from tkinter import messagebox
from clTask import Task
import guiTaskNew
from globalData import STRGS
#=========================================================================================
class guiItineraryNew(form.Toplevel):
    """Form for creating new Itinerary"""

    def __init__(self, master, aNewItinerary):
        form.Toplevel.__init__(self, master)
        
        self.title(STRGS['TITLE_NEW_ITINERARIES'])
        self.geometry("%dx%d+%d+%d" % (400,350, int(self.winfo_screenwidth() / 2 - 400 / 2), int(self.winfo_screenheight() / 2 - 350 / 2)))
        self.resizable(False, False)

        ttk.Label(self, text=STRGS['ITINERARY_NAME']).grid(column=0, row=0, padx=5, pady=10, sticky=form.N)
        self.itineraryName = form.StringVar()
        self.itineraryName.set(aNewItinerary.name)
        self.entItineraryName = ttk.Entry(self, textvariable=self.itineraryName, width=15)
        self.entItineraryName.grid(column=1, row=0, padx=5, pady=10, sticky =form.N)
        self.entItineraryName.focus()

        frTaskDetails = ttk.LabelFrame(self, text=STRGS['TASK_DETAIL'])
        frTaskDetails.grid(column=0, columnspan=2, row=1, padx=5, pady=5, sticky=form.NSEW)

        ttk.Label(frTaskDetails, text=STRGS['NAME']).grid(column=0, row=0, padx=3, pady=3,sticky=form.E)
        ttk.Label(frTaskDetails, text=STRGS['DURATION']).grid(column=0, row=1, padx=3, pady=3,sticky=form.E)
        ttk.Label(frTaskDetails, text=STRGS['ORDER']).grid(column=0, row=2, padx=3, pady=3,sticky=form.E)
        ttk.Label(frTaskDetails, text=STRGS['MACH']).grid(column=0, row=3, padx=3, pady=3,sticky=form.E)

        self.lblName = ttk.Label(frTaskDetails, width=20)
        self.lblName.grid(column=1, row=0, padx=3, pady=3, sticky=form.E)

        self.lblDuration = ttk.Label(frTaskDetails, width=20)
        self.lblDuration.grid(column=1, row=1, padx=3, pady=3, sticky=form.E)

        self.lblOrder = ttk.Label(frTaskDetails, width=20)
        self.lblOrder.grid(column=1, row=2, padx=3, pady=3, sticky=form.E)

        self.lblMachine = ttk.Label(frTaskDetails, width=20)
        self.lblMachine.grid(column=1, row=3, padx=3, pady=3, sticky=form.E)

        frTasksList = ttk.LabelFrame(self, text=STRGS['TASKS_INITERARY'])
        frTasksList.grid(column=2, row=0, padx=5, pady=5, rowspan=2)

        scrollbar = ttk.Scrollbar(frTasksList)
        self.lboxTasksList = form.Listbox(frTasksList, width=27, height=15, yscrollcommand=scrollbar.set)
        self.lboxTasksList.grid(column=0, columnspan=3, row=0, padx=3, pady=3)
        self.lboxTasksList.bind("<ButtonRelease-1>", self.showDetailsTask)
        scrollbar.config(command=self.lboxTasksList.yview)

        ttk.Button(frTasksList, text=STRGS['ADD'], width=6, command=self.addTaskToItinerary).grid(column=0, row=1, padx=2, pady=4)
        ttk.Button(frTasksList, text=STRGS['EDIT'], width=6, command=self.editTaskSelected).grid(column=1, row=1, padx=2, pady=4)
        ttk.Button(frTasksList, text=STRGS['DELETE'], width=6, command=self.deleteTaskSelected).grid(column=2, row=1, padx=2, pady=4)

        ttk.Button(self, text=STRGS['SAVE'], width=20, command= lambda: self.saveItinerary(aNewItinerary)).grid(column=0, row=2, columnspan=3, padx=3, pady=3)

        #set to be on top, hijack all comands and pause anything until close
        self.transient(master)
        self.grab_set()
        master.wait_window(self)

    def addTaskToItinerary(self):
        newTask = Task()
        guiTaskNew.GuiTaskNew(self, newTask)
        print(newTask.name, newTask.duration, newTask.machine.name)
        #TODO if change or obj not null add to tasks list
        pass

    def editTaskSelected(self):
        pass

    def deleteTaskSelected(self):
        pass

    def showDetailsTask(self, event=None):
        try:
            pass
        except :
            pass

    def saveItinerary(self, itin):
        if not self.itineraryName.get():
            itin.itineraryChanged = False
            messagebox.showerror(STRGS['MSG_ERR_ITINERARY_NO_NAME'],STRGS['MSG_ERR_ITINERARY_ENTER_NAME'])
            pass
        else:
            itin.name = self.itineraryName.get()
            itin.itineraryChanged = True
            self.destroy()



        




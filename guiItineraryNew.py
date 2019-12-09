import tkinter as form
from tkinter import ttk
from tkinter import messagebox as msg
from clTask import Task
from clMachine import Machine
import guiTaskNew
from globalData import machinesList, itinerariesList, STRGS
#=========================================================================================
class GuiItineraryNew(form.Toplevel):
    """Form for creating new Itinerary"""

    def __init__(self, master, aNewItinerary, aIndex):
        form.Toplevel.__init__(self, master)
        
        self.editedItemIndex = aIndex
        self.title(STRGS['TITLE_NEW_ITINERARIES'])
        self.geometry("%dx%d+%d+%d" % (600,400, int(self.winfo_screenwidth() / 2 - 600 / 2), int(self.winfo_screenheight() / 2 - 400 / 2)))
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
        for taskObj in aNewItinerary.tasksList:
            self.lboxTasksList.insert(form.END, taskObj.name)
        self.lboxTasksList.bind("<ButtonRelease-1>", lambda event, argument = aNewItinerary: self.showDetailsTask(event, argument))
        scrollbar.config(command=self.lboxTasksList.yview)

        ttk.Button(frTasksList, text=STRGS['ADD'], width=6, command= lambda: self.taskToItinerary(aNewItinerary, isEdited=False)).grid(column=0, row=1, padx=2, pady=4)
        ttk.Button(frTasksList, text=STRGS['EDIT'], width=6, command= lambda: self.taskToItinerary(aNewItinerary, isEdited = True)).grid(column=1, row=1, padx=2, pady=4)
        ttk.Button(frTasksList, text=STRGS['DELETE'], width=6, command= lambda: self.deleteTaskSelected(aNewItinerary)).grid(column=2, row=1, padx=2, pady=4)

        ttk.Button(self, text=STRGS['SAVE'], width=20, command= lambda: self.saveItinerary(aNewItinerary)).grid(column=0, row=2, columnspan=3, padx=3, pady=3)

        #set to be on top, hijack all comands and pause anything until close
        self.transient(master)
        self.grab_set()
        master.wait_window(self)

    def taskToItinerary(self, aNewItinerary, isEdited):
        """Add or edit task in Itinerary"""
        global machinesList
        task = Task("", 0.0, machinesList[0])   
        index =0
        preventEditEmptyTask = False
        try:
            if isEdited:
                index = self.lboxTasksList.curselection()[0]
                task = aNewItinerary.tasksList[index]
        except IndexError:
            preventEditEmptyTask = True     #this is for preventing run edit dialog on empty task
            pass
        finally:
            if preventEditEmptyTask:
                return
            guiTaskNew.GuiTaskNew(self, task)
            if task.taskChanged == True:
                if isEdited:    #if edited item then do not change task list, else case add task to end
                    aNewItinerary.tasksList[index] = task
                else:
                    aNewItinerary.tasksList.append(task)

            #reload gui list and show updates
            self.lboxTasksList.delete(0, form.END)
            for taskObj in aNewItinerary.tasksList:
                self.lboxTasksList.insert(form.END, taskObj.name)
            self.showDetailsTask(self,aNewItinerary)

    def deleteTaskSelected(self, aNewItinerary):
        """Delete selected task in itinerary"""
        try:
            index = self.lboxTasksList.curselection()[0]
            self.lboxTasksList.delete(index)
            del aNewItinerary.tasksList[index]
            self.showDetailsTask(self,aNewItinerary)
        except IndexError:
            pass

    def showDetailsTask(self, event, aNewItinerary):
        """Show all important data on click in details"""
        try:
            index = self.lboxTasksList.curselection()[0]
            selectedTask = aNewItinerary.tasksList[index]

            self.lblDuration.configure(text= str(selectedTask.duration))
            self.lblMachine.configure(text= str(selectedTask.machine.name))
            self.lblName.configure(text=str(selectedTask.name))
            self.lblOrder.configure(text=str(index+1))
        except IndexError:      #not selected empty everything
            self.lblDuration.configure(text="")
            self.lblMachine.configure(text="")
            self.lblName.configure(text="")
            self.lblOrder.configure(text="")

    def saveItinerary(self, aNewItinerary):
        """Save itinerary object. to save itinerary it is compulsory to enter name"""
        if not self.itineraryName.get():
            msg.showerror(STRGS['MSG_ERR_ITINERARY_NO_NAME'], STRGS['MSG_ERR_ITINERARY_ENTER_NAME'])
            self.tkraise()
        else:
            global itinerariesList
            for index, itinObj in enumerate(itinerariesList):
                if itinObj.name == self.itineraryName.get() and self.editedItemIndex != index:
                    msg.showerror(STRGS['ERR_ILLEGAL'], itinObj.name + STRGS['ERR_EXIST_DIFF_NAME'])
                    return
            aNewItinerary.name = self.itineraryName.get()
            aNewItinerary.itineraryChanged = True
            self.destroy()

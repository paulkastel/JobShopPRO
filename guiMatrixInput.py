import tkinter as form
from tkinter import ttk
from tkinter import messagebox as msg
from clItinerary import Itinerary
from clMachine import Machine
from clTask import Task
from globalData import *
#=========================================================================================
class GuiMatrixInput(form.Toplevel):
    """Here user provide all data to the matrix """

    def __init__(self, master, aColMachines, aRowItineraries):
        form.Toplevel.__init__(self, master)

        self.title(STRGS['ENTER_MATRIX_DATA'])
        self.resizable(True, True)
        self.geometry("%dx%d+%d+%d" % (1200,600, int(master.winfo_screenwidth() / 2 - 1200 / 2), int(master.winfo_screenheight() / 2 - 600 / 2)))
        self.minsize(width=500, height=300)

        #set this window to be on top and in focus
        self.grab_set()
        self.focus_force()

        frMain = ttk.Frame(self)

        # Canvas creation with double scrollbar
        hscrollbar = ttk.Scrollbar(frMain, orient = form.HORIZONTAL)
        vscrollbar = ttk.Scrollbar(frMain, orient = form.VERTICAL)
        sizegrip = ttk.Sizegrip(frMain)
        canvas = form.Canvas(frMain, bd=0, highlightthickness=0, yscrollcommand = vscrollbar.set, xscrollcommand = hscrollbar.set)
        vscrollbar.config(command = canvas.yview)
        hscrollbar.config(command = canvas.xview)

        # everything scrollable should be in subFrame
        subFrame = ttk.Frame(canvas)
        frGridHeadline = form.Frame(subFrame)   #some constrains label

        #two matrixes for creating tasks and itineraries
        frGridTasks = ttk.Frame(subFrame)
        frGridTasks.grid(column=0, row=1,padx=30, pady=10)
        frGridItineraries = ttk.Frame(subFrame)
        frGridItineraries.grid(column=1, row=1, padx=30, pady=10)

        #here important entries are storaged
        self.timesEntries = self.createThatMatrixEntries(frGridTasks, aColMachines, aRowItineraries, validateFloat)
        self.machinesEntries = self.createThatMatrixEntries(frGridItineraries, aColMachines, aRowItineraries, validateOnlyInt)

        #after creatings frames mandatory is to get the newiest values
        frGridItineraries.update()
        frGridTasks.update()
        frGridHeadline.grid(columnspan=2, column=0, row=0, sticky=form.W)
        frGridHeadline.configure(width=frGridTasks.winfo_width() + frGridItineraries.winfo_width() + 30 * 4, height=50)
        frGridHeadline.propagate(0)
        frGridHeadline.update()
        
        #header labels added in top frame, adjusted to be in center of created
        #matrixs
        form.Label(frGridHeadline, text=STRGS['TIMES_TASKS'], font=69).place(x=40 + frGridTasks.winfo_width() / 2, y=25, anchor="center")  # x=(middle and padding)/2 and y= middle
        form.Label(frGridHeadline, text=STRGS['MACHS_ITINERARIES'], font=50).place(x=frGridTasks.winfo_width() + 60 + (frGridItineraries.winfo_width() + 90) / 2, y=25, anchor="center") # x=previous + (middle and padding)/2 and y= middle
        form.Button(self, text=STRGS['SAVE'], width=100, height=2, command=self.saveAndCreate).pack(side=form.BOTTOM, padx = 5, pady = 10)

        #Packing everything
        subFrame.pack(fill = form.BOTH, expand = form.TRUE)
        hscrollbar.pack(fill=form.X, side=form.BOTTOM, expand=form.FALSE)
        vscrollbar.pack(fill=form.Y, side=form.RIGHT, expand=form.FALSE)
        sizegrip.pack(in_= hscrollbar, side = form.BOTTOM, anchor = "se")
        canvas.pack(side = form.LEFT, padx = 5, pady = 5, fill = form.BOTH, expand= form.TRUE)
        frMain.pack(padx = 5, pady = 5, expand = True, fill = form.BOTH)

        canvas.create_window(0,0, window=subFrame, anchor = "center")
        self.update_idletasks() # update geometry
        canvas.config(scrollregion = canvas.bbox("all"))
        canvas.xview_moveto(0) 
        canvas.yview_moveto(0)

    def createThatMatrixEntries(self, frGrid, aCols, aRows, aValidateCommand):
        """returns matrix of entries in given Frame of size aCols x aRows """
        #2D array
        entriesArr = [[0 for x in range(aCols)] for x in range(aRows)]
        ttk.Label(frGrid, text="i\m", width=8, anchor="center").grid(padx=2, pady=2, row=0, column=0, sticky=form.N)
        for c in range(aCols):
            for r in range(aRows):
                if r == 0 or c == 0:
                    ttk.Label(frGrid, text=c + 1, width=8, anchor="center").grid(padx=2, pady=2, row=r, column=c + 1, sticky=form.N)
                    ttk.Label(frGrid, text=r + 1, width=8, anchor="center").grid(padx=2, pady=2, row=r + 1, column=c, sticky=form.N)

        vcmd = (self.register(aValidateCommand), self, '%d', '%i', '%P', 6, '%s', '%S', '%v', '%V', '%W')
        for c in range(1, aCols + 1):
            for r in range(1, aRows + 1):
                entriesArr[r - 1][c - 1] = ttk.Entry(frGrid, width=8, validate='key', validatecommand = vcmd)
                entriesArr[r - 1][c - 1].grid(padx=2, pady=2, row=r, column=c, sticky=form.N)

        return entriesArr

    def saveAndCreate(self):
        """Gets values from all entries in GUI and saves it into the global data lists"""
        global machinesList, itinerariesList
        flagForExit = True

        #create machines
        for m in range(len(self.timesEntries[0])):
            machinesList.append(Machine("M" + str(m + 1)))
        
        try:
            #for each itinerary create new one
            for r in range(len(self.timesEntries)):
                itin = Itinerary()
                itin.name = "Itinerary " + str(r + 1)
                #and for each machine get value after validation for corectness
                for c in range(len(self.timesEntries[r])):
                    if self.timesEntries[r][c].get() == "" and self.machinesEntries[r][c].get() == "":
                        pass
                    elif (self.timesEntries[r][c].get() == "" and self.machinesEntries[r][c].get() != "") or (self.timesEntries[r][c].get() != "" and self.machinesEntries[r][c].get() == ""):
                        raise ValueError("Task have no time or machine assigned", (r + 1,c + 1))
                    else:
                        #create task in itinerary if machine id exist in range
                        if int(self.machinesEntries[r][c].get()) in range(1,len(self.timesEntries[r]) + 1):
                            if float(self.timesEntries[r][c].get()) != 0:
                                task = Task("Task " + (str(c + 1)), float(self.timesEntries[r][c].get()), machinesList[int(self.machinesEntries[r][c].get()) - 1])
                                itin.tasksList.append(task)
                            else:
                                raise ValueError("Task duration cannot be equal zero!", (r + 1, c + 1))
                        else:
                            raise ValueError("Machine ID is invalid!", (r + 1,c + 1))
                #and add it to global list
                itinerariesList.append(itin)    
        except ValueError as errMsg:
            flagForExit = False
            msg.showerror(STRGS['ERR'], errMsg.args[0] + STRGS['MSG_ERR_INVOLVE_TASK'] + str(errMsg.args[1]))
            machinesList.clear()
            itinerariesList.clear()

        if flagForExit:
            self.destroy()
        
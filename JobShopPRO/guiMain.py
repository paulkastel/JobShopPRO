import tkinter as form
from tkinter import ttk
import guiMachine
import guiItinerary
import guiMatrixParam
import guiMatrixInput
from globalData import *
from tkinter import messagebox as msg
#=========================================================================================
class GuiMain(form.Frame):
    """Main form to manage all the program and options"""

    def __init__(self, master):
        form.Frame.__init__(self, master)

        master.title(STRGS['TITLE_PROGRAM'])
        #center window in the middle of the screen
        master.geometry("%dx%d+%d+%d" % (600,400, int(master.winfo_screenwidth() / 2 - 600 / 2), int(master.winfo_screenheight() / 2 - 400 / 2)))
        master.resizable(False, False)

        menuBar = form.Menu(master)
        master.config(menu=menuBar)

        setupOption = form.Menu(menuBar, tearoff=0)
        dataOption = form.Menu(menuBar, tearoff=0)
        aboutOption = form.Menu(menuBar, tearoff=0)

        setupOption.add_command(label=STRGS['ENTER_MATRIX_DATA'], command=self.popMatrixDlg)
        setupOption.add_separator()
        setupOption.add_command(label=STRGS['MACHS'], command=self.popMachinesDlg)
        setupOption.add_command(label=STRGS['ITINERARIES'], command=self.popItinerariesDlg)
        setupOption.add_separator()
        setupOption.add_command(label=STRGS['EXIT'], command=self.exitProgram)

        dataOption.add_command(label=STRGS['FILE_IMPORT'], command=self.dataFileImport)
        dataOption.add_command(label=STRGS['FILE_EXPORT'], command=self.dataFileExport)
        
        #TODO: to dataOption create new window with logs?

        aboutOption.add_command(label=STRGS['ABOUT'], command=self.popAboutDlg)
      
        menuBar.add_cascade(label=STRGS['SETUP'], menu=setupOption)
        menuBar.add_cascade(label=STRGS['DATA'], menu=dataOption)
        menuBar.add_cascade(label=STRGS['DETAILS'], menu=aboutOption)

        tabController = ttk.Notebook(master, width=40)
        frTabMain = ttk.Frame(tabController)
        frTabLPT = ttk.Frame(tabController)
        frTabSPT = ttk.Frame(tabController)
        frTabLifo = ttk.Frame(tabController)
        frTabFifo = ttk.Frame(tabController)

        tabController.add(frTabMain, text=STRGS['SETUP'])
        tabController.add(frTabLPT, text="LPT")
        tabController.add(frTabSPT, text="SPT")
        tabController.add(frTabLifo, text="LIFO")
        tabController.add(frTabFifo, text="FIFO")
        tabController.pack(expand=1, fill="both")

        ttk.Button(frTabMain, text=STRGS['MACHS'], width=20, command=self.popMachinesDlg).grid(column=0, row=0, padx=5, pady=5)
        ttk.Button(frTabMain, text=STRGS['ITINERARIES'], width=20, command=self.popItinerariesDlg).grid(column=0, row=1, padx=5, pady=5)
        ttk.Button(frTabMain, text=STRGS['ENTER_MATRIX_DATA'], width=20, command=self.popMatrixDlg).grid(column=0, row=2, padx=5, pady=5)
        form.Button(frTabMain, text=STRGS['CALC'], width=17, height=8, command=self.createGraphs).grid(column=0, row=3, padx=5, pady=5)

        global machinesList, itinerariesList
        self.lblMachinesCount = ttk.Label(frTabMain)
        self.lblMachinesCount.grid(column =1, row=0, padx=5, pady=5)

        self.lblItinerariesCount = ttk.Label(frTabMain)
        self.lblItinerariesCount.grid(column =1, row=1, padx=5, pady=5)

        self.updateMainLabelsConfiguration()

        #gui footer that shows additional information
        #TODO: use it to show logs in app?
        self.statusBar = form.Label(master, text="status bar info", bd=1, relief=form.SUNKEN, anchor=form.W)
        self.statusBar.pack(side=form.BOTTOM, fill=form.X)

    def popAboutDlg(self):
        """Shows info about program and author"""
        msg.showinfo(STRGS['ABOUT_TITLE'], STRGS['ABOUT_MESG'])
        pass

    def popMachinesDlg(self):
        """Shows dialog to create machines"""
        guiMachine.GuiMachine(form.Toplevel(self)).wait_window()
        self.updateMainLabelsConfiguration()
        pass

    def popMatrixDlg(self):
        """Initiates procedure of entering values by matrix"""
        global machinesList, itinerariesList
        if len(machinesList) or len(itinerariesList):
            answer = msg.askyesno(STRGS['WARN'],STRGS['MSG_WARN_ERASE_DATA'], icon="warning")
            if answer:
                machinesList.clear()
                itinerariesList.clear()
            else:
                return

        #save important values in tuple
        machinesAmount = 0
        itinerariesAmount = 0
        arrAmount = [machinesAmount, itinerariesAmount]

        #python only allow pass-by-object, so this is only way to get numbers
        #from next gui
        guiMatrixParam.GuiMatrixParam(self, arrAmount).wait_window()
        self.focus_force()
        if all(x != 0 for x in arrAmount):
            guiMatrixInput.GuiMatrixInput(self, arrAmount[0], arrAmount[1]).wait_window()
        self.updateMainLabelsConfiguration()    

    def popItinerariesDlg(self):
        """Shows dialog to create itineraries"""
        guiItinerary.GuiItinerary(form.Toplevel(self)).wait_window()
        self.updateMainLabelsConfiguration()
        pass

    def exitProgram(self):
        """Quit everything"""
        answer = msg.askyesno(STRGS['EXIT'], STRGS['MSG_REALLY_QUIT'])
        if answer:
            self.quit()
            self.destroy()
            exit()

    def createGraphs(self):
        print("#TODO: graph")
        pass

    def dataFileImport(self):
        print("#TODO: import")
        pass

    def dataFileExport(self):
        print("#TODO: export")
        pass

    def updateMainLabelsConfiguration(self):
        """Updates labels with actual amount of items in global lists"""
        global machinesList, itinerariesList
        self.lblItinerariesCount.config(text=STRGS['CREATED'] + str(len(itinerariesList)) + " " + STRGS['MACHS'])
        self.lblMachinesCount.config(text=STRGS['CREATED'] + str(len(machinesList)) + " " + STRGS['ITINERARIES'])
        
    #TODO: favicon
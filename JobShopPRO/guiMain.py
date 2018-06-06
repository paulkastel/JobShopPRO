import tkinter as form
from tkinter import ttk
import guiMachine, guiItinerary
from globalData import STRGS
from tkinter import messagebox as msg
#=========================================================================================
class GuiMain(form.Frame):
    """ Main form to manage all the program and options """

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

        setupOption.add_command(label="Enter data in matrix", command=self.popMatrixDlg)
        setupOption.add_separator()
        setupOption.add_command(label="Machines", command=self.popMachinesDlg)
        setupOption.add_command(label="Itineraries", command=self.popItinerariesDlg)
        setupOption.add_separator()
        setupOption.add_command(label="Exit", command=self.exitProgram)

        dataOption.add_command(label="Import from file...", command=self.dataFileImport)
        dataOption.add_command(label="Export to file...", command=self.dataFileExport)

        aboutOption.add_command(label="About", command=self.popAboutDlg)
      
        menuBar.add_cascade(label="Setup", menu=setupOption)
        menuBar.add_cascade(label="Data", menu=dataOption)
        menuBar.add_cascade(label="Information", menu=aboutOption)

        tabController = ttk.Notebook(master)
        frTabMain = ttk.Frame(tabController)
        frTabLPT = ttk.Frame(tabController)
        frTabSPT = ttk.Frame(tabController)

        tabController.add(frTabMain, text="Setup")
        tabController.add(frTabLPT, text="LPT")
        tabController.add(frTabSPT, text="SPT")

        tabController.pack(expand=1, fill="both")

        ttk.Button(frTabMain, text="Machines", width=20, command=self.popMachinesDlg).grid(column=0, row=0, padx=5, pady=5)
        ttk.Button(frTabMain, text="Itineraries", width=20, command=self.popItinerariesDlg).grid(column=0, row=1, padx=5, pady=5)
        form.Button(frTabMain, text="Itineraries", width=17, height=8, command=self.createGraphs).grid(column=0, row=2, padx=5, pady=5)

        self.lblMachinesCount = ttk.Label(frTabMain, text="Created 3 machines").grid(column =1, row=0, padx=5, pady=5)
        self.lblItinerariesCount = ttk.Label(frTabMain, text="Created 3 itinereaies").grid(column =1, row=1, padx=5, pady=5)

        #gui footer that shows additional information
        self.statusBar = form.Label(master, text="status bar info", bd=1, relief=form.SUNKEN, anchor=form.W)
        self.statusBar.pack(side=form.BOTTOM, fill=form.X)


    def popAboutDlg(self):
        msg.showinfo("About JobShopPRO", "This is JobShopPRO\nMade as Master Thesis at AGH University\nby Pawel Kastelik, 2018")
        pass

    def popMachinesDlg(self):
        guiMachine.GuiMachine(form.Toplevel(self))
        pass

    def popMatrixDlg(self):
        print("TODO matrix")
        pass    

    def popItinerariesDlg(self):
        guiItinerary.GuiItinerary(form.Toplevel(self))
        pass

    def exitProgram(self):
        answer = msg.askyesno("Exit", "For sure you want to quit?")
        if answer:
            self.quit()
            self.destroy()
            exit()

    def createGraphs(self):
        print("TODO graph")
        pass

    def dataFileImport(self):
        print("TODO import")
        pass

    def dataFileExport(self):
        print("TODO export")
        pass




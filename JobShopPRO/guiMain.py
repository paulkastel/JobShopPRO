import tkinter as form
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
import guiMachine
import guiItinerary
import guiMatrixParam
import guiMatrixInput
from clMachine import Machine
from clItinerary import Itinerary
from clTask import Task
from globalData import *
from tkinter import messagebox as msg
from time import gmtime, strftime
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

        dataOption.add_command(label=STRGS['M_FILE_IMPORT'], command=self.dataFileImport)
        dataOption.add_command(label=STRGS['M_FILE_EXPORT'], command=self.dataFileExport)
        
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
                pass
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
            machinesList.clear()
            itinerariesList.clear()
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
        """Tries to import JSON JobShop PRO file to program"""
        savePath = askopenfilename(defaultextension=".json", filetypes =(("JSON files",".json"),("Allfiles","*.*")))

        if savePath == "":
            return
        
        importedData = None

        #in case of corrupted file or entering wrong file create backup of existing data in program
        global machinesList, itinerariesList
        machinesListBackup = machinesList[:]        #create backup by copying by slicing
        itinerariesListBackup = itinerariesList[:]
        machinesList.clear()
        itinerariesList.clear()

        try:
            with open(savePath, 'r') as infile:
                importedData = json.loads(infile.read())

                if list(importedData.keys()) == ["itineraries", "machines"]:
                    imMachines = importedData['machines']
                    imItineraries = importedData['itineraries']

                    if len(list(imMachines)) > 0 and len(list(imItineraries)) > 0:
                        for index, machDict, in enumerate(imMachines):
                            if list(machDict.keys()) == ["machineName"]:
                                machinesList.append(Machine(imMachines[index]['machineName']))
                            else:
                                raise ValueError("Machine is not correct")
                    
                        for index, itinDict in enumerate(imItineraries):
                            if list(itinDict.keys()) == ["itineraryName", "tasksList"]:
                                iti = Itinerary()
                                iti.name = itinDict['itineraryName']
                                if len(list(itinDict['tasksList'])) > 0:
                                    itiTaskList = itinDict['tasksList']

                                    for index, taskDict in enumerate(itiTaskList):
                                        if list(itiTaskList[index].keys()) == ['taskName', 'taskMachine', 'taskDuration']:
                                            taskMach = itiTaskList[index]['taskMachine']
                                            if list(taskMach.keys()) == ["machineName"]:
                                                iti.tasksList.append(Task(itiTaskList[index]['taskName'], float(itiTaskList[index]['taskDuration']), Machine(taskMach["machineName"])))
                                            else:
                                                raise ValueError("Machine in task is not correct")   
                                        else:
                                            raise ValueError("One of tasks in itinerary is not correct")
                                    itinerariesList.append(iti)
                                else:
                                    raise ValueError("List of task in itinerary is not correct")
                            else:
                                raise ValueError("Structure of itineraries is invalid!")
                    else:
                        raise ValueError("Itineraries and machines lists are empty or structure is not correct!")
                else:
                    raise ValueError("Itineraries or machines structure is invalid!")

                for testItinObj in itinerariesList:
                    for testTaskObj in testItinObj.tasksList:
                        if not testTaskObj.machine.name in [mach.name for mach in machinesList]:
                            raise ValueError(testTaskObj.name + " in " + testItinObj.name + " have invalid machine.\nData is incopatible")            
            
            #TODO: checking if values are not null  or empty and raise exception!
            #TODO: change var names
            msg.showinfo(STRGS['OK'], STRGS['MSG_OK_FILE_IMPORTED'])

            machinesListBackup = None
            itinerariesListBackup = None

        except ValueError as err:
            msg.showerror(STRGS['ERR'], err)
            machinesList = machinesListBackup
            itinerariesList = itinerariesListBackup
        except:
            msg.showerror("Unexpected " + STRGS['ERR'])
            machinesList = machinesListBackup
            itinerariesList = itinerariesListBackup
        finally:
            self.updateMainLabelsConfiguration()

    def dataFileExport(self):
        """Export all data (project) as json file in specified path"""
        global machinesList, itinerariesList
        if not len(machinesList) and not len(itinerariesList):
            msg.showwarning(STRGS['WARN'], STRGS['MSG_WARN_NO_EXPORT'])
            return

        exItinerariesToJSON = []       #export machines in kinda serializable form
        for itin in itinerariesList:
            exItinerariesToJSON.append(itin.exportToDict()) 

        exMachinesToJSON = [] 
        for mach in machinesList:
            exMachinesToJSON.append(mach.exportToDict())
        
        #to have nice structure of json file we store dictionary data in one
        #file
        exportData = {}
        exportData['itineraries'] = exItinerariesToJSON
        exportData['machines'] = exMachinesToJSON

        try:
            fileName = STRGS['TITLE_PROGRAM'] + " - projectExport " + strftime("%Y%m%d%H%M", gmtime()) + ".json"
            savePath = asksaveasfilename(initialfile=fileName, defaultextension=".json", filetypes =(("JSON files", ".json"),("All files", "*.*")))  #open save file window
            
            if savePath != "":
                with open(savePath, 'w', encoding='utf-8') as outfile:
                    json.dump(exportData, outfile, indent=4)    #put serialzed json data in outfile saved in savePath directory
                msg.showinfo(STRGS['OK'], STRGS['MSG_OK_FILE_EXPORTED'])
        except Exception as err:
            msg.showerror(STRGS['ERR'], err)

    def updateMainLabelsConfiguration(self):
        """Updates labels with actual amount of items in global lists"""
        global machinesList, itinerariesList
        self.lblItinerariesCount.config(text=STRGS['CREATED'] + str(len(itinerariesList)) + " " + STRGS['ITINERARIES'])
        self.lblMachinesCount.config(text=STRGS['CREATED'] + str(len(machinesList)) + " " + STRGS['MACHS'])
        
    #TODO: favicon
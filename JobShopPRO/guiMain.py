import tkinter as form
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
import guiMachine
import guiItinerary
import guiMatrixParam
import guiMatrixInput
from algorithms import *
from chartGanttCreator import createGanttChart
from clMachine import Machine
from clItinerary import Itinerary
from clTask import Task
from globalData import *
from tkinter import messagebox as msg
from time import gmtime, strftime
import json
import sys
import copy
from random import randint
import os
#=========================================================================================
class GuiMain(form.Frame):
    """Main form to manage all the program and options"""

    def __init__(self, master):
        form.Frame.__init__(self, master)

        master.title(STRGS['TITLE_PROGRAM'])
        #center window in the middle of the screen
        master.geometry("%dx%d+%d+%d" % (600,450, int(master.winfo_screenwidth() / 2 - 600 / 2), int(master.winfo_screenheight() / 2 - 450 / 2)))
        master.minsize(width=600, height=450)

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
        dataOption.add_separator()
        dataOption.add_command(label="Populate random data files", command=self.exportRandomDataFiles)
        
        #TODO: to dataOption create new window with logs?

        aboutOption.add_command(label=STRGS['ABOUT'], command=self.popAboutDlg)
      
        menuBar.add_cascade(label=STRGS['SETUP'], menu=setupOption)
        menuBar.add_cascade(label=STRGS['DATA'], menu=dataOption)
        menuBar.add_cascade(label=STRGS['DETAILS'], menu=aboutOption)

        tabController = ttk.Notebook(master, width=40)
        frTabMain = ttk.Frame(tabController)
        
        self.frTabRandomSol = ttk.Frame(tabController)
        self.frTabFifo = ttk.Frame(tabController)
        self.frTabLifo = ttk.Frame(tabController)
        self.frTabLPT = ttk.Frame(tabController)
        self.frTabSPT = ttk.Frame(tabController)
        self.frTabOptSol = ttk.Frame(tabController)
        
        tabController.add(frTabMain, text=STRGS['SETUP'])
        tabController.add(self.frTabRandomSol, text="RANDOM")        
        tabController.add(self.frTabFifo, text="FIFO")        
        tabController.add(self.frTabLifo, text="LIFO")
        tabController.add(self.frTabSPT, text="SPT")       
        tabController.add(self.frTabLPT, text="LPT")
        tabController.add(self.frTabOptSol, text="OPTIMUM")

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

        #TODO: create and store logs of what is happening

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
        """Start calculations for existing data and creates graphs"""
        global itinerariesList, machinesList
        if len(itinerariesList) and len(machinesList):
            #TODO: progress bar of calculations

            jobList = prepareJobs()

            randomResult = randomSolution(copy.deepcopy(jobList))
            createGanttChart(self.frTabRandomSol, randomResult)

            fifoResult = algorithmFIFO(copy.deepcopy(jobList))
            createGanttChart(self.frTabFifo, fifoResult)            
            
            lifoResult = algorithmLIFO(copy.deepcopy(jobList))
            createGanttChart(self.frTabLifo, lifoResult)

            resultLPT = algorithmLPT(copy.deepcopy(jobList))
            createGanttChart(self.frTabLPT, resultLPT)
                        
            resultSPT = algorithmSPT(copy.deepcopy(jobList))
            createGanttChart(self.frTabSPT, resultSPT)

            optResult = optimalSolution(copy.deepcopy(jobList))
            createGanttChart(self.frTabOptSol, optResult)

            msg.showinfo(STRGS['OK'], "Calculations finished!")

        else:
            msg.showerror(STRGS['ERR_ILLEGAL'], STRGS['MSG_ERR_EMPTY_VAL'])

    def dataFileImport(self):
        """Tries to import JSON JobShop PRO file to program"""
        global machinesList, itinerariesList
        if len(machinesList) or len(itinerariesList):
            answer = msg.askyesno(STRGS['WARN'],STRGS['MSG_WARN_ERASE_DATA'], icon="warning")
            if answer:
                pass
            else:
                return

        savePath = askopenfilename(defaultextension=".json", filetypes =(("JSON files",".json"),("All files","*.*")))

        if not isStringNotBlank(savePath):
            return              #cancelled?  stop this madness now
       
        #in case of corrupted file or entering wrong file create backup of
        #existing data in program
        machinesListBackup = machinesList[:]                    #create backup by copying by slicing
        itinerariesListBackup = itinerariesList[:]

        importedData = None

        try:
            if savePath[-5:].upper().lower() != ".json":        #insensitive extension comparision
                raise ValueError("This is not JSON file!")

            with open(savePath, 'r', encoding="utf8") as inputfile:              #read file from path
                importedData = json.loads(inputfile.read())

            if list(importedData.keys()) == ["itineraries", "machines"]:
                imMachines = importedData['machines']                               #is firstlevel structure is correct, then split
                imItineraries = importedData['itineraries']
                
                machinesList.clear()
                itinerariesList.clear()

                if len(list(imMachines)) > 0 and len(list(imItineraries)) > 0:
                    for index, dictMachine, in enumerate(imMachines):           
                        if list(dictMachine.keys()) == ["machineName"]:                         #if structure of machine element is correct
                            if isStringNotBlank(imMachines[index]['machineName']):              #if not empty, parse values from dictionary
                                machinesList.append(Machine(imMachines[index]['machineName']))
                            else:
                                raise ValueError("Name of machine is empty. This is illegal!")
                        else:
                            raise ValueError("Machine is not correct")
                    
                    for _, dictItinerary in enumerate(imItineraries):                           #for each itinerary check structure
                        if list(dictItinerary.keys()) == ["itineraryName", "tasksList"]:
                            tmpItinerary = Itinerary()

                            if isStringNotBlank(dictItinerary['itineraryName']):                    #and correctness
                                tmpItinerary.name = dictItinerary['itineraryName']

                                if len(list(dictItinerary['tasksList'])) > 0:                       #if tasks not empty
                                    tmpItineraryTasks = dictItinerary['tasksList']

                                    for i, taskDict in enumerate(tmpItineraryTasks):                #check structure of each task in itinerary
                                        if list(tmpItineraryTasks[i].keys()) == ['taskName', 'taskMachine', 'taskDuration']:
                                            taskMachine = tmpItineraryTasks[i]['taskMachine']

                                            if list(taskMachine.keys()) == ["machineName"]:                     #check corectness of elements
                                                if isStringNotBlank(tmpItineraryTasks[i]['taskName']) and isStringNotBlank(taskMachine["machineName"]) and tmpItineraryTasks[i]['taskDuration'] > 0:

                                                    tmpItinerary.tasksList.append(Task(tmpItineraryTasks[i]['taskName'], 
                                                                                        float(tmpItineraryTasks[i]['taskDuration']),     #parse values to taskList
                                                                                        Machine(taskMachine["machineName"])))
                                                else:
                                                    raise ValueError("Task properties are incorrect.")          #anything wrong?  throw exception!
                                            else:
                                                raise ValueError("Machine in task is not correct")   
                                        else:
                                            raise ValueError("One of tasks in itinerary is not correct")
                                    itinerariesList.append(tmpItinerary)            #add itinerary to global list, beacuse parsing finished
                                else:
                                    raise ValueError("List of task in itinerary is not correct")
                            else:
                                raise ValueError("Itinerary name is empty. This is illegal!")
                        else:
                            raise ValueError("Structure of itineraries is invalid!")
                else:
                    raise ValueError("Itineraries or machines lists is empty or structure is not correct!")
            else:
                raise ValueError("Itineraries or machines structure is invalid!\nProbably not an JobShop JSON file!")

            #at this stage values should be OK, but check if machines are
            #not twisted and if that all itineraries have unique names
            for testItinObj in itinerariesList:
                for testTaskObj in testItinObj.tasksList:
                    if not testTaskObj.machine.name in [mach.name for mach in machinesList]:
                        raise ValueError(testTaskObj.name + " in " + testItinObj.name + " have invalid machine.\nData is incompatibile!")            
            
            if len([testItinObj.name for testItinObj in itinerariesList]) != len(set([testItinObj.name for testItinObj in itinerariesList])):
                raise ValueError("Not all itineraries have unique names!\nData is incompatibile!")

            #msg.showinfo(STRGS['OK'], STRGS['MSG_OK_FILE_IMPORTED']) #notify
            #user that succeded
 
        except ValueError as err:
            msg.showerror(STRGS['ERR'], err)
            machinesList = machinesListBackup[:]
            itinerariesList = itinerariesListBackup[:]
        except:
            msg.showerror("Unexpected " + STRGS['ERR'], sys.exc_info())    #in case if anything unexpected happen pop up
            machinesList = machinesListBackup[:]                            #and restore deleted data from backup
            itinerariesList = itinerariesListBackup[:]
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
    
    def exportRandomDataFiles(self):
        machinesAmount = 0
        itinerariesAmount = 0
        arrAmount = [machinesAmount, itinerariesAmount]
        machinesRandomList =[]
        itinerariesRandomList = []
        #python only allow pass-by-object, so this is only way to get numbers
        #from next gui
        guiMatrixParam.GuiMatrixParam(self, arrAmount).wait_window()
        self.focus_force()
        if all(x != 0 for x in arrAmount):
            machinesAmount, itinerariesAmount = arrAmount
            for filesID in range(5):
                for mach in range(machinesAmount):
                    machinesRandomList.append(Machine("M"+str(mach+1)))

                for itin in range(itinerariesAmount):
                    itinObj = Itinerary()
                    itinObj.name = "Itinerary "+str(itin+1)
                    for rndTask in range(randint(1, machinesAmount)):
                        t = Task("Task "+str(rndTask+1),randint(1, 100), machinesRandomList[randint(0, machinesAmount-1)])
                        itinObj.tasksList.append(t)
                    itinerariesRandomList.append(itinObj)

                exItinerariesToJSON = []       #export machines in kinda serializable form
                for itin in itinerariesRandomList:
                    exItinerariesToJSON.append(itin.exportToDict()) 

                exMachinesToJSON = [] 
                for mach in machinesList:
                    machinesRandomList.append(mach.exportToDict())
        
                #to have nice structure of json file we store dictionary data in one
                #file
                exportData = {}
                exportData['itineraries'] = exItinerariesToJSON
                exportData['machines'] = exMachinesToJSON

                try:
                    fileName = STRGS['TITLE_PROGRAM'] + " - randomExport "+str(filesID+1)+ ".json"
                    savePath = "TestCases M"+str(machinesAmount)+" X J"+str(itinerariesAmount)+ strftime(" %Y%m%d%H%M", gmtime()) +"/"+fileName
            
                    if savePath != "":
                        if not os.path.exists(os.path.dirname(savePath)):
                            os.makedirs(os.path.dirname(savePath))
                        with open(savePath, 'w', encoding='utf-8') as outfile:
                            json.dump(exportData, outfile, indent=4)    #put serialzed json data in outfile saved in savePath directory
                        #msg.showinfo(STRGS['OK'], STRGS['MSG_OK_FILE_EXPORTED'])
                except Exception as err:
                    msg.showerror(STRGS['ERR'], err)

                machinesRandomList.clear()
                itinerariesRandomList.clear()

    #TODO: favicon
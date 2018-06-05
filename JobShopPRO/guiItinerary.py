import tkinter as form
from tkinter import ttk
from tkinter import messagebox
from guiItineraryNew import guiItineraryNew
from clItinerary import Itinerary
from globalData import *
#=========================================================================================
class GuiItinerary(form.Frame):
    """ Form to manage itineraries in project """

    def __init__(self, master):
        form.Frame.__init__(self, master)

        master.title(STRGS['TITLE_ITINERARIES'])
        master.geometry("%dx%d+%d+%d" % (350,400, int(master.winfo_screenwidth() / 2 - 350 / 2), int(master.winfo_screenheight() / 2 - 400 / 2)))
        master.resizable(False, False)

        frItineraries = ttk.LabelFrame(master, text=STRGS['TITLE_ITINERARIES'])
        frItineraries.grid(column=0, row=0, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(frItineraries)
        self.lboxItierariesList = form.Listbox(frItineraries, width=30, height=18, yscrollcommand=scrollbar.set)
        self.lboxItierariesList.grid(column=0, row=0, padx=3, pady=3)
        self.lboxItierariesList.bind("<ButtonRelease-1>", self.showDetailsItineraries)
        scrollbar.config(command=self.lboxItierariesList.yview)
        
        frButtons = ttk.Frame(master)
        frButtons.grid(column = 1, row=0, padx=5, pady=5, sticky=form.N)

        ttk.Button(frButtons, text=STRGS['ADD_NEW'], width=15, command=self.addNewItinerary).grid(column=0, row=0, padx=2, pady=2)
        ttk.Button(frButtons, text=STRGS['EDIT'], width=15, command=self.editItinerary).grid(column=0, row=1, padx=2, pady=2)
        ttk.Button(frButtons, text=STRGS['DELETE'], width=15, command=self.deleteItinerary).grid(column=0, row=2, padx=2, pady=2)

        #TODO: add two buttons to change order? (up/down)

        frItineraryDetail = ttk.LabelFrame(master, text=STRGS['DETAILS'])
        frItineraryDetail.grid(column=0, row=1, columnspan=2, padx=5, pady=5, sticky=form.W)

        self.lblProperties = ttk.Label(frItineraryDetail, width=50)
        self.lblProperties.grid(column=0, row=0, padx=3, pady=3)

    def addNewItinerary(self):
        global machinesList
        if not machinesList:
            messagebox.showerror(STRGS['ERR_NO_MACH_CREATE'], STRGS['ERR_NO_MACH_NO_ITINERS'])
        else:
            newItinerary = Itinerary()
            guiItineraryNew(self, newItinerary)
            if newItinerary.itineraryChanged == True:
                global itinerariesList
                itinerariesList.append(newItinerary)
                self.lboxItierariesList.insert(form.END, newItinerary.name)

    def editItinerary(self):
        try:
            global itinerariesList
            index = self.lboxItierariesList.curselection()[0]
            guiItineraryNew(self, itinerariesList[index])

            #reload gui list of itineraries
            self.lboxItierariesList.delete(0, form.END)
            for itinerary in itinerariesList:
                self.lboxItierariesList.insert(form.END, itinerary.name)

            #self.showDetailsItineraries()
        except IndexError:
            pass

    def deleteItinerary(self):
        try:
            index = self.lboxItierariesList.curselection()[0]
            self.lboxItierariesList.delete(index)
            global itinerariesList
            itinerariesList.pop(index)
        except IndexError:
            pass
    
    def showDetailsItineraries(self, event):
        try:
            global itinerariesList
            index = self.lboxItierariesList.curselection()[0]
            selectedValue = itinerariesList[index].name
            self.lblProperties.configure(text=selectedValue+", "+str(len(itinerariesList[index].tasksList))+" "+STRGS['TASKS_INITERARY'])
        except IndexError:
             self.lblProperties.configure(text="")

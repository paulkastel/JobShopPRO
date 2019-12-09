import tkinter as form
from tkinter import ttk
from tkinter import messagebox
from guiItineraryNew import GuiItineraryNew
from clItinerary import Itinerary
from globalData import *
#=========================================================================================
class GuiItinerary(form.Frame):
    """Form to manage itineraries in project"""

    def __init__(self, master):
        form.Frame.__init__(self, master)

        master.title(STRGS['ITINERARIES'])
        master.geometry("%dx%d+%d+%d" % (500,500, int(master.winfo_screenwidth() / 2 - 500 / 2), int(master.winfo_screenheight() / 2 - 500 / 2)))
        master.resizable(False, False)

        frItineraries = ttk.LabelFrame(master, text=STRGS['ITINERARIES'])
        frItineraries.grid(column=0, row=0, padx=5, pady=5)

        #listbox with itineraries
        scrollbar = ttk.Scrollbar(frItineraries)
        self.lboxItinerariesList = form.Listbox(frItineraries, width=30, height=18, yscrollcommand=scrollbar.set)
        self.lboxItinerariesList.grid(column=0, row=0, padx=3, pady=3)
        self.lboxItinerariesList.bind("<ButtonRelease-1>", self.showDetailsItineraries)
        for itineraryObj in itinerariesList:
            self.lboxItinerariesList.insert(form.END, itineraryObj.name)
        scrollbar.config(command=self.lboxItinerariesList.yview)
        
        frButtons = ttk.Frame(master)
        frButtons.grid(column = 1, row=0, padx=5, pady=5, sticky=form.N)

        ttk.Button(frButtons, text=STRGS['ADD_NEW'], width=15, command=self.addNewItinerary).grid(column=0, row=0, padx=2, pady=2)
        ttk.Button(frButtons, text=STRGS['EDIT'], width=15, command=self.editItinerary).grid(column=0, row=1, padx=2, pady=2)
        ttk.Button(frButtons, text=STRGS['DELETE'], width=15, command=self.deleteItinerary).grid(column=0, row=2, padx=2, pady=2)

        #TODO: add two buttons to change order?  (up/down)

        frItineraryDetail = ttk.LabelFrame(master, text=STRGS['DETAILS'])
        frItineraryDetail.grid(column=0, row=1, columnspan=2, padx=5, pady=5, sticky=form.W)

        self.lblProperties = ttk.Label(frItineraryDetail, width=50)
        self.lblProperties.grid(column=0, row=0, padx=3, pady=3)

        master.grab_set()
        master.focus()

    def addNewItinerary(self):
        """Runs dialog to add new itinerary"""
        global machinesList, itinerariesList
        if not machinesList:
            messagebox.showerror(STRGS['MSG_ERR_NO_MACH_CREATE'], STRGS['MSG_ERR_NO_MACH_NO_ITINERS'])
        else:
            newItinerary = Itinerary()
            GuiItineraryNew(self, newItinerary, len(itinerariesList))
            if newItinerary.itineraryChanged == True:
                itinerariesList.append(newItinerary)
                self.lboxItinerariesList.insert(form.END, newItinerary.name)

    def editItinerary(self):
        """Runs dialog with itinerary info to edit its values"""
        try:
            global itinerariesList
            index = self.lboxItinerariesList.curselection()[0] #selected itinerary in listbx
            GuiItineraryNew(self, itinerariesList[index], index)

            #reload gui list of itineraries
            self.lboxItinerariesList.delete(0, form.END)
            for itinerary in itinerariesList:
                self.lboxItinerariesList.insert(form.END, itinerary.name)
        except IndexError:
            pass

    def deleteItinerary(self):
        """Removes selected itinerary"""
        try:
            index = self.lboxItinerariesList.curselection()[0]
            self.lboxItinerariesList.delete(index)
            global itinerariesList
            itinerariesList.pop(index)
        except IndexError:
            pass
    
    def showDetailsItineraries(self, event):
        """Shows detailed info about selected itinerary in listbox"""
        try:
            global itinerariesList
            index = self.lboxItinerariesList.curselection()[0]
            selectedValue = itinerariesList[index].name
            self.lblProperties.configure(text=selectedValue + ", " + str(len(itinerariesList[index].tasksList)) + " " + STRGS['TASKS_INITERARY'])
        except IndexError:
             self.lblProperties.configure(text="")

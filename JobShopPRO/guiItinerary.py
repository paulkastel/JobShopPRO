import tkinter as form
from tkinter import ttk
from guiItineraryNew import guiItineraryNew
from clItinerary import Itinerary
#=========================================================================================
class GuiItinerary(form.Frame):
    """ Form to manage itineraries in project """

    def __init__(self, master):
        form.Frame.__init__(self, master)

        master.title("Itineraries")
        master.geometry("%dx%d+%d+%d" % (400,400, int(master.winfo_screenwidth() / 2 - 400 / 2), int(master.winfo_screenheight() / 2 - 400 / 2)))
        master.resizable(False, False)

        frItineraries = ttk.LabelFrame(master, text="Itneraries")
        frItineraries.grid(column=0, row=0, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(frItineraries)
        self.lboxItieraries = form.Listbox(frItineraries, width=30, height=18, yscrollcommand=scrollbar.set)
        self.lboxItieraries.grid(column=0, row=0, padx=3, pady=3)
        scrollbar.config(command=self.lboxItieraries.yview)
        
        frButtons = ttk.Frame(master)
        frButtons.grid(column = 1, row=0, padx=5, pady=5, sticky=form.N)

        ttk.Button(frButtons, text="Add new", width=15, command=self.addNewItinerary).grid(column=0, row=0, padx=2, pady=2)
        ttk.Button(frButtons, text="Edit", width=15, command=self.editItinerary).grid(column=0, row=1, padx=2, pady=2)
        ttk.Button(frButtons, text="Delete", width=15, command=self.deleteItinerary).grid(column=0, row=2, padx=2, pady=2)

        #TODO: add two buttons to change order? (up/down)

        frItineraryDetail = ttk.LabelFrame(master, text="Details")
        frItineraryDetail.grid(column=0, row=1, columnspan=2, padx=5, pady=5, sticky=form.W)

        self.lblProperties = ttk.Label(frItineraryDetail, width=40)
        self.lblProperties.grid(column=0, row=0, padx=3, pady=3)

    def addNewItinerary(self):
        newItinerary = Itinerary()
        print("b4", newItinerary.aaa)
        guiItineraryNew(self, newItinerary)
        print("after", newItinerary.aaa)

    def editItinerary(self):
        pass

    def deleteItinerary(self):
        pass

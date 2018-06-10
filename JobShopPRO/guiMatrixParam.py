import tkinter as form
from tkinter import ttk
from tkinter import messagebox as msg
from globalData import STRGS
from guiMatrixInput import GuiMatrixInput
import sys
#=========================================================================================

class GuiMatrixParam(form.Toplevel):
    """Form to get number of itineraries and machines"""

    def __init__(self, master, arrAmount):
        form.Toplevel.__init__(self, master)

        self.title("Enter input data")
        #center window in the middle of the screen
        self.geometry("%dx%d+%d+%d" % (250,140, int(master.winfo_screenwidth() / 2 - 250 / 2), int(master.winfo_screenheight() / 2 - 140 / 2)))
        self.resizable(False, False)

        frInput = ttk.LabelFrame(self, text="Enter input data")
        frInput.pack(padx=5, pady=5)

        ttk.Label(frInput, text="Number of machines:").grid(column=0, row=0, padx=5, pady=5)
        ttk.Label(frInput, text="Number of itineraries:").grid(column=0, row=1, padx=5, pady=5)

        vcmd = (master.register(self.validateNumbers), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.spbMachinesQuant = form.Spinbox(frInput, width=7, from_=3, to=100, validate='key', validatecommand = vcmd)
        self.spbMachinesQuant.grid(column=1, row=0, padx=3, pady=3)

        self.spbItinerariesQuant = form.Spinbox(frInput, width=7, from_=2, to=100, validate='key', validatecommand = vcmd)
        self.spbItinerariesQuant.grid(column=1, row=1, padx=3, pady=3)

        form.Button(self, text="OK", width=20, command=lambda arg=arrAmount: self.createMatrix(arg)).pack(padx=5, pady=5)
        self.bind('<Return>', lambda event, arg=arrAmount: self.createMatrix(arg))
        self.bind('<Escape>', lambda event: self.destroy())
        
        #set this window to be on top
        self.grab_set()
        self.focus_set()

    def createMatrix(self, arrAmount):
        """Gets values for spinboxes """
        try:
            arrAmount[0] = int(float(self.spbMachinesQuant.get()))
            arrAmount[1] = int(float(self.spbItinerariesQuant.get()))
            if len(str(arrAmount[1])) != 0 and len(str(arrAmount[0])) !=0:
                if arrAmount[1] != 0 and arrAmount[0] != 0:
                    self.destroy()
                else:
                    msg.showerror("is zero")                
        except ValueError:
            msg.showerror("empty")

    def validateNumbers(self, action, index, valueIfAllowed, priorValue, text, validationType, triggerType, widgetName):
        """Preserve to enter only specified keys into entry """
        if(len(valueIfAllowed) >3): #no longer than 3 digits
            return False
        elif(action == '1'): #Type of action (1=insert, 0=delete, -1 for others)
            if text in '0123456789':
                try:
                    float(valueIfAllowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True
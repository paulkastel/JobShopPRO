import tkinter as form
from tkinter import ttk
from tkinter import messagebox as msg
from globalData import STRGS
from guiMatrixInput import GuiMatrixInput
import sys
#=========================================================================================

class GuiMatrixParam(form.Toplevel):
    """Form to get number of itineraries and machines"""

    def __init__(self, master):
        form.Toplevel.__init__(self, master)

        self.master = master
        self.title("Enter input data")
        #center window in the middle of the screen
        self.geometry("%dx%d+%d+%d" % (250,140, int(master.winfo_screenwidth() / 2 - 250 / 2), int(master.winfo_screenheight() / 2 - 140 / 2)))
        self.resizable(False, False)

        frInput = ttk.LabelFrame(self, text="Enter input data")
        frInput.pack(padx=5, pady=5)

        ttk.Label(frInput, text="Number of itineraries:").grid(column=0, row=0, padx=5, pady=5)
        ttk.Label(frInput, text="Number of machines:").grid(column=0, row=1, padx=5, pady=5)

        vcmd = (master.register(self.validateNumbers), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.spbItinerariesQuant = form.Spinbox(frInput, width=7, from_=1, to=sys.maxsize, validate='key', validatecommand = vcmd)
        self.spbItinerariesQuant.grid(column=1, row=0, padx=3, pady=3) 

        vcmd = (master.register(self.validateNumbers), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.spbMachinesQuant = form.Spinbox(frInput, width=7, from_=1, to=sys.maxsize, validate='key', validatecommand = vcmd)
        self.spbMachinesQuant.grid(column=1, row=1, padx=3, pady=3) 

        form.Button(self, text="OK", width=20, command=self.createMatrix).pack(padx=5, pady=5)
        
        #set this window to be on top
        self.grab_set()
        self.focus()

    def createMatrix(self):
        try:
            mach = int(self.spbMachinesQuant.get())
            itin = int(self.spbItinerariesQuant.get())
            if len(str(itin)) != 0 and len(str(mach)) !=0:
                if itin != 0 and mach != 0:
                    GuiMatrixInput(self, mach, itin)
                    self.withdraw()
                else:
                    msg.showerror("is zero")                
        except ValueError:
            msg.showerror("empty")

       

    def validateNumbers(self, action, index, valueIfAllowed, priorValue, text, validationType, triggerType, widgetName):
        """Preserve to enter only specified keys into entry """
        if(action == '1'): #user can delete input e.g. erase wrong number and enter it again
            if text in '0123456789.':
                try:
                    float(valueIfAllowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True
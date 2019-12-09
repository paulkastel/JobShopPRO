import tkinter as form
from tkinter import ttk
from tkinter import messagebox as msg
from globalData import STRGS, validateOnlyInt
from guiMatrixInput import GuiMatrixInput
#=========================================================================================
class GuiMatrixParam(form.Toplevel):
    """Form to get number of itineraries and machines"""

    def __init__(self, master, arrAmount):
        form.Toplevel.__init__(self, master)

        self.title(STRGS['ENTER_MATRIX_DATA'])
        #center window in the middle of the screen
        self.geometry("%dx%d+%d+%d" % (280,140, int(master.winfo_screenwidth() / 2 - 280 / 2), int(master.winfo_screenheight() / 2 - 140 / 2)))
        self.resizable(False, False)

        frInput = ttk.LabelFrame(self, text=STRGS['ENTER_MATRIX_DATA'])
        frInput.pack(padx=5, pady=5)

        ttk.Label(frInput, text=STRGS['NUM_MACHS']).grid(column=0, row=0, padx=5, pady=5)
        ttk.Label(frInput, text=STRGS['NUM_ITINERS']).grid(column=0, row=1, padx=5, pady=5)

        vcmd = (master.register(validateOnlyInt), self, '%d', '%i', '%P', 3, '%s', '%S', '%v', '%V', '%W')
        self.spbMachinesQuant = form.Spinbox(frInput, width=7, from_=1, to=999, validate='key', validatecommand = vcmd)
        self.spbMachinesQuant.grid(column=1, row=0, padx=3, pady=3)

        self.spbItinerariesQuant = form.Spinbox(frInput, width=7, from_=1, to=999, validate='key', validatecommand = vcmd)
        self.spbItinerariesQuant.grid(column=1, row=1, padx=3, pady=3)

        form.Button(self, text=STRGS['OK'], width=20, command=lambda arg=arrAmount: self.createMatrix(arg)).pack(padx=5, pady=5)
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
            if len(str(arrAmount[1])) != 0 and len(str(arrAmount[0])) != 0:
                if arrAmount[1] != 0 and arrAmount[0] != 0:
                    self.destroy()
                else:
                    msg.showerror(STRGS['ERR'],STRGS['MSG_ERR_VALUE_NO_ZERO'])                
        except ValueError:
            msg.showerror(STRGS['ERR'],STRGS['MSG_ERR_EMPTY_VAL'])
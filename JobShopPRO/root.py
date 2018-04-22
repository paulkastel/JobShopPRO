import tkinter as form
from guiItinerary import GuiItinerary
from guiMachine import GuiMachine
#=========================================================================================
def main():
    """ MAIN FUNCTION """
    root = form.Tk()
    app = GuiItinerary(root)
    root.mainloop()

if __name__ == '__main__':
    main()
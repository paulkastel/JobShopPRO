import tkinter as form
from guiMain import GuiMain
#=========================================================================================
def main():
    """MAIN FUNCTION """
    root = form.Tk()
    app = GuiMain(root)
    root.mainloop()

if __name__ == '__main__':
    main()
    exit()

    #TODO: database sqlite
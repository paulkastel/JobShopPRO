#=========================================================================================
class Machine():
    """Machine in factory - properties"""
   
    def __init__(self, aName):
        self.name = aName

    def exportToDict(self):
        """Serialize information about Machine into dictionary"""
        exData = {}
        exData['machineName'] = self.name
        return exData
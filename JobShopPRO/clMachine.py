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

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return self.name
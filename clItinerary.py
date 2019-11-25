#=========================================================================================
class Itinerary():
    """Itinerary is a list of ordered tasks """

    def __init__(self):
        self.name = ""
        self.itineraryChanged = False
        self.tasksList = []

    def exportToDict(self):
        """Serialize information about Itinerary into dictionary"""
        exData = {}
        exData['itineraryName'] = self.name
        exData['tasksList'] = []
        for t in self.tasksList:
            exData['tasksList'].append(t.exportToDict())
        return exData

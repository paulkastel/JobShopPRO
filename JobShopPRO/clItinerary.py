#=========================================================================================
class Itinerary():
    """Itinerary is a list of ordered tasks """

    def __init__(self):
        self.name = ""
        self.itineraryChanged = False
        self.tasksList = []

#=========================================================================================
class Task():
    """Task is a part of Itinerary """

    def __init__(self, aName, aDuration, aMachine):
        self.name = aName
        self.duration = aDuration
        self.machine = aMachine
        self.taskChanged = False

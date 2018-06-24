#=========================================================================================
class Job():
    """Represent job to-do in schedule"""

    def __init__(self, aItineraryName, aItineraryColor, aTaskNumber, aItineraryNumber, aMachineName, aMachineID, aDuration):
        self.itinerary = aItineraryName
        self.machine = aMachineName
        self.machineID = aMachineID
        self.startTime = 0
        self.duration = aDuration
        self.endTime = 0
        self.colorOfItinerary = aItineraryColor
        self.idOperation = aTaskNumber
        self.idItinerary = aItineraryNumber
        self.completed = False
        self.priority = 0

    def __eq__(self, other):
        return self.itinerary == other.itinerary and self.colorOfItinerary == other.colorOfItinerary and self.machine == other.machine and self.duration == other.duration and self.completed == other.completed and self.idOperation == other.idOperation

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return "Job" + str(self.idItinerary) + "_" + str(self.idOperation) + " Machine:" + self.machine + "Duration: " + str(self.duration)

    def getTupleStartAndDuration(self):
        return (self.startTime, self.duration)

    def getEndTime(self):
        self.endTime = self.startTime + self.duration
        return self.endTime

#=========================================================================================
class Job():
    """Represent job to-do in schedule"""

    def __init__(self, aItineraryName, aItineraryColor, aTaskNumber, aItineraryNumber, aMachineName, aDuration):
        self.itinerary = aItineraryName
        self.machine = aMachineName
        self.startTime = 0
        self.duration = aDuration
        self.endTime = 0
        self.colorOfItinerary = aItineraryColor
        self.idOperation = aTaskNumber
        self.idItinerary = aItineraryNumber
        self.itineraryEndTime = 0
        self.completed =False

    def getTupleStartAndDuration(self):
        return (self.startTime, self.duration)

    def getEndTime(self):
        self.endTime = self.startTime+self.duration
        return self.endTime

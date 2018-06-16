from globalData import *
from clJob import Job
import random
#=========================================================================================
def prepareJobs():
    """Converts available data to list of jobs on which is calculations and graphs made"""
    global machinesList, itinerariesList

    jobsList = []
    itineraryColors = []

    pastelFactor = random.uniform(0, 1)
    #parse all tasks from all itineraries
    for idItinerary, itineraryObj in enumerate(itinerariesList):
        itineraryColors.append(generate_new_color(itineraryColors, pastelFactor)) #create new color for every new itinerary
        for idTask, taskObj in enumerate(itineraryObj.tasksList):
            jobsList.append(Job(itineraryObj.name, itineraryColors[idItinerary], idTask + 1, idItinerary + 1, taskObj.machine.name, taskObj.duration))
    return jobsList

def algorithmLIFO(aJobsList):
    print("TODO: LIFO ")
    return aJobsList


def algorithmFIFO(aJobsList):
    """
    FIFO/FCFS heuristic algorithm for job shop problem
    """
    global machinesList, itinerariesList
    jobsListToExport = []
    tmp = []

    curMachinesTime = {}
    curItinerariesTime = {}

    for m in machinesList:
        curMachinesTime[m.name] = 0

    for i in itinerariesList:
        curItinerariesTime[i.name] = 0

    #===== FIFO =====
    while len(jobsListToExport) != len(aJobsList): #repeat until all task are assigned somewhere
        for mach in machinesList:
            tmp = [job for job in aJobsList if job.machine == mach.name]
            tmp.sort(key=lambda j: j.idOperation)

        for mach in machinesList:
            tmp = [job for job in aJobsList if job.machine == mach.name and job.completed == False]     
            if len(tmp):
                for t in tmp:
                    t.itineraryEndTime = curItinerariesTime[t.itinerary]
                tmp.sort(key=lambda j: j.itineraryEndTime)

                for job in tmp:
                    #go check ahead all jobs to do for this machine
                    allJobsInItinerary = [j for j in aJobsList if j.itinerary == job.itinerary]
                    if job.idOperation > 1:
                        for t in tmp:
                            t.itineraryEndTime = curItinerariesTime[t.itinerary]
                        tmp.sort(key=lambda j: j.itineraryEndTime)
                        if allJobsInItinerary[job.idOperation - 2].completed:
                            #if current time in machine > than previous finished element
                            if curMachinesTime[job.machine] > allJobsInItinerary[job.idOperation - 2].endTime:
                                job.startTime = curMachinesTime[job.machine]
                            else:
                                job.startTime = allJobsInItinerary[job.idOperation - 2].endTime
                            job.completed = True
                            curItinerariesTime[job.itinerary] = job.getEndTime()
                            curMachinesTime[job.machine] = job.getEndTime()
                            jobsListToExport.append(job)
                            break
                    else:
                        #do this only for first elements in itineraries
                        if job.idOperation == 1 :
                            job.startTime = curMachinesTime[job.machine]
                            job.completed = True
                            curItinerariesTime[job.itinerary] = job.getEndTime()
                            job.itineraryEndTime = job.getEndTime()
                            curMachinesTime[job.machine] = job.duration + curMachinesTime[job.machine] 
                            jobsListToExport.append(job)
                            break
                tmp.clear()
    return jobsListToExport

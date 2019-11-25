from globalData import *
from clJob import Job
from copy import deepcopy
import random
#from numpy.random import choice
from sortedcollections import SortedDict
# Import Python wrapper for or-tools constraint solver.
from ortools.constraint_solver import pywrapcp

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
            for index, mach in enumerate(machinesList):
                if mach.name == taskObj.machine.name:
                    jobsList.append(Job(itineraryObj.name, itineraryColors[idItinerary], idTask + 1, idItinerary + 1, taskObj.machine.name, index, taskObj.duration))
                    break
    return jobsList

def algorithmSPT(aJobsList):
    """
    SPT/SJF heuristic algorithm for job shop problem
    """

    time = {}
    waitingOperations = {}
    currentTimeOnMachines = {}
    jobsListToExport = []

    #initialize machines times and get 
    #first waiting operations for each machine
    global machinesList
    for machine in machinesList:
        waitingOperations[machine.name] = [job for job in aJobsList if job.machine == machine.name and job.idOperation == 1]
        waitingOperations[machine.name].sort(key=lambda j: j.duration)
        currentTimeOnMachines[machine.name] = 0

    time[0] = waitingOperations

    for keyMach, operations in waitingOperations.items():
        #for each waiting task in front of machine set time to 0, update
        #properties
        if len(operations):

            operations[0].startTime = 0
            operations[0].completed = True

            #push task to production, and create new event to stop at,
            #on ending time, then update machines time
            jobsListToExport.append(operations[0])
            currentTimeOnMachines[keyMach] = operations[0].getEndTime()
            time[currentTimeOnMachines[keyMach]] = {}

    while len(jobsListToExport) != len(aJobsList):
        for t, operations in time.items():
            operations = getWaitingOperationsSPT(aJobsList, float(t))

            for keyMach, tasks in operations.items():
                if len(tasks):
                    if float(t) < currentTimeOnMachines[tasks[0].machine]:
                        continue

                    tasks[0].startTime = float(t)
                    tasks[0].completed = True

                    jobsListToExport.append(tasks[0])
                    
                    currentTimeOnMachines[keyMach] = tasks[0].getEndTime()
                    time[currentTimeOnMachines[keyMach]] = {}  

            del time[t]
            break

        time = SortedDict(time) #chronological order

    return jobsListToExport

def getWaitingOperationsSPT(aJobsList, time):
    """Get waiting jobs at current time in shortest duration order"""

    incomingOperations = {}
    assignedJobsForMachine = []

    global machinesList
    for mach in machinesList:
        assignedJobsForMachine = [job for job in aJobsList if job.completed == False and job.machine == mach.name]
        incomingOperations[mach.name] = []

        for j in assignedJobsForMachine:
            if j.idOperation == 1:
                incomingOperations[mach.name].append(j)
            else:
                previousTask = [job for job in aJobsList if job.itinerary == j.itinerary and job.idOperation == j.idOperation - 1 and job.endTime <= time ]
                if len(previousTask):
                    if previousTask[0].completed:
                        incomingOperations[mach.name].append(j)
        #sort added jobs by duration
        incomingOperations[mach.name].sort(key=lambda j: j.duration)
    return incomingOperations

def algorithmLPT(aJobsList):
    """
    LPT/LJF heuristic algorithm for job shop problem
    """

    time = {}
    waitingOperations = {}
    currentTimeOnMachines = {}
    jobsListToExport = []

    #initialize machines times and get first 
    #waiting operations for each machine
    global machinesList
    for machine in machinesList:
        waitingOperations[machine.name] = [job for job in aJobsList if job.machine == machine.name and job.idOperation == 1]
        waitingOperations[machine.name].sort(key=lambda j: j.duration, reverse=True)
        currentTimeOnMachines[machine.name] = 0

    time[0] = waitingOperations

    for keyMach, operations in waitingOperations.items():
        #for each waiting task in front of machine set time to 0, update
        #properties
        if len(operations):

            operations[0].startTime = 0
            operations[0].completed = True

            #push task to production, and create new event to stop at, at
            #on ending time, then update machines time
            jobsListToExport.append(operations[0])
            currentTimeOnMachines[keyMach] = operations[0].getEndTime()
            time[currentTimeOnMachines[keyMach]] = {}

    while len(jobsListToExport) != len(aJobsList):
        for t, operations in time.items():
            operations = getWaitingOperationsLPT(aJobsList, float(t))

            for keyMach, tasks in operations.items():
                if len(tasks):
                    if float(t) < currentTimeOnMachines[tasks[0].machine]:
                        continue

                    tasks[0].startTime = float(t)
                    tasks[0].completed = True

                    jobsListToExport.append(tasks[0])
                    
                    currentTimeOnMachines[keyMach] = tasks[0].getEndTime()
                    time[currentTimeOnMachines[keyMach]] = {}  

            del time[t]
            break

        time = SortedDict(time) #chronological order

    return jobsListToExport

def getWaitingOperationsLPT(aJobsList, time):
    """Get waiting jobs at current time in the longest duration order"""

    incomingOperations = {}
    assignedJobsForMachine = []

    global machinesList
    for mach in machinesList:
        assignedJobsForMachine = [job for job in aJobsList if job.completed == False and job.machine == mach.name]
        incomingOperations[mach.name] = []

        for j in assignedJobsForMachine:
            if j.idOperation == 1:
                incomingOperations[mach.name].append(j)
            else:
                previousTask = [job for job in aJobsList if job.itinerary == j.itinerary and job.idOperation == j.idOperation - 1 and job.endTime <= time ]
                if len(previousTask):
                    if previousTask[0].completed:
                        incomingOperations[mach.name].append(j)
        #sort added jobs by duration
        incomingOperations[mach.name].sort(key=lambda j: j.duration, reverse=True)

    return incomingOperations

def algorithmFIFO(aJobsList):
    """
    FIFO/FCFS heuristic algorithm for job shop problem
    """

    time = {}
    waitingOperations = {}
    recentOperations = {}
    currentTimeOnMachines = {}
    jobsListToExport = []

    global machinesList
    for machine in machinesList:
        waitingOperations[machine.name] = [job for job in aJobsList if job.machine == machine.name and job.idOperation == 1]
        currentTimeOnMachines[machine.name] = 0

    time[0] = waitingOperations
    recentOperations = deepcopy(waitingOperations)

    for keyMach, operations in waitingOperations.items():
        #for each waiting task in front of machine set time to 0, update
        #properties
        if len(operations):
            for job in aJobsList:
                if job == operations[0]:
                    job.completed = True
                    job.startTime = 0
                    job.getEndTime()

            operations[0].startTime = 0
            operations[0].completed = True

            #push task to production, and create new event to stop at,
            #on ending time, then update machines time
            jobsListToExport.append(operations[0])
            currentTimeOnMachines[keyMach] = operations[0].getEndTime()

            del recentOperations[keyMach][0]
            time[currentTimeOnMachines[keyMach]] = {}

    while len(jobsListToExport) != len(aJobsList):
        for t, operations in time.items():
            operations = deepcopy(getWaitingOperationsFIFO(aJobsList, float(t), recentOperations))

            for keyMach, tasks in operations.items():
                if len(tasks):
                    if float(t) < currentTimeOnMachines[tasks[0].machine]:
                        continue

                    for job in aJobsList:
                        if job == tasks[0]:
                            job.completed = True
                            job.startTime = float(t)
                            job.getEndTime()

                    tasks[0].startTime = float(t)
                    tasks[0].completed = True

                    jobsListToExport.append(tasks[0])

                    del recentOperations[keyMach][0]
                    currentTimeOnMachines[keyMach] = tasks[0].getEndTime()
                    time[currentTimeOnMachines[keyMach]] = {}
                    
            del time[t]
            break

        time = SortedDict(time) #chronological order

    return jobsListToExport

def getWaitingOperationsFIFO(aJobsList, aTime, aRecentOp):
    """Get waiting jobs at current time in FIFO order"""

    for mach in machinesList:
        assignedJobsForMachine = [job for job in aJobsList if job.completed == False and job.machine == mach.name]

        for j in assignedJobsForMachine:
            if j.idOperation == 1 and j not in aRecentOp[mach.name]:
                aRecentOp[mach.name].append(j)
            else:
                previousTask = [job for job in aJobsList if job.itinerary == j.itinerary and job.idOperation == j.idOperation - 1 and job.endTime <= aTime ]
                if len(previousTask):
                    if previousTask[0].completed and j not in aRecentOp[mach.name]:
                        aRecentOp[mach.name].append(j)

    return aRecentOp

def algorithmLIFO(aJobsList):
    """
    LIFO/LCFS heuristic algorithm for job shop problem
    """

    time = {}
    waitingOperations = {}
    recentOperations = {}
    currentTimeOnMachines = {}
    jobsListToExport = []

    global machinesList
    for machine in machinesList:
        waitingOperations[machine.name] = [job for job in aJobsList if job.machine == machine.name and job.idOperation == 1]
        currentTimeOnMachines[machine.name] = 0

    time[0] = waitingOperations
    recentOperations = deepcopy(waitingOperations)

    for keyMach, operations in waitingOperations.items():
        #for each waiting task in front of machine set time to 0, update
        #properties
        if len(operations):
            for job in aJobsList:
                if job == operations[0]:
                    job.completed = True
                    job.startTime = 0
                    job.itineraryEndTime = job.getEndTime()

            operations[0].startTime = 0
            operations[0].completed = True

            #push task to production, and create new event to stop at,
            #on ending time, then update machines time
            jobsListToExport.append(operations[0])
            currentTimeOnMachines[keyMach] = operations[0].getEndTime()

            del recentOperations[keyMach][0]
            time[currentTimeOnMachines[keyMach]] = {}

    while len(jobsListToExport) != len(aJobsList):
        for t, operations in time.items():
            operations = deepcopy(getWaitingOperationsLIFO(aJobsList, float(t), recentOperations))

            for keyMach, tasks in operations.items():
                if len(tasks):
                    if float(t) < currentTimeOnMachines[tasks[0].machine]:
                        continue

                    for job in aJobsList:
                        if job == tasks[0]:
                            job.completed = True
                            job.startTime = float(t)
                            job.itineraryEndTime = job.getEndTime()

                    tasks[0].startTime = float(t)
                    tasks[0].completed = True

                    jobsListToExport.append(tasks[0])
                    del recentOperations[keyMach][0]

                    currentTimeOnMachines[keyMach] = tasks[0].getEndTime()
                    time[currentTimeOnMachines[keyMach]] = {}  

            del time[t]
            break

        time = SortedDict(time) #chronological order

    return jobsListToExport

def getWaitingOperationsLIFO(aJobsList, aTime, aRecentOp):
    """Get waiting jobs at current time in LIFO order"""

    global machinesList
    for mach in machinesList:
        assignedJobsForMachine = [job for job in aJobsList if job.completed == False and job.machine == mach.name]
        assignedJobsForMachine = list(reversed(assignedJobsForMachine)) #reverse all tasks to get last tasks first

        for j in assignedJobsForMachine:       
            previousTask = [job for job in aJobsList if job.itinerary == j.itinerary and job.idOperation == j.idOperation - 1 and job.endTime <= aTime ]

            if len(previousTask):
                if previousTask[0].completed and j not in aRecentOp[mach.name]:   
                    aRecentOp[mach.name].insert(0, j)

    return aRecentOp

def randomSolutionByPriority(aJobsList):
    """
    Choose jobs in random order for job shop problem (worst case scenario)
    """

    time = {}
    waitingOperations = {}
    currentTimeOnMachines = {}
    jobsListToExport = []

    #initialize machines times and get first 
    #waiting operations for each machine
    global machinesList
    for machine in machinesList:
        waitingOperations[machine.name] = [job for job in aJobsList if job.machine == machine.name and job.idOperation == 1]
        currentTimeOnMachines[machine.name] = 0

    time[0] = waitingOperations

    for keyMach, operations in waitingOperations.items():
        #for each waiting task in front of machine set time to 0, 
        #update properties
        if len(operations):
            #r = choice(len(operations),1,p=[j.priority for j in operations])
            r = random.choices(range(0, len(operations)), weights=[j.priority for j in operations])
            operations[r[0]].startTime = 0
            operations[r[0]].completed = True

            #push task to production, and create new event to stop at, 
            #on ending time, then update machines time
            jobsListToExport.append(operations[r[0]])
            currentTimeOnMachines[keyMach] = operations[r[0]].getEndTime()
            time[currentTimeOnMachines[keyMach]] = {}

    while len(jobsListToExport) != len(aJobsList):
        for t, operations in time.items():
            #doesnt really matter the order if you choose random operation from it
            operations = getWaitingOperationsLPT(aJobsList, float(t))

            for keyMach, tasks in operations.items():
                if len(tasks):
                    #if more than 1 operation in queue, choose the random one
                    r = random.choices(range(0, len(tasks)), weights=[j.priority for j in tasks])
                    if float(t) < currentTimeOnMachines[tasks[r[0]].machine]:
                        continue               
                    tasks[r[0]].startTime = float(t)
                    tasks[r[0]].completed = True

                    jobsListToExport.append(tasks[r[0]])
                    
                    currentTimeOnMachines[keyMach] = tasks[r[0]].getEndTime()
                    time[currentTimeOnMachines[keyMach]] = {}  

            del time[t]
            break
        time = SortedDict(time) #chronological order
    return jobsListToExport

def randomSolution(aJobsList):
    """
    Choose jobs in random order for job shop problem (worst case scenario)
    """

    time = {}
    waitingOperations = {}
    currentTimeOnMachines = {}
    jobsListToExport = []

    #initialize machines times and get first 
    #waiting operations for each machine
    global machinesList
    for machine in machinesList:
        waitingOperations[machine.name] = [job for job in aJobsList if job.machine == machine.name and job.idOperation == 1]
        currentTimeOnMachines[machine.name] = 0

    time[0] = waitingOperations

    for keyMach, operations in waitingOperations.items():
        #for each waiting task in front of machine set time to 0, 
        #update properties
        if len(operations):
            r = random.randint(0, len(operations) - 1)
            operations[r].startTime = 0
            operations[r].completed = True

            #push task to production, and create new event to stop at, 
            #on ending time, then update machines time
            jobsListToExport.append(operations[r])
            currentTimeOnMachines[keyMach] = operations[r].getEndTime()
            time[currentTimeOnMachines[keyMach]] = {}

    while len(jobsListToExport) != len(aJobsList):
        for t, operations in time.items():
            #doesnt really matter the order if you choose random operation from it
            operations = getWaitingOperationsLPT(aJobsList, float(t))

            for keyMach, tasks in operations.items():
                if len(tasks):
                    #if more than 1 operation in queue, choose the random one
                    r = random.randint(0, len(tasks) - 1) 
                    if float(t) < currentTimeOnMachines[tasks[r].machine]:
                        continue               
                    tasks[r].startTime = float(t)
                    tasks[r].completed = True

                    jobsListToExport.append(tasks[r])
                    
                    currentTimeOnMachines[keyMach] = tasks[r].getEndTime()
                    time[currentTimeOnMachines[keyMach]] = {}  

            del time[t]
            break
        time = SortedDict(time) #chronological order
    return jobsListToExport

def algorithmPriority(aJobsList):
    """
    Priority heuristic algorithm for job shop problem
    """

    time = {}
    waitingOperations = {}
    currentTimeOnMachines = {}
    jobsListToExport = []

    #initialize machines times and get first 
    #waiting operations for each machine
    global machinesList
    for machine in machinesList:
        waitingOperations[machine.name] = [job for job in aJobsList if job.machine == machine.name and job.idOperation == 1]
        waitingOperations[machine.name].sort(key=lambda j: j.priority)
        currentTimeOnMachines[machine.name] = 0

    time[0] = waitingOperations

    for keyMach, operations in waitingOperations.items():
        #for each waiting task in front of machine set time to 0, update
        #properties
        if len(operations):

            operations[0].startTime = 0
            operations[0].completed = True

            #push task to production, and create new event to stop at, at
            #on ending time, then update machines time
            jobsListToExport.append(operations[0])
            currentTimeOnMachines[keyMach] = operations[0].getEndTime()
            time[currentTimeOnMachines[keyMach]] = {}

    while len(jobsListToExport) != len(aJobsList):
        for t, operations in time.items():
            operations = getWaitingOperationsPriority(aJobsList, float(t))

            for keyMach, tasks in operations.items():
                if len(tasks):
                    if float(t) < currentTimeOnMachines[tasks[0].machine]:
                        continue

                    tasks[0].startTime = float(t)
                    tasks[0].completed = True

                    jobsListToExport.append(tasks[0])
                    
                    currentTimeOnMachines[keyMach] = tasks[0].getEndTime()
                    time[currentTimeOnMachines[keyMach]] = {}  

            del time[t]
            break

        time = SortedDict(time) #chronological order

    return jobsListToExport

def getWaitingOperationsPriority(aJobsList, time):
    """Get waiting jobs at current time in the longest duration order"""

    incomingOperations = {}
    assignedJobsForMachine = []

    global machinesList
    for mach in machinesList:
        assignedJobsForMachine = [job for job in aJobsList if job.completed == False and job.machine == mach.name]
        incomingOperations[mach.name] = []

        for j in assignedJobsForMachine:
            if j.idOperation == 1:
                incomingOperations[mach.name].append(j)
            else:
                previousTask = [job for job in aJobsList if job.itinerary == j.itinerary and job.idOperation == j.idOperation - 1 and job.endTime <= time ]
                if len(previousTask):
                    if previousTask[0].completed:
                        incomingOperations[mach.name].append(j)
        #sort added jobs by duration
        incomingOperations[mach.name].sort(key=lambda j: j.priority)

    return incomingOperations

def optimalSolution(aJobList):
    """
    Solves job problem with google optimization tools
    """
    solver = pywrapcp.Solver('jobshop')
    jobsListToExport = []
    machines_count = len(machinesList)
    jobs_count = len(itinerariesList)
    all_machines = range(0, machines_count)
    all_jobs = range(0, jobs_count)

    processing_times = []
    machines = []

    for itin in itinerariesList:
        tmpDur = [job for job in aJobList if job.itinerary == itin.name]
        tmpDur.sort(key=lambda j: j.idOperation)
        machines.append([job.machineID for job in tmpDur])
        processing_times.append([int(job.duration) for job in tmpDur])
        tmpDur.clear()

    # Computes horizon.
    horizon = 0
    for i in all_jobs:
        horizon += sum(processing_times[i])
    # Creates jobs.
    all_tasks = {}
    for i in all_jobs:
        for j in range(0, len(machines[i])):
            all_tasks[(i, j)] = solver.FixedDurationIntervalVar(0, horizon, processing_times[i][j], False, 'Job_%i_%i' % (i, j))

    # Creates sequence variables and add disjunctive constraints.
    all_sequences = []
    all_machines_jobs = []
    for i in all_machines:
        machines_jobs = []
        for j in all_jobs:
            for k in range(0, len(machines[j])):
                if machines[j][k] == i:
                    machines_jobs.append(all_tasks[(j, k)])
        disj = solver.DisjunctiveConstraint(machines_jobs, 'machine %i' % i)
        all_sequences.append(disj.SequenceVar())
        solver.Add(disj)

    # Add conjunctive contraints.
    for i in all_jobs:
        for j in range(0, len(machines[i]) - 1):
            solver.Add(all_tasks[(i, j + 1)].StartsAfterEnd(all_tasks[(i, j)]))

    # Set the objective.
    obj_var = solver.Max([all_tasks[(i, len(machines[i]) - 1)].EndExpr() for i in all_jobs])
    objective_monitor = solver.Minimize(obj_var, 1)
    
    # Create search phases.
    sequence_phase = solver.Phase([all_sequences[i] for i in all_machines], solver.SEQUENCE_DEFAULT)
    vars_phase = solver.Phase([obj_var], solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE)
    main_phase = solver.Compose([sequence_phase, vars_phase])
    
    # Create the solution collector.
    collector = solver.LastSolutionCollector()

    # Add the interesting variables to the SolutionCollector.
    collector.Add(all_sequences)
    collector.AddObjective(obj_var)

    for i in all_machines:
        sequence = all_sequences[i]
        sequence_count = sequence.Size()
        for j in range(0, sequence_count):
            t = sequence.Interval(j)
            collector.Add(t.StartExpr().Var())
            collector.Add(t.EndExpr().Var())

    # Solve the problem
    if solver.Solve(main_phase, [objective_monitor, collector]):
        for i in all_machines:
            seq = all_sequences[i]
            sequence = collector.ForwardSequence(0, seq)
            seq_size = len(sequence)

            for j in range(0, seq_size):
                t = seq.Interval(sequence[j])
                name_arr = str(t.Name())
                
                x = [job for job in aJobList if int(name_arr.split("_")[1]) == job.idItinerary - 1 and int(name_arr.split("_")[2]) == job.idOperation - 1 and job.machineID == i]
                x[0].startTime = collector.Value(0, t.StartExpr().Var())
                x[0].endTime = collector.Value(0, t.EndExpr().Var())
                jobsListToExport.append(x[0])

    return jobsListToExport

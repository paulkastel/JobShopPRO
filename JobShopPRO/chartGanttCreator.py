import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.ticker as ticker
import tkinter as form
from math import fmod
from tkinter import messagebox as msg
import random
from globalData import machinesList, itinerariesList
#=========================================================================================
def createGanttChart(aFrame, aJobsList):
    """Creates graph in specified aFrame"""

    for widget in aFrame.winfo_children():
        widget.destroy()    #clear previous charts

    cMax = max([j.endTime for j in aJobsList])
    chartFig, ax = plt.subplots()
    ax.set_xlabel('Time', fontsize =14)       #description of axis and chart title
    ax.set_ylabel('Machines',fontsize =14)
    chartTitle = "Gantt chart\nCmax=" + str(cMax)
    
    for i, itin in enumerate(itinerariesList):
        arr = [job for job in aJobsList if job.itinerary == itin.name]
        arr.sort(key=lambda x: x.endTime)
        chartTitle = chartTitle + ", C" + str(i + 1) + "=" + str(arr[-1].endTime)
        if not fmod(i, 5) and i != 0:
            chartTitle = chartTitle + "\n"
    
    plt.title(chartTitle)

    #values for machines y axis
    machinesNamesRev = list(reversed([mach.name for mach in machinesList]))
    ax.set_yticklabels(machinesNamesRev)    #set labels as machines names in reversed order

    machinesTicksPos = [15]
    for i in range(len(machinesNamesRev[1:])):
        machinesTicksPos.append(machinesTicksPos[i] + 10) #machine increase this +10
    ax.set_yticks(machinesTicksPos)

    ax.set_ylim(5, machinesTicksPos[-1] + 10) #this is related with amout of machines and height (last machine+10) of chart.
    ax.set_xlim(0, cMax + 10)     #from zero to end time of last job (max end time in job.endtime list)
    
    #setting the legend (color and itinerary)
    legendsColors = []
    seen = set()
    uniqueItinerariesInJobList = [job for job in aJobsList if job.itinerary not in seen and not seen.add(job.itinerary)]
    for job in uniqueItinerariesInJobList:
        legendsColors.append(mpatches.Patch(color=job.colorOfItinerary, label=job.itinerary))      #legend color and name
    plt.legend(handles=legendsColors)
    
    seen = set()
    uniqueItinerariesInJobList = [job for job in aJobsList if job.machine not in seen and not seen.add(job.itinerary)]

    tuplesForMachineAxis = []
    colorsForMachineAxis = []
    for index, machLabel in enumerate(machinesNamesRev):
        for job in aJobsList:
            if job.machine == machLabel:
                tuplesForMachineAxis.append(job.getTupleStartAndDuration())
                colorsForMachineAxis.append(job.colorOfItinerary)
        ax.broken_barh(tuplesForMachineAxis, ((index + 1) * 10, 9), facecolors=colorsForMachineAxis)
        print(tuplesForMachineAxis)        
        tuplesForMachineAxis.clear()
        colorsForMachineAxis.clear()

    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))  #this is cosmetics to set unit to 10
    for label in ax.get_xticklabels()[::2]: #and show only every two ticks
        label.set_visible(False)

    ax.grid(True)
    canva = FigureCanvasTkAgg(chartFig, aFrame)     #adding chart to frame
    canva.show()
    canva.get_tk_widget().pack(side=form.TOP, fill =form.BOTH, expand=True)
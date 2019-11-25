import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.ticker as ticker
import tkinter as form
import numpy as np
import scipy.stats as stats
from math import fmod
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
        chartTitle = chartTitle + " C" + str(i + 1) + "=" + str(arr[-1].endTime)+","
        if not fmod(i, 10) and i != 0:
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
    plt.legend(handles=legendsColors, fontsize =9)
    
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
        tuplesForMachineAxis.clear()
        colorsForMachineAxis.clear()

    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))  #this is cosmetics to set unit to 10
    for label in ax.get_xticklabels()[::2]: #and show only every two ticks
        label.set_visible(False)

    ax.grid(True)
    canva = FigureCanvasTkAgg(chartFig, aFrame)     #adding chart to frame
    canva.draw()
    canva.get_tk_widget().pack(side=form.TOP, fill =form.BOTH, expand=True)


def createHistogram(aFrame, aYXList):
    """Draws histogram with Gaussian function in aFrame"""

    for widget in aFrame.winfo_children():
        widget.destroy()    #clear previous charts

    x=[]
    y=[]

    defaultVal = aYXList[0][1]
    aYXList.remove(aYXList[0])

    for data in aYXList:
        x.append(data[0])
        y.append(data[1])
    
    y.sort(reverse=True)
    seen = set() 

    # bins are used for histogram ticks 
    bins = [seen.add(val) or val for val in y if val not in seen]
    bins.sort(reverse=True)

    chartFig, ax = plt.subplots()
    plt.title("Influence of probability\n Default Cmax is "+str(defaultVal)+", Iterations: "+str(len(aYXList)))

    #use this to draw histogram of your data, red columns
    plt.hist(y,edgecolor='black', linewidth=1, align='left', bins=np.arange(min(bins)-5,max(bins)+5,5), color='r')  
    
    #x-axis labels
    plt.xticks(np.arange(min(bins)-5,max(bins)+5,5)) 
    ax.set_xlabel("Obtained Cmax time in iterations")

    #y-axis labels for histogram
    plt.ylabel('Amount of iterations', color='r')
    plt.tick_params('y', colors='r')
    #ax.set_yticks(np.arange(start=0, stop=(y.count(max(set(y), key=y.count))+5)))
    
    #second chart
    ax2 =plt.twinx()

    #gaussian function
    ax = stats.norm.pdf(y, np.mean(y), np.std(y)) 
    plt.plot(y,ax,'b')

    plt.ylabel("Probability density", color='b')
    plt.tick_params('y', colors='b')
    
    chartFig.tight_layout()

    canva = FigureCanvasTkAgg(chartFig, aFrame)     #adding chart to frame
    canva.draw()
    canva.get_tk_widget().pack(side=form.TOP, fill =form.BOTH, expand=True)


def createScatter(aFrame, aYXList):
    """Draws histogram with Gaussian function in aFrame"""

    for widget in aFrame.winfo_children():
        widget.destroy()    #clear previous charts

    x=[]
    y=[]
    ymin=[]
    xmin=[]
    defaultVal = aYXList[0][1]

    chartFig, ax = plt.subplots()
    plt.title("Result of scheduling in iterations\n Default Cmax is "+str(defaultVal)+", Iterations: "+str(len(aYXList)-1))   
    minVal = defaultVal
    ymin.append(defaultVal)
    xmin.append(0)
    aYXList.remove(aYXList[0])

    for i, data in enumerate(aYXList):
        x.append(data[0])
        y.append(data[1])
        if (y[i] <=defaultVal):
            ymin.append(y[i])
            xmin.append(x[i])
            defaultVal = y[i]

   
    plt.scatter(x, y, label='skitscat', color='b', s=1)
    plt.xlabel("Iterations")
    plt.ylabel('Cmax')
    plt.ylim((min(y)-5, max(y)+5))

    #second chart
    ax2 =plt.twinx()
    plt.plot(xmin, ymin, color='green')
    plt.ylim((min(y)-5, max(y)+5))
    plt.ylabel("Minimal values", color='green')
    chartFig.tight_layout()
    canva = FigureCanvasTkAgg(chartFig, aFrame)     #adding chart to frame
    canva.draw()
    canva.get_tk_widget().pack(side=form.TOP, fill =form.BOTH, expand=True)
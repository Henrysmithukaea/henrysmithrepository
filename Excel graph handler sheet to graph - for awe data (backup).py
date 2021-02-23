# henry.smith@ukaea.uk. Version 0.1.1

                                           ##### READ ME #####

# This is a python script - some text that can be copied and pasted into a python terminal.
# It does the following:
# - Reads each sheet of an excel spreadsheet. For each sheet you choose, it makes an overlaid plot of the data in that sheet
# - Takes one data point from each sheet in the spreadsheet and overlays them all in a histogram.
# - Takes one column from each sheet in the spreadsheet and overlays them all in one final plot.
# - Saves all the graphs as pngs in an output folder

# The python terminal interprets the python script as a list of instructions. For example, I could write:
##### print ('hello world') 
# The python terminal would interpret this as an instruction to write the phrase 'hello world'
# Alternately, we can "define" a particular variable as 'hello world', and then ask for that variable to be printed.
# For example:
##### horse = 'hello world'
##### print (horse)
# We just wrote that horse = 'hello world'. Therefore, this would also make the python terminal write the phrase 'hello world'. 


# Below is a customisable list of "defines". In order to use this script, there are two defines that must be changed

# Please define 'filepath' as the filepath containing your excel spreadsheet(s). At the end, include '/*' to search for all spreadsheets in that folder, or write its name. 
filepath = 'N:\CCFE\H3AT\TritiumScience\Tritium Research\Tricem\Data\Science\Analysis/_AWE_*'

# Please define 'outputfolder' as the folder, where you'd like to save the .pngs that this script generates.
outputfolder = 'N:\CCFE\H3AT\TritiumScience\Tritium Research\Tricem\Data\Science\Analysis\ScienceRun3-D2\Output'

# Please define 'specific_sheets' as the list of numbers (or sheet names) containing your data in each spreadsheet, in squared brackets, separated by commas.
specific_sheets = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]

# Ordinarily, you will not need to make any further changes.
# There are further defines below. 

# Defines that are standardised by Yevhen and should not require any further updates

datacolumn = 1 			#The column in each sheet of the doc that contains the x data
Ydatacolumns = [3,4,5,6,7,8,9,10] 	#all columns in each sheet of the doc that contain Y data
header_row = 2 				#This defines the row that is expected to contain the column titles
histrow = 27 # the row containing data for the histogram in each sheet.Default 27
histcol = [14] # the column containing data for the histogram in each sheet.Default 14
smoothfactor =50 #window size for the rolling window average we take
colours = ("Yellow", "Green", "Blue", "Red", "Orange", "Purple", "Black", "Teal",
           "rosybrown", "salmon", "darkgoldenrod", "lightseagreen", "darkolivegreen", "saddlebrown", "cornflowerblue",
          "fuchsia", "grey", "darkslategray", "navy", "royalblue", "lightgreen", "mediumseagreen") # The script will cycle through this index colouring each new graph in a new colour
ignored_sheets = 2			#the number of sheets in the spreadsheet you don't want processed. All of these have to be reordered to appear at the end of the list of sheets. 

Ymultiplotcolumn = [11] #The column that you will use for the logarithmic comparison plot.
xinterceptofmultiplot = 100000000000000 # This is the X intercept of the logarithmic comparison plot.


# Import


import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.axes as axes
import matplotlib.patches as patches
import glob
from pathlib import Path


#Command defines. These can be modified if you wish to change the formatting of graphs

header_row_csv=2

def getcontentx(i, sname, colno):
    data = pd.read_excel(i, sheet_name = sname, usecols = [colno], header = header_row)
    indexeddata = [list(x) for x in zip(*data.values)]
    x = pd.Series(indexeddata[0]).rolling(window=10).mean()
    plt.xlabel(data.columns[0])  	# column header becomes the x axis title. You can replace this with any string you like.
    return x

def plotYandreturnlegendvalues(i, sname, colnos):
    data = pd.read_excel(i, sheet_name = sname, usecols = colnos, header = header_row)
    indexeddata = [list(x) for x in zip(*data.values)] #pulls out the data
    legendvalues = (data.columns)
    print (legendvalues)
    for column in range(len(colnos)): 
        y = pd.Series(indexeddata[column]).rolling(window=smoothfactor).mean() 		#pulls out a column in the data
        plt.plot(x, y, color =colours[column], linewidth = 1.5, alpha = 0.7) #  There's a lot of options here, e.g 'o' means it plots as dots. you may want to add 'color =colours[each], ' - this will then use the colours specified in defines
    return legendvalues 

def plotandsave(titlestring,ystring,yv,linearity):
    plt.title(titlestring)
    plt.axis(ymin=yv)
    plt.ylabel(ystring) 			#defines labels for your graph. "D flux (N m⁻²s⁻ˡ)"
    plt.rcParams.update({"savefig.facecolor":  ('white'),"figure.figsize": (14, 8)})  			#big nice pngs
    if linearity:
        plt.yscale("log") 				#If Log is set to true, it plots on a logarithmic axis.
    savestring = '/'.join([outputfolder, titlestring])
    plt.savefig(savestring, bbox_inches='tight') #this will throw a bunch of .png files into the folder specified in filepath, overwriting anything with the same name.
    plt.show()				#shows you the graph that was saved

#Script
legendvalues =[]
xlsx_filepath = ''.join([filepath, ".xlsx"])
xlsx_files = glob.glob(xlsx_filepath)
csv_filepath = ''.join([filepath, ".csv"])
csv_files = glob.glob(csv_filepath)
print (xlsx_filepath, csv_filepath)
print ('files found:', xlsx_files, csv_files)

for each in xlsx_files:
    i = pd.ExcelFile(each)
    histopoint = []
    alldata = pd.read_excel(i, sheet_name=None)
    listofsheetnames = list(alldata.keys())
    sheetcount = len(listofsheetnames)
    sheetdisplay = [listofsheetnames[each] for each in Ydatacolumns]
    print ('Began reading', i, 'and found these sheets in this document:', sheetdisplay)
    for sheetno in specific_sheets:
        print ('reading sheet', listofsheetnames[sheetno])
        x = getcontentx(i,sheetno,Xdatacolumn)
        legendvalues = plotYandreturnlegendvalues(i,sheetno,Ydatacolumns)
        leg = plt.legend(legendvalues, bbox_to_anchor=(1, 1)) 
        for line in leg.get_lines(): #Formats legend to use a wider linewidth. Thank you Adam
            line.set_linewidth(6.0)       
        titlestring = '.'.join([each[(len(filepath)-1):-5],listofsheetnames[sheetno],"png"]) # makes a string for the title of graphs and for saving the files as a svg. To make png instead, change svg to png.
        plotandsave(titlestring,"Count",5,True)
    for sheetno in specific_sheets:
        print ('reading sheet', listofsheetnames[sheetno])
        hst = pd.read_excel(i, sheet_name = sheetno, usecols = histcol, header = header_row)
        histopoint.append(hst.iat[histrow,0]) # hey look i can pull a single data point out from the entire graph that's useful we can append it and make it a histogram
        ydata = pd.read_excel(i, sheet_name = sheetno, usecols = Ymultiplotcolumn, header = header_row)    
        indexedydata = [list(x) for x in zip(*ydata.values)]
        y = pd.Series(indexedydata[0]).rolling(window=smoothfactor).mean()
        x = getcontentx(i,sheetno,Xdatacolumn)
        plt.plot(x, y, color = colours[sheetno], linewidth = 1.5, alpha = 0.7)
    legendvalues= (list(listofsheetnames[x] for x in specific_sheets))
    leg = plt.legend(legendvalues, bbox_to_anchor=(1, 1)) 
    for line in leg.get_lines(): #Formats legend to use a wider linewidth. Thank you Adam
        line.set_linewidth(6.0) 
    plotandsave("Log comparison of D release over time for each sample","total D atoms per m²s", xinterceptofmultiplot, True)
    plt.bar(legendvalues, histopoint,color = (list(colours[x] for x in specific_sheets)), alpha = 0.7) 
    plotandsave('Comparison of total D release for each sample',"total D atoms per cm² e17",0, False)
    
        
for i in csv_files:
    alldata = pd.read_csv(i, header= header_row_csv)
    print ('Began reading', i)
    datavalues = [list(x) for x in zip(*alldata.values)]
    datalabels = alldata.columns
    print(datalabels)
    x = pd.Series(datavalues[Xdatacolumn]).rolling(window=smoothfactor).mean()
    for each in Ydatacolumns:
        y = pd.Series(datavalues[each]).rolling(window=smoothfactor).mean()
        plt.plot(x, y, color =colours[each], linewidth = 1.5, alpha = 0.7)
    plt.xlabel(datalabels[Xdatacolumn])
    leg = plt.legend(legendvalues, bbox_to_anchor=(1, 1)) 
    for line in leg.get_lines(): #Forplt.legend(datalabels[Ydatacolumns], bbox_to_anchor=(1, 1))mats legend to use a wider linewidth. Thank you Adam
        line.set_linewidth(6.0) 
    titlestring = '.'.join([i[len(filepath):-4],"svg"])
    plotandsave(titlestring,"count",5, True)

print ('"My work here is done." The python executable revs a big motorcycle and drives away in a cloud of smoke. It lights a cigarette, and gazes wistfully back at you, tears forming in its eyes')

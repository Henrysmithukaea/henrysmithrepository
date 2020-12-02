# henry.smith@ukaea.uk


import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import glob
from pathlib import Path

#defines
filepath = 'C:/Users/hsmith/Anaconda/Anaconda script files\*' #write the filepath, and at the end, include '*' - can't end in a \
Xdatacolumn = 1 			#only column in each sheet of the doc that contains the x data
Ydatacolumns = [3,4,5,6,7,8,9,10] 	#all columns in each sheet of the doc that contains Y data
header_row = 2 				#row of the header (i.e the column titles)
colours = ("Yellow", "Green", "Blue", "Red", "Orange", "Purple", "Black", "Teal", "Yellow", "Green", "Blue", "Red", "Orange", "Purple", "Black") #will cycle through this index colouring each new graph in a new colour
ignored_sheets = 1 			#the number of sheets in the spreadsheet you don't want processed. All of these have to be reordered to appear at the end of the list of sheets. 

#Command defines

def getcontentx(i, sname, colno):
    data = pd.read_excel(i, sheet_name = sname, usecols = [colno], header = header_row)
    indexeddata = [list(x) for x in zip(*data.values)]
    x = pd.Series(indexeddata[0]).rolling(window=7).mean()
    plt.xlabel(data.columns[0])  	# column header becomes the x axis title. You can replace this with any string you like.
    return x

def plotYandreturnlegendvalues(i, sname, colnos):
    data = pd.read_excel(i, sheet_name = sname, usecols = colnos, header = header_row)
    indexeddata = [list(x) for x in zip(*data.values)] #pulls out the data
    legendvalues = (data.columns)
    for column in range(len(colnos)): 
        y = pd.Series(indexeddata[column]).rolling(window=7).mean() 		#pulls out a column in the data
        plt.plot(x, y, color =colours[column], linewidth = 1.5, alpha = 0.7) #  There's a lot of options here, e.g 'o' means it plots as dots. you may want to add 'color =colours[each], ' - this will then use the colours specified in defines
    return legendvalues 

def plotandsave(titlestring):
    plt.title(titlestring)
    plt.ylabel("Count")  			#defines labels for your graph.
    plt.yscale("log") 				#logarithmic axis
    plt.savefig(titlestring, bbox_inches='tight') #this will throw a bunch of .png files into the folder specified in filepath, overwriting anything with the same name.
    plt.show()				#shows you the graph that was saved

#Script
legendvalues =[]
xlsx_filepath = ''.join([filepath, ".xlsx"])
xlsx_files = glob.glob(xlsx_filepath)
csv_filepath = ''.join([filepath, ".csv"])
csv_files = glob.glob(csv_filepath)
print (xlsx_filepath, csv_filepath)
print ('files found:', xlsx_files, csv_files)

for i in xlsx_files:
    alldata = pd.read_excel(i, sheet_name=None)
    listofsheetnames = list(alldata.keys())
    sheetcount = len(listofsheetnames) - ignored_sheets
    print ('Began reading', i, 'and found', sheetcount, 'sheets in this document.', listofsheetnames)
    for sheetno in range (sheetcount):
        print ('reading sheet', listofsheetnames[sheetno])
        x = getcontentx(i,sheetno,Xdatacolumn)
        legendvalues = plotYandreturnlegendvalues(i,sheetno,Ydatacolumns)
        plt.legend(legendvalues, bbox_to_anchor=(1, 1)) #Formats legend. for some reason there's no setting to alter line width of legend outside of making it fully custom. is dumb.
        titlestring = '.'.join([listofsheetnames[sheetno],i[(len(filepath):-5],"png"]) # makes a string for the title of graphs and for saving the files as a svg. To make png instead, change svg to png.
        plotandsave(titlestring)

        
      
print ('"My work here is done." The python executable revs a big motorcycle and drives away in a cloud of smoke. It lights a cigarette, and gazes wistfully back at you, tears forming in its eyes')

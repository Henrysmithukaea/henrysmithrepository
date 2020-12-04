# henry.smith@ukaea.uk


import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.axes as axes
import glob
from pathlib import Path

#defines
filepath = 'C:/Users/hsmith/Anaconda/Anaconda script files\*' #write the filepath, and at the end, include '*' - can't end in a \
Xdatacolumn = 1 			#only column in each sheet of the doc that contains the x data
Ydatacolumns = [3,4,5,6,7,8,9,10] 	#all columns in each sheet of the doc that contains Y data
Ymultiplotcolumn = [3]
header_row = 2 				#row of the header (i.e the column titles)
colours = ("Yellow", "Green", "Blue", "Red", "Orange", "Purple", "Black", "Teal",
           "rosybrown", "salmon", "darkgoldenrod", "lightseagreen", "darkolivegreen", "saddlebrown", "cornflowerblue",
          "fuchsia", "grey", "darkslategray", "navy", "royalblue", "lightgreen", "mediumseagreen") #will cycle through this index colouring each new graph in a new colour
ignored_sheets = 1 			#the number of sheets in the spreadsheet you don't want processed. All of these have to be reordered to appear at the end of the list of sheets. 
specific_sheets = [2,3,4,5,6,8,12,13,14,16,18,20]

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
    print (legendvalues)
    for column in range(len(colnos)): 
        y = pd.Series(indexeddata[column]).rolling(window=7).mean() 		#pulls out a column in the data
        plt.plot(x, y, color =colours[column], linewidth = 1.5, alpha = 0.7) #  There's a lot of options here, e.g 'o' means it plots as dots. you may want to add 'color =colours[each], ' - this will then use the colours specified in defines
    return legendvalues 

def plotandsave(titlestring):
    plt.title(titlestring)
    plt.axis(ymin=5)
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

for each in xlsx_files:
    i = pd.ExcelFile(each)
    alldata = pd.read_excel(i, sheet_name=None)
    listofsheetnames = list(alldata.keys())
    sheetcount = len(listofsheetnames) - ignored_sheets
    print ('Began reading', i, 'and found', sheetcount, 'sheets in this document.', listofsheetnames)
    print (alldata.keys)
    print (listofsheetnames)
    for sheetno in range (sheetcount):
        print ('reading sheet', listofsheetnames[sheetno])
        x = getcontentx(i,sheetno,Xdatacolumn)
        legendvalues = plotYandreturnlegendvalues(i,sheetno,Ydatacolumns)
        plt.legend(legendvalues, bbox_to_anchor=(1, 1)) #Formats legend. for some reason there's no setting to alter line width of legend outside of making it fully custom. is dumb.
        titlestring = '.'.join([listofsheetnames[sheetno],each[len(filepath):-5],"png"]) # makes a string for the title of graphs and for saving the files as a svg. To make png instead, change svg to png.
        plotandsave(titlestring)
    for sheetno in specific_sheets:
        print ('reading sheet', listofsheetnames[sheetno])
        ydata = pd.read_excel(i, sheet_name = sheetno, usecols = Ymultiplotcolumn, header = header_row)    
        indexedydata = [list(x) for x in zip(*ydata.values)]
        y = pd.Series(indexedydata[0]).rolling(window=7).mean()
        x = getcontentx(i,sheetno,Xdatacolumn)
        print (colours[sheetno])
        plt.plot(x, y, color = colours[sheetno], linewidth = 1.5, alpha = 0.7)
    legendvalues= (list(listofsheetnames[x] for x in specific_sheets))
    plt.legend(legendvalues, bbox_to_anchor=(1, 1)) 
    titlestring = "comparison.svg"
    plotandsave(titlestring,500)               
             
                  
        
        
for i in csv_files:
    alldata = pd.read_csv(i, header= header_row_csv)
    print ('Began reading', i)
    datavalues = [list(x) for x in zip(*alldata.values)]
    datalabels = alldata.columns
    print(datalabels)
    x = pd.Series(datavalues[Xdatacolumn]).rolling(window=7).mean()
    for each in Ydatacolumns:
        y = pd.Series(datavalues[each]).rolling(window=7).mean()
        plt.plot(x, y, color =colours[each], linewidth = 1.5, alpha = 0.7)
    plt.xlabel(datalabels[Xdatacolumn])
    plt.legend(datalabels[Ydatacolumns], bbox_to_anchor=(1, 1))
    titlestring = '.'.join([i[len(filepath):-4],"svg"])
    plotandsave(titlestring)
         
print ('"My work here is done." The python executable revs a big motorcycle and drives away in a cloud of smoke. It lights a cigarette, and gazes wistfully back at you, tears forming in its eyes')

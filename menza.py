#region IMPORTS (ignore, nothing to see here)
 
import os
import enum
import sys

# Clears terminal for nice clean output
os.system('cls||clear')

class Mode():
    PDF = True
    Webpage = False
   
#endregion

#region INTIAL SETUP (your FILENAME and DATE of interest)

#https://issp.srce.hr/Account/OdaberiPrijavu?ReturnUrl=%2Fstudent%2Fstudentracuni


# data needs to be saved as .txt and moved to same the same folder as this python script
# insert the name of your file in line of code below like this:
# inputData = 'nameOfYourFile.txt'
# edit the line below
inputData = 'myData.txt'

# insert your date of interest and run the script
# date like "MM.YYYY", "dd.MM.YYYY" or "YYYY"
# dd - day, MM - month, YYYY - year
# ranges are not implemented
# if the script RUNS FINE but with EMPTY OUTPUT, it is very likely that this variable is incorrectly set
dateOfInterest = '10.2021'

#endregion

#region CODE (ignore, nothing to see here)
# no need to touch any of this

# helps program ignore rows with insufficient number of characters ("bad" rows)
# example of a good row for webpage and .pdf mode (everything else is considered bad):
# .pdfmode
# "Restoran Kampus, Kampus2 85317777355 19.01.2021 10:33 22.3000 13.7200 Skenirano"
# note: better leave it be, it should work fine
approximateNumberOfLettersPerRow = 40

try:
    inputFileHandle = open(inputData, "r", encoding="utf8")
    
    if "link" in inputFileHandle.read(): 
        modeOfOperation = Mode.Webpage
    else:
        modeOfOperation = Mode.PDF
    inputFileHandle.close

    inputFileHandle = open(inputData, "r", encoding="utf8")
except:
    print("""THIS ERROR CAN EASILY BE FIXED:
    Wrong filename, enter the name of your OWN .txt file (look for \"INTIAL SETUP\" region in the script) if you havent already.""")
    sys.exit()

if modeOfOperation:
    dateIndex = -5
    priceIndex = -3
    subventionIndex = -2
else:
    dateIndex = -6
    priceIndex = -4
    subventionIndex = -3

myList = []
bill = 0

for line in inputFileHandle:
    # only lines (rows) of interest are processed 
    #you can adjust 'averageNumberOfLettersPerRow' in ADJUSTABLE VALUES section
    if len(line) > approximateNumberOfLettersPerRow:       
        line = line.rstrip().lstrip()           
        myList.append(line)

inputFileHandle.close()

print()
print()
print()

# making a log file with given paramethers in it's name
temp = inputData.split(".")[0]
temp = temp.replace(" ", "")
print(temp)
logFilename = temp + "_calculation_for_" + dateOfInterest +".txt"
f = open(logFilename, "w")

text = """DATE: {}
BILL SUBVENTION PAID
--------------------\n""".format(dateOfInterest)
print(text)
f.write(text)

for line in myList: 
    if modeOfOperation:
        # in case of .pdf mode of operation
        x = line.split(" ")
    else:
        # in case of web mode of operation
        x = line.split("\t")

    try:
        if dateOfInterest in x[dateIndex]:
            
            price = float(x[priceIndex])        
            subvention = float(x[subventionIndex])
            paid = round( price - subvention, 2)
            bill += paid

            logText = "{} - {} = {}  SUBTOTAL: {}".format(price, subvention, paid, round(bill, 2))

            f.write(logText + "\n")
            print(logText)
    except:
        # if date is not positioned well, row is "bad" and can be skipped. WARNING: hides all index out of range errors!
        # IF YOU ARE CONSTANTLY GETTING "TOTAL: 0" WITHOUT CRASH AND TRYING TO FIX IT,  
        # REMOVE THIS "continue" or whole TRY/EXEPT BLOCK, IT CAN GIVE YOU A WALUABLE FEEDBACK 
        continue

text = """
TOTAL: {}
end of calculation""".format(round(bill, 2))
print(text)
f.write(text)  
f.close()

#endregion
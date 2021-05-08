#Script To to Remove Range of Sims From Sim Upload File
import pathlib
import re
import csv
import threading

## First open the file in Input Location of the File 
#outputFileName = input("Name of OutPut File ")
functionCounter = 0
storeOutputFilesLines = []
globalCsvFile = open('D:\\Jada Codwell\\T-Mobile\\Automation\\Sim Upload\\CSV\\VST61775.csv', encoding='utf-8-sig' )
globalListOfData = csv.reader(globalCsvFile)


def openBatchFile():
    csvFile = open('D:\\Jada Codwell\\T-Mobile\\Automation\\Sim Upload\\CSV\\VST61775.csv', encoding='utf-8-sig' )
    listOfData = csv.reader(csvFile)
    batchFileName = ''
    duplicateCounter = 0
    for filename in listOfData:
        if batchFileName != filename[3]:
            batchFileName = filename[3]
            print("The Batch File is " + batchFileName)
            inputFile = open('D:\\Jada Codwell\\T-Mobile\\Automation\\Sim Upload\\Input Files\\' + batchFileName +'.txt' )
            #inputFile = open('D:\\Jada Codwell\\T-Mobile\\Automation\\Sim Upload\\Input Files\\VST57052.txt' )
            inputFileLines = inputFile.readlines()
            loopThroughQuantitty(inputFileLines[32:], batchFileName )

        elif batchFileName == filename[3]:
            inputFile = open('D:\\Jada Codwell\\T-Mobile\\Automation\\Sim Upload\\Input Files\\' + batchFileName +'.txt' ) 
            inputFileLines = inputFile.readlines()
            loopThroughQuantitty(inputFileLines[32:], batchFileName)
                  
    #return batchFileName


def readCSV():
    csvFile = open('D:\\Jada Codwell\\T-Mobile\\Automation\\Sim Upload\\CSV\\VST61775.csv', encoding='utf-8-sig' )
    readCsvFile = csv.reader(csvFile)
    listOfData = list(readCsvFile)
    listOfDicts = []
    for i in listOfData:
        subtractOne = int(i[0]) - 1
        listOfDicts.append({'imsiRange2':i[1], 'imsiRange1': subtractOne, 'batchNumber': i[3]}) # Creates a list of dictionaries: I chose to use a dictionary to create as the key represent the columns from my csv file
  
    return listOfDicts 
    # The output of listofDicts looks like this ---> [{'imsiRange2': '311882002117605', 'imsiRange1': 311882002117602, 'batchNumber': 'VST61775'}, {'imsiRange2': '311882002117631', 'imsiRange1': 311882002117626, 'batchNumber': 'VST61776'}]
   
    

def i_oCloseFunctions(length):
    global functionCounter
    global storeOutputFilesLines
    functionCounter += 1
    outputFile = open("storedSims" + ".txt")
    outputFileFinal = open("CompletedSimList" + ".txt", "a")
    if functionCounter == length:
        content = outputFile.readlines()       
        outputFileFinal.writelines(list(dict.fromkeys(content)))
        storeOutputFilesLines = list(dict.fromkeys(content))    
    outputFile.close() 
    outputFileFinal.close()
    print("Completed")
    return storeOutputFilesLines
    


def findQuantity(imsiRange2, imsiRange1):
    return int(imsiRange2) - int(imsiRange1)


def loopThroughQuantitty(Input, batchname):
    print("reading...")            
    i = 0
    count = 0 
    csvResults = readCSV()
    list = []
    for index in range(len(csvResults)):
        startRange = int(csvResults[index]['imsiRange1']) + 1
        imsiRange1 = int(csvResults[index]['imsiRange1']) 
        quauntity = findQuantity(csvResults[index]['imsiRange2'], str(imsiRange1 + 1))
        
         
        while i <= quauntity:
            i += 1
            for item in Input:
                if item.find(str(startRange)) == 0 and count <= quauntity  :
                    itemIndexNum = Input.index(item) 
                    list.append([Input.pop(itemIndexNum)])
                    itemIndexNum += 1
                    startRange += 1
                    count += 1
                   
        i = 0            
        count = 0
        itemIndexNum = 0
        
         
    i_oWriteFunctions(list)
    i_oCloseFunctions(len(csvResults))


def i_oWriteFunctions(list):
    print("Writing the list...")

    count = 0 
    listCopy = list.copy()
    csvDataList = readCSV()
    for line in list:
        if len(list) != []:
            outputFile = open("storedSims" + ".txt", "a" )
            outputFile.writelines(line)

def checkRanges(ranges):
    global globalListOfData
    listOfSimsPrinted = []
    for items in globalListOfData:
        try:
            for iteminRange in ranges:   
                listOfSimsPrinted.append(iteminRange[0:15])

            listOfSimsPrinted.index(items[0])        
        except :

            print("Missing start range: " + items[0] +" in " + items[3])
            

def checkLines(ranges):  
    for iteminRange in ranges:
         if len(iteminRange) > 156:
           print("****************************************************************************")
           print("There is an Issue with line :" )
           print(iteminRange) 

   
      

#Executed Functions ----
openBatchFile()

#Testing the output files for any issues
checkRanges(i_oCloseFunctions(len(readCSV())))
checkLines(i_oCloseFunctions(len(readCSV())))

#Script To to split Files

import pathlib
import re

## First open the file in Input Location of the File 
outputFileName = input("Name of OutPut File ")
inputFile = open('D:\\Jada Codwell\\T-Mobile\\Automation\\Subscriber Update\\File Split Scripts\\Input Files\\test.txt')


## this method then takes every line and puts it in a array 
inputFileLines = inputFile.readlines()
inputFilesCopy = inputFileLines.copy()
## Input the Ranges in which you want to search and print for
##changeTypeId = input("Enter ChangeTypeID: ")

def i_oCloseFunctions():
    outputFile = open(outputFileName + ".txt")
    content = outputFile.readlines()
    outputFile.close()

def processFileGen(input):
    processFile = open("Processed.txt", "a" )
    processFile.writelines(input)
    processFile = open("Processed.txt")
    processFileContent = processFile.readlines()
    processFile.close()

def removeLine(Input):
    i = 0
    count = 0;
    itemsCount =0;
    outputFile = open(outputFileName + ".txt", "a" )  
    changeTypeID = ["|30|"]

    for item in Input:
        for changeTypeIDs in changeTypeID:
            #A Script to split by changeType Id 
            if item.find(changeTypeIDs) >= 0 and count != 40000:
                count += 1
                print(count)
                outputFile.writelines(item)
                inputFilesCopy.remove(item)
                continue    
               
                
            
                
           
removeLine(inputFileLines)
i_oCloseFunctions()
processFileGen(inputFilesCopy)

                            
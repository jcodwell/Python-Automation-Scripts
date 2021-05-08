#Script To to Remove Range of Sims From Sim Upload File

import pathlib
import re

## First open the file in Input Location of the File 
#outputFileName = input("Name of OutPut File ")
inputFile = open('D:\\Jada Codwell\\T-Mobile\\Automation\\Sim Upload\\Input Files\\VST57101.txt')

## this method then takes every line and puts it in a array 
inputFileLines = inputFile.readlines()

## Input the Ranges in which you want to search and print for
imsiRange1 = input("Enter Start Imsi: ")
imsiRange2 = input("Enter End Imsi ")

def i_oCloseFunctions():
    outputFile = open("57101" + ".txt")
    content = outputFile.readlines()
    outputFile.close()
 

def findQuantity():
    return int(imsiRange2) - int(imsiRange1)

def loopThroughQuantitty(Input):
    i = 0
    count = 0 
    while i <= findQuantity():
        i += 1
        for item in Input:
            if item.find(imsiRange1) == 0 and count != findQuantity():
                count += 1
                outputFile = open("57101" + ".txt", "a" )
                outputFile.writelines(Input.pop(Input.index(item) + 1))
                i_oCloseFunctions()
                
findQuantity()
loopThroughQuantitty(inputFileLines)
                            
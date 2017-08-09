#!/usr/bin/env python
#USAGE ./run.py -trace[optinal] [experimentos.csv] [parser.txt] [plat.xml] [d-plat.xml]
import os
import multiprocessing
import argparse
import csv
import sys
import ctypes

"""
    read the content of a csv and return the
    
"""
def csvToList(csvFile):
    csvContent = csv.reader(csvFile,delimiter=',')
    csvList=[]
    while True:
        try:
            csvList.append(csvContent.next())
	except Exception :
	    return csvList
            break


def main():
    args = readArgs()
    trace = args.trace

    if trace==False:
        numCores = multiprocessing.cpu_count() -1 
        mraCsv  = csvToList(args.mra)
         
        mrsgCsv = csvToList(args.mrsg)
        if len(mraCsv)!=len(mrsgCsv):
            print "ERROR: input files doesn't have same rows size!"
            sys.exit()
        # Skip the labels row (i.e., the first row )
        row = multiprocessing.Value('i',0)
       
	for core in range(numCores):
           
            newProcess = multiprocessing.Process(target=runParallelTest,args=(mraCsv,mrsgCsv,args.parser,row))
 	    newProcess.start()
    else:
        runTests(args.mra,args.mrsg,args.parser)

def runParallelTest(mraCsv,mrsgCsv,parser,row):
    confFields= mrsgCsv[0][5:]
    confFields= confFields + mraCsv[0][5:]
     
    while True:
	with row.get_lock():
            row.value+=1
            if len(mrsgCsv) <= row.value:
                sys.exit()
        
        platFile = "Exp_" + str(row.value) 
        mraPlat = " ".join(mraCsv[row.value][:5])
        mrsgPlat = " ".join(mrsgCsv[row.value][:5])
        platFile = "Exp_" + str(row.value) 
        print "Plat: "+ platFile +" MRA:" +mraPlat+" MRSG:" + mrsgPlat
        os.system("python create-bighybrid-plat.py "+platFile + ".xml " + mraPlat +" "+ mrsgPlat)
        os.system("python create-bighybrid-depoly.py "+ platFile+ ".xml ")
       
        createConfFile(platFile,confFields,mrsgCsv[row.value][5:]+mraCsv[row.value][5:])
        params= platFile+ ".xml d-"+ platFile +".xml " + platFile + ".conf "+ parser 
        print "Running main ..."
        os.system("./hello_bighybrid.bin "+ params)
        print "run ok"
	
"""
        Main script function.
        Creates all input files for bighybrid and run tests
"""
def runTests(mraFile,mrsgFile,parser):
    mraCsv  = csv.reader(mraFile,delimiter=',')
    mrsgCsv = csv.reader(mrsgFile,delimiter=',')
    # Skip the labels row (i.e., the first row )
    confFields= mrsgCsv.next()[5:]
    confFields= confFields + mraCsv.next()[5:]
    row = 0
    while True:
	try:
                mra  = mraCsv.value.next()
                mrsg = mrsgCsv.value.next()
            # Take the first five fields of both csv to generate the bighybrid plat file
	        mraPlat = " ".join(mra[:5])
	        mrsgPlat = " ".join(mrsg[:5])
                platFile = "Exp_" + str(row) 
                os.system("python create-bighybrid-plat.py "+platFile + ".xml " + mraPlat +" "+ mrsgPlat)
	        os.system("python create-bighybrid-depoly.py "+ platFile+ ".xml ")
                createConfFile(platFile,confFields,mrsg[5:]+mra[5:])
                params= platFile+ ".xml d-"+ platFile +".xml " + platFile + ".conf "+ parser 
                os.system("./hello_bighybrid.bin "+ params)
                row = row +1        
	except Exception :
	    print "gotcha"
            break

#Define and return the Args
def readArgs():
    parser = argparse.ArgumentParser(description='Execute BigHybrid experiments')
    parser.add_argument('-trace',action='store_true',help='set SimGrid tracefile to be generated')
    parser.add_argument('-mra',type=file, help='input csv file with mra config fields')
    parser.add_argument('-mrsg',type=file, help='input csv file with mrsg config fields')
    parser.add_argument('-parser',help='volatile parser for MRA')

    return parser.parse_args()


#Creates the .conf file (i.e., the workload file) for the given experiment
def createConfFile(fileName,fields,data):
    with open(fileName+".conf",'w') as confFile:
        for i in range(len(fields)):
            print fields[i] + ": "+ data[i]
            confFile.write(fields[i] + " " + data[i] +"\n")

if __name__=="__main__":
    main()

#!/usr/bin/env python
#USAGE ./run.py -trace[optinal] [experimentos.csv] [parser.txt] [plat.xml] [d-plat.xml]
import os
import multiprocessing
import argparse
import csv
import sys
import ctypes
import subprocess

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
    os.system("export LD_LIBRARY_PATH=$HOME/simgrid-3.14.159/lib")
    os.system("make clean all")
    if trace==False:
        numCores = multiprocessing.cpu_count() -1
        mraCsv  = csvToList(args.mra)

        mrsgCsv = csvToList(args.mrsg)
        if len(mraCsv)!=len(mrsgCsv):
            print "ERROR: input files doesn't have same rows size!"
            sys.exit()
        # Skip the labels row (i.e., the first row )
        row = multiprocessing.Value('i',1)
       
        #if the number of cores is bigger then number of tests, switch cores value (value of processes spwaned)
        if len(mrsgCsv)<numCores:
            numCores = len(mrsgCsv) -1
        #    print "cores = " + str(numCores)
	for core in range(numCores):

            newProcess = multiprocessing.Process(target=runParallelTest,args=(mraCsv,mrsgCsv,args.parser,row))
 	    newProcess.start()
    else:
        runTests(args.mra,args.mrsg,args.parser)

def runParallelTest(mraCsv,mrsgCsv,parser,row):
    confFields= mrsgCsv[0][5:]
    confFields= confFields + mraCsv[0][5:]

    while True:
        currentValue = 0
	with row.get_lock():
            currentValue = row.value
            row.value+=1
            if len(mrsgCsv) < row.value:
                return None

        platFile = "Exp_" + str(currentValue)
       # print "len ="+str(len(mrsgCsv))+"current = "+ str(currentValue)
        mraPlat = " ".join(mraCsv[currentValue][:5])
        mrsgPlat = " ".join(mrsgCsv[currentValue][:5])
        platFile = "Exp_" + str(currentValue)
       # print "value = "+str(currentValue)+"\nPlats:"
       # print mraPlat
       # print mrsgPlat
        os.system("python create-bighybrid-plat.py "+platFile + ".xml " + mraPlat +" "+ mrsgPlat)
        os.system("python create-bighybrid-depoly.py "+ platFile+ ".xml ")

        createConfFile(platFile,confFields,mrsgCsv[currentValue][5:]+mraCsv[currentValue][5:])
        params = []
	params.append("./hello_bighybrid.bin")
	params.append(platFile+ ".xml")
	params.append("d-"+platFile +".xml" ) 
	params.append(platFile + ".conf")
	params.append(parser)
	
        print "running...."
	saida = open(platFile,'w')
        output = subprocess.Popen(params, stdout=saida,stdin=saida,stderr=saida)#subprocess.PIPE)
	saida.close()
	#tmp = output.stdout.read()
	#'./hello_bighybrid.bin '#print tmp[11]
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
                output = os.popen("./hello_bighybrid.bin "+ params).read()
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
            confFile.write(fields[i] + " " + data[i] +"\n")

if __name__=="__main__":
    main()

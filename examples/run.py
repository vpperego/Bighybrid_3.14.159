#!/usr/bin/env python

#USAGE ./run.py -trace[optinal] [experimentos.csv] [parser.txt] [plat.xml] [d-plat.xml]
import os
import multiprocessing
import argparse
import csv
import sys
import thread
import threading


def main():
    args = readArgs()
    trace = args.trace

    if trace==False:
        numCores = multiprocessing.cpu_count() -1 
        print "paral " + str(numCores) 
        mraCsv  = csv.reader(args.mra,delimiter=',')
        mrsgCsv = csv.reader(args.mrsg,delimiter=',')
        threadLock = threading.Lock()
        print "lock?"
        # Skip the labels row (i.e., the first row )
        confFields= mrsgCsv.next()[5:]
        confFields= confFields + mraCsv.next()[5:]
        row =0
        print "witf"
        for core in range(numCores):
            print "inew thread..."
            thread.start_new_thread(runParallelTest,(args.mra,args.mrsg,args.parser,threadLock,row))
    else:
        print "normal"
        runTests(args.mra,args.mrsg,args.parser)

def runParallelTest(mraCsv,mrsgCsv,parser,threadLock,row):
    print "paralel"

    while True:
	try:
                threadLock.acquire()
                mra  = mraCsv.next()
                mrsg = mrsgCsv.next()
            # Take the first five fields of both csv to generate the bighybrid plat file
	        mraPlat = " ".join(mra[:5])
	        mrsgPlat = " ".join(mrsg[:5])
                platFile = "Exp_" + str(row) 
                
                row = row +1
                threadLock.release()
                os.system("python create-bighybrid-plat.py "+platFile + ".xml " + mraPlat +" "+ mrsgPlat)
	        os.system("python create-bighybrid-depoly.py "+ platFile+ ".xml ")
                createConfFile(platFile,confFields,mrsg[5:]+mra[5:])
                params= platFile+ ".xml d-"+ platFile +".xml " + platFile + ".conf "+ parser 
                os.system("./hello_bighybrid.bin "+ params)
	except Exception :
	    print "gotcha"
            break


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
                mra  = mraCsv.next()
                mrsg = mrsgCsv.next()
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
    print "will open file"
    with open(fileName+".conf",'w') as confFile:
        print "Working?"
        for i in range(len(fields)):
            confFile.write(fields[i] + " " + data[i] +"\n")

if __name__=="__main__":
    main()

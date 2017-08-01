#!/usr/bin/env python

#USAGE ./run.py -trace[optinal] [experimentos.csv] [parser.txt] [plat.xml] [d-plat.xml]
import os
import multiprocessing
import argparse
import csv

def main():
	args = readArgs() 
	trace = args.trace
	if trace==False:
		numCores = multiprocessing.cpu_count()
	else:
		numCores = 1
	mraFile = args.mra
	mrsgFile = args.mrsg
	
"""
	Main script function.
	Creates all input files for bighybrid and run tests
"""
def runTests(mraFile,mrsgFile):
	mraPlat = ""
	mrsgPlat = ""
	mra = open(mraFile,'r')
	mrsg = open(mrsgFile,'r')
	mraCsv = csv.reader(mra,delimiter=',')
	mrsgCsv = csv.reader(mrsg,delimiter=',')
		
	os.system("python create-bighybrid-plat.py "+ str(n) +" " + mraPlat +" " mrsgPlat)
	os.system("python create-bighybrid-depoly.py" + str(n))
	
#Define and return the Args
def readArgs():
	parser = argparse.ArgumentParser(description='Execute BigHybrid experiments')
	parser.add_argument('-trace',action='store_true',help='set SimGrid tracefile to be generated')  
	parser.add_argument('-mra',type=file, help='input csv file with mra config fields')
	parser.add_argument('-mrsg',type=file, help='input csv file with mrsg config fields')
	return parser.parse_args()


#Creates the .conf file (i.e., the workload file) for the given experiment
def createConfFile(xpNumber,fields,data)
	with open("workload_"+str(xpNumber)+".conf",'w') as confFile:
		for i in range(len(fields)):
			confFile.write(fields[i] + " " + data[i] +"\n")
	
if __name__=="__main__":
   main()

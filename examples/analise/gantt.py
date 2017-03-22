#!/usr/bin/python

import sys
import re

TASK, TTYPE, TRACKER, START, END = range(5)

# [ (TASK, TTYPE, TRACKER, START, END) ]
tasks = []

def getTimeStamp(line):
	return line[0:23]

def getTracker(line):
	match = re.search(r'for tracker \'tracker_([^:]*):.*\'', line)
	return match.groups()[0]

def getTask(line):
	match = re.search(r'(attempt_[_0-9mr]*)', line)
	return match.groups()[0]

def getTType(task):
	if re.search(r'_m_', task):
		return '1'
	return '2'

def setTaskEnd(task, end):
	for i in range(len(tasks)):
		if tasks[i][TASK] == task:
			if len(tasks[i]) == 4:
				tasks[i] += end,
			return
	print 'ERRO'
	sys.exit(1)

if len(sys.argv) < 3:
	print 'Usage:', sys.argv[0], 'log_file job'
	sys.exit(1)

logFile = open(sys.argv[1], 'r')
job = sys.argv[2]

match = None
while not match:
	line = logFile.readline()
	match = re.search(r'JobInProgress: Initializing ' + job, line)

while True:

	line = logFile.readline()
	if not line:
		sys.exit(0)

	if re.search(r'JobTracker: Adding task \'attempt', line):
		task = getTask(line)
		ttype = getTType(task)
		tracker = getTracker(line)
		start = getTimeStamp(line)
		tasks.append( (task, ttype, tracker, start) )
		continue

	if re.search(r'has completed task_', line) or re.search(r'JobTracker: Adding task \(cleanup\)', line) or re.search(r'JobTracker: Removed completed task', line):
		setTaskEnd(getTask(line), getTimeStamp(line))
		continue

	if re.search(r'JobInProgress: Job ' + job + r' has completed successfully', line):
		break

logFile.close()

outFile = open('tasks.dat', 'w')

for task in tasks:
	if len(task) == 5:
		print task
		outFile.write(task[TASK] + '\t' + task[TTYPE] + '\t' + task[START] + '\t' + task[END] + '\n')
	else:
		print 'ERRO:', task

outFile.close()

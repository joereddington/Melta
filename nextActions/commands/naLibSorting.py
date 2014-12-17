#!/usr/bin/python
import csv
import time
import datetime
import operator
import io
import os


def sortTasksCSV():
   with open(os.environ['JURGEN']+'/joereddington.com/Jurgen/nextActions/nextActions.csv', 'rb') as f:
	reader = csv.reader(f, skipinitialspace=True)
	tasklist=sorted(reader,key=operator.itemgetter(3), reverse=True)
	tasklist.sort(key=lambda item: datetime.datetime.strptime(item[3], '%Y-%m-%d (%a) -  %H:%M:%S'))
	output=io.BytesIO()
	writer=csv.writer(output)
	return tasklist




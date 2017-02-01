#!/usr/bin/python
from na_lib_sorting import get_sorted_actions
import argparse
import time
import sys
import csv
import datetime
import operator
import io
import os
from na_lib_sorting import  get_sorted_actions
from filelock import FileLock

def setup_argument_list():
     "creates and parses the argument list for naCount"
     parser = argparse.ArgumentParser( description=__doc__)
     parser.add_argument('-echo', dest='echo', action='store_true', help='just print to screen; NO write to file')
     parser.add_argument('-sort', dest='sort', action='store_true', help='Ignore other input, print sorted list')
     parser.set_defaults(echo=False)
     parser.set_defaults(sort=False)
     parser.add_argument("action",nargs='?', help='The action to do')
     parser.add_argument("delay", nargs='?', default=0, help='A delay to add in days')
     parser.add_argument("context", nargs='?', default="0", help='The context for the action')
     parser.add_argument("priority", nargs='?', default="0", help='From 0 to 7 how important is this action')
     parser.add_argument("time", nargs='?', default="0", help='How long in minutes is this likely to take')
     return parser.parse_args()

def increatmentAndGetValue():

     with FileLock("myfile.txt"):
        with open(os.environ['JURGEN'] + 'Jurgen/nextActions/count.config', 'r+') as f:
                value = int(f.read())
                f.seek(0)
                f.write(str(value + 2))
                return value

def write_to_file(toprint):
    with open(os.environ['JURGEN'] + 'Jurgen/nextActions/nextActions.csv', 'a') as actions_file:
        actions_file.write(toprint)

def write_to_archive(toprint):
    with open(os.environ['JURGEN'] + 'Jurgen/nextActions/all_tasks.csv', 'a') as actions_file:
        actions_file.write(toprint )

def print_sorted_tasks():
	tasklist=get_sorted_actions()
	for row in tasklist:
	   toprint=  "%s, %s, %2s, \"%s\", %s, %s" % (row[0].strip(),  row[1].strip(), row[2], row[3] , row[4], row[5])
	   if len(row)==7:
		toprint=toprint+", "+row[6]
	   print toprint







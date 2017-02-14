#!/usr/bin/python
"A set of functions designed to make it easier to process a next actions list"
from __future__ import division
import argparse
import csv
import random
import datetime
import io
import operator
import os
import time
import sys
import csv


TIMESTAMP_FORMAT = '%y-%m-%d %H:%M'

NEXTACTIONS_LOC=os.environ['JURGEN'] + 'Jurgen/nextactions.md'
ALLACTIONS_LOC=os.environ['JURGEN'] + 'Jurgen/data/all_tasks.csv'
WAITACTIONS_LOC=os.environ['JURGEN'] + 'Jurgen/data/waitactions.md'

def get_sorted_actions():
    "returns a sorted list of nextActions"
    with open(NEXTACTIONS_LOC, 'rU') as actions_file:
        reader = csv.reader(actions_file, skipinitialspace=True)
        lines = filter(None, reader)
        tasklist = sorted(lines, key=operator.itemgetter(4), reverse=True)
        tasklist.sort(key=lambda item: datetime.datetime.strptime(
            item[4], TIMESTAMP_FORMAT))
        return tasklist


def write_to_file(toprint):
    with open(NEXTACTIONS_LOC, 'a') as actions_file:
        actions_file.write(toprint)

def write_to_archive(toprint):
    with open(ALLACTIONS_LOC, 'a') as actions_file:
        actions_file.write(toprint )








def setup_argument_list():
    "creates and parses the argument list for naCount"
    parser = argparse.ArgumentParser(
        description="manages a todo list")
    parser.add_argument("action", help="What to do/display: options are 'add', 'print', 'count', and 'info'  ")
    parser.add_argument("content",nargs='?', help='The action to do')
    parser.add_argument("delay", nargs='?', default=0, help='A delay to add in days')
    parser.add_argument("context", nargs='?', default="0", help='The context for the action')
    parser.add_argument("priority", nargs='?', default="0", help='From 0 to 7 how important is this action')
    parser.add_argument("time", nargs='?', default="0", help='How long in minutes is this likely to take')
    parser.add_argument('-c', nargs="?", help="if context_filter is activated then only actions in the relevant contexts (contexts are generally in 'bgthop0ry') are counted")
    parser.add_argument('-d', nargs="?" , help="Show only tasks that are at least this many days old")
    parser.add_argument( '-n', nargs="?", help="reverse context filter, eliminates certain contexts from the count")
    parser.add_argument( '-s', action='store_true', help="use if called by a script or cron")
    return parser.parse_args()



def filter_actions(args):
    "fetches the actions and runs a filter on them depending on the arguments"
    tasks = get_sorted_actions()
    if args.c:
        tasks = [i for i in tasks if i[1] in args.c]
    if args.n:
        tasks = [i for i in tasks if i[1] not in args.n]
    if args.d:
        tasks = [i for i in tasks if days_old(i)>=int(args.d)]
    return tasks

def print_actions(tasks):
    count_items= get_action_age_info_with_priority(tasks, lambda x:1, False)
    pri_items= get_action_age_info_with_priority(tasks)
    print " %d, %s,  %d, %d, %d, %d" % pri_items, ", %d, %d, %d, %d" % count_items

def print_time(tasks):
    running_total=0
    for row in tasks:
	running_total+=int(row[2])
    hours=running_total //60
    minutes=running_total -hours*60
    print "The total time for the set is {} minutes ({}:{})".format(running_total,hours,minutes)



def days_old(row):
	seconds_in_day=60*60*24
        datestring = row[4]
        timestamp_on_action = time.strptime( datestring.strip(), TIMESTAMP_FORMAT)
        age = time.time() - time.mktime(timestamp_on_action) 
	age = age+seconds_in_day*7#when we switched from origin to deadline
	days=int(age/(seconds_in_day))
	return days

def get_action_age_info_with_priority(tasklist, scorer=lambda x:7-int(x[0][-1]), time_print=True):
    "prints out the number of nextactions of each age in a current nextactions"
    now, dayold, threedayold, weekold = (0, 0, 0, 0)
    for row in tasklist:
	now+=scorer(row)
	days=days_old(row)
        if days>=1:
            dayold += scorer(row)
            if days>=3:
                threedayold += scorer(row)
                if days>=7:
                    weekold += scorer(row)
    if time_print==True:
	return (now, datetime.date.today(), time.time(), weekold, dayold, threedayold)

    return (now, weekold, dayold, threedayold)

def print_random(tasklist):
	row=random.choice(tasklist)
	print  "%s, %s, %2s, \"%s\", %s" % (row[0].strip(),  row[1].strip(), row[2], row[3] , row[4])
	
def print_next(tasklist):
	row= sorted(tasklist)[0]
	print  "%s, %s, %2s, \"%s\", %s" % (row[0].strip(),  row[1].strip(), row[2], row[3] , row[4])


def print_sorted_tasks(tasklist):
	for row in tasklist:
	   toprint=  "%s, %s, %2s, \"%s\", %s" % (row[0].strip(),  row[1].strip(), row[2], row[3] , row[4])
	   if len(row)==7:  
		toprint=toprint+", "+row[6]
	   print toprint
	

            

def write_to_waiting_list(toprint):
       with open(WAITACTIONS_LOC, 'a') as actions_file:
           actions_file.write(toprint)

def add(args):
	today = datetime.date.today()
	deadline=today+datetime.timedelta(days=7)
	date= deadline.strftime(TIMESTAMP_FORMAT)
        if args.content:
            toprint = "- [ ] %s, %s, %s, \"%s\", %s\n" % (args.priority, args.context, args.time, args.content, date)
            write_to_archive(str(date)+", "+toprint)
	    if args.s:
		    write_to_waiting_list(toprint)
            else:	
		    write_to_file(toprint)



if __name__ == '__main__':
    args = setup_argument_list()
    if args.action == "count":
        print_actions(filter_actions(args))
    elif args.action == "sort":
	print_sorted_tasks(filter_actions(args))
    elif args.action == "add":
	add(args)
    elif args.action == "random":
        print_random(filter_actions(args))
    elif args.action == "next":
        print_next(filter_actions(args))
    elif args.action == "time":
        print_time(filter_actions(args))
    else:
	print "Error, missing action" 


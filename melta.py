#!/usr/bin/python
"A set of functions designed to make it easier to process a next actions list"
from __future__ import division
import argparse
import csv
import random
import datetime
import operator
import os
import time
import csv
import json

TIMESTAMP_FORMAT = '%y-%m-%d %H:%M'
config = json.loads(open('config.json').read())
NEXTACTIONS_LOC=config["jurgen_location"] + '/nextactions.md'
ALLACTIONS_LOC=config["jurgen_location"] + '/data/all_tasks.csv'
WAITACTIONS_LOC=config["jurgen_location"] + '/data/waitactions.md'

def get_sorted_actions():
    "returns a sorted list of nextActions"
    with open(NEXTACTIONS_LOC, 'rU') as actions_file:
        reader = csv.reader(actions_file, skipinitialspace=True)
        lines = filter(None, reader)
        tasklist=[]
        for line in lines:
            task={}
            task['timestamp']=line[4]
            task['action']=line[3]
            task['time']=int(line[2])
            task['context']=line[1]
            task['priority']=line[0][6:]
            task['extra']=line[5:]
            tasklist.append(task)
        tasklist =sorted(tasklist,key=lambda item: item['timestamp'])
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
    for task in tasks:
	running_total+=task['time']
    hours=running_total //60
    minutes=running_total -hours*60
    print "The total time for the set is {} minutes ({}:{})".format(running_total,hours,minutes)



def days_old(task):
	seconds_in_day=60*60*24
        datestring = task['timestamp']
        timestamp_on_action = time.strptime( datestring.strip(), TIMESTAMP_FORMAT)
        age = time.time() - time.mktime(timestamp_on_action)
	age = age+seconds_in_day*7#when we switched from origin to deadline
	days=int(age/(seconds_in_day))
	return days


def tasks_this_old(tasklist, scorer, days):
    count=0
    for row in tasklist:
        if days_old(row)>=days:
            count += scorer(row)
    return count


def get_action_age_info_with_priority(tasklist, scorer=lambda x:7-int(x['priority'][-1]), time_print=True):
    "prints out the number of nextactions of each age in a current nextactions"
    now=tasks_this_old(tasklist,scorer,0)
    dayold=tasks_this_old(tasklist,scorer,1)
    threedayold=tasks_this_old(tasklist,scorer,3)
    weekold=tasks_this_old(tasklist,scorer,7)
    if time_print==True:
	return (now, datetime.date.today(), time.time(), weekold, dayold, threedayold)
    return (now, weekold, dayold, threedayold)

def print_random(tasklist):
	task=random.choice(tasklist)
	print_task(task)

def print_next(tasklist):
	task= sorted(tasklist)[0]
	print_task(task)


def print_sorted_tasks(tasklist):
	for task in tasklist:
	   print_task(task)


def print_task(task):
    print "- [ ] %s, %s, %2s, \"%s\", %s" % (task['priority'].strip(),  task['context'].strip(), task['time'], task['action'] , task['timestamp'])+ ''.join(task['extra'])

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



def run_melta():
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

if __name__ == '__main__':
    run_melta()


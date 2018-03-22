#!/usr/bin/python
"A set of functions designed to make it easier to process a next actions list"
from __future__ import division
from __future__ import print_function
import argparse
import sys
import csv
import random
import datetime
import operator
import os
import time
import csv
import json

TIMESTAMP_FORMAT = '%y-%m-%d %H:%M'
config = json.loads(open(os.path.dirname(os.path.abspath(__file__))+'/config.json').read())
NEXTACTIONS_LOC=config["jurgen_location"] + '/nextactions.md'
ALLACTIONS_LOC=config["jurgen_location"] + '/data/all_tasks.csv'
PRI_LOC=config["jurgen_location"] + '/data/priority.txt'
WAITACTIONS_LOC=config["jurgen_location"] + '/data/waitactions.md'

def eprint(*args, **kwargs):
	pass
#    print(*args, file=sys.stderr, **kwargs)#from https://stackoverflow.com/a/14981125/170243

def last_line_pri():
	return open(PRI_LOC).readlines()[-1]

def update_pri_if_different():
   try:
     parser = setup_argument_list()
     args=parser.parse_args(['sort','-o', '-s'])
     now=print_actions(filter_actions(args),args).strip()
     before=last_line_pri().strip()
     now_a=now[30:]
     before_a=before[30:]
     if now_a == before_a:
	pass
#	print "idenical, NO updated needed"
     else:
	    with open(PRI_LOC, 'a') as pri_file:
		pri_file.write(now+"\n")
   except IOError:
        eprint("Could NOT update priority log file")
#	print "There has been a change. Writing. "
#     print "N"+now_a+"X"
#     print "T"+before_a+"X"

def get_sorted_actions():
    "returns a sorted list of nextActions, strips out any line without four fields"
    with open(NEXTACTIONS_LOC, 'rU') as actions_file:
        reader = csv.reader(actions_file, skipinitialspace=True)
        lines = filter(None, reader)
        tasklist=[]
        for line in lines:
          if len(line)>=4:
	   if "- [" in line[0]:
		    task={}
		    task['timestamp']=line[3]
		    task['action']=line[2]
		    task['time']=int(line[1])
	#            task['context']=line[1]
		    task['priority']=line[0][6:]
		    task['extra']=line[4:]
		    task['completed']=line[0][3:4]
		    tasklist.append(task)
          else:
            eprint( "The following line did NOT parse and was removed")
            eprint(line)
        tasklist =sorted(tasklist,key=lambda item: item['priority']+item['timestamp'])
        return tasklist

def write_to_file(toprint):
    with open(NEXTACTIONS_LOC, 'a') as actions_file:
        actions_file.write(toprint)

def write_to_archive(toprint):
    with open(ALLACTIONS_LOC, 'a') as actions_file:
        actions_file.write(toprint )

def setup_argument_list():
    parser = argparse.ArgumentParser(
        description="manages a todo list")
    parser.add_argument("action", help="What to do/display: options are 'add', 'print', 'count', and 'info'  ")
    parser.add_argument("content",nargs='?', help='The action to do')
    parser.add_argument("delay", nargs='?', default=0, help='A delay to add in days')
    parser.add_argument("context", nargs='?', default="0", help='The context for the action')
    parser.add_argument("priority", nargs='?', default="0", help='From 0 to 7 how important is this action')
    parser.add_argument("time", nargs='?', default="0", help='How long in minutes is this likely to take')
#    parser.add_argument('-c', nargs="?", help="if context_filter is activated then only actions in the relevant contexts (contexts are generally in 'bgthop0ry') are counted")
    parser.add_argument('-m', action='store_true', help="show only marked tasks")
    parser.add_argument('-d', nargs="?" , help="Show only tasks that are at least this many days old")
#    parser.add_argument( '-n', nargs="?", help="reverse context filter, eliminates certain contexts from the count")
    parser.add_argument( '-o', action='store_true', help="Open tasks")
    parser.add_argument( '-s', action='store_true', help="use if called by a script or cron")
    return parser



def filter_actions(args):
    "fetches the actions and runs a filter on them depending on the arguments"
    tasks = get_sorted_actions()
#    if args.c:
#        tasks = [i for i in tasks if i['context'] in args.c]
    if args.m:
        tasks = [i for i in tasks if i['completed'] in ["x","e"]]
    if args.o:
        tasks = [i for i in tasks if i['completed'] ==" "]
#    if args.n:
#        tasks = [i for i in tasks if i['context'] not in args.n]
    if args.d:
        tasks = [i for i in tasks if days_old(i)>=int(args.d)]
    return tasks

def powerhour(tasks):
    tasks = [i for i in tasks if i['time'] != 0 ]
    tasks =sorted(tasks,key=lambda item: item['time'])
    total_time_remaining=60
    powertasks=[]
    for a in tasks:
        if a['time']<total_time_remaining:
            powertasks.append(a)
            total_time_remaining-=a['time']



    return powertasks

def print_actions(tasks,args):
    count_items= get_action_age_info_with_priority(tasks, lambda x:1, False)
    pri_items= get_action_age_info_with_priority(tasks)
    if args.s:
       result= str(" %d, %s,  %d, %d, %d, %d" % pri_items + ", %d, %d, %d, %d" % count_items)
       return result
    return """State of Next Actions as of {}
Now:   {}({})
1 day  {}({})
3 day  {}({})
7 day  {}({})
""".format(pri_items[1],pri_items[0],count_items[0],pri_items[4],count_items[4],pri_items[5],count_items[5],pri_items[3],count_items[3])

def print_time(tasks):
    running_total=0
    for task in tasks:
	running_total+=task['time']
    hours=running_total //60
    minutes=running_total -hours*60
    print("The total time for the set is {} minutes ({}:{})".format(running_total,hours,minutes))
    nowtime=time.time()+running_total*60
    print("Target finish time: {}".format(time.ctime(nowtime)))



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


def print_sorted_tasks(tasklist):
	for task in tasklist:
	   print(action_to_string(task))


def action_to_string(task):
    return "- [%s] %s,  %2s, \"%s\", %s" % (task['completed'], task['priority'].strip(),  task['time'], task['action'] , task['timestamp'])+ ''.join(task['extra'])

def write_to_waiting_list(toprint):
       with open(WAITACTIONS_LOC, 'a') as actions_file:
           actions_file.write(toprint)

def add(args):
	today = datetime.datetime.now()
	deadline=today+datetime.timedelta(days=7)
	date= deadline.strftime(TIMESTAMP_FORMAT)
        if args.content:
            toprint = "- [ ] %s,%s, \"%s\", %s\n" % (args.priority, args.time, args.content, date)
            write_to_archive(str(date)+", "+toprint)
	    if args.s:
		    print(toprint)
		    write_to_waiting_list(toprint)
            else:
		    write_to_file(toprint)



def run_melta():
    parser = setup_argument_list()
    args=parser.parse_args()
    if args.action == "count":
        print(print_actions(filter_actions(args),args))
    elif args.action == "sort":
	print_sorted_tasks(filter_actions(args))
    elif args.action == "add":
	add(args)
    elif args.action == "random":
        print_random(filter_actions(args))
    elif args.action == "next":
	args.o=True
	print_sorted_tasks([filter_actions(args)[0]])
    elif args.action == "time":
        print_time(filter_actions(args))
    elif args.action == "powerhour":
	print_sorted_tasks(powerhour(filter_actions(args)))
    else:
	print("Error, missing action")
    update_pri_if_different()



if __name__ == '__main__':
    run_melta()

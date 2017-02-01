#!/usr/bin/python
"A set of functions designed to make it easier to process a next actions list"
import csv
import time
import datetime
import operator
import os
#There are two copies of this file, one in Jurgen and one cpoies to the system path

TIMESTAMP_FORMAT = '%Y-%m-%d (%a) -  %H:%M:%S'


def get_sorted_actions():
    "returns a sorted list of nextActions"
    with open(os.environ['JURGEN'] + 'Jurgen/nextActions/nextActions.csv', 'rU') as actions_file:
        reader = csv.reader(actions_file, skipinitialspace=True)
        lines = filter(None, reader)
        tasklist = sorted(lines, key=operator.itemgetter(5), reverse=True)
        tasklist.sort(key=lambda item: datetime.datetime.strptime(
            item[5], TIMESTAMP_FORMAT))
        return tasklist


def get_action_age_info(tasklist):
    "prints out the number of nextactions of each age in a current nextactions"
    dayold, threedayold, weekold = (0, 0, 0)
    for row in tasklist:
        datestring = row[5]
        timestamp_on_action = time.strptime(
            datestring.strip(), TIMESTAMP_FORMAT)
        age = time.time() - time.mktime(timestamp_on_action)
        if age > 60 * 60 * 24:
            dayold += 1
            if age > 60 * 60 * 24 * 3:
                threedayold += 1
                if age > 60 * 60 * 24 * 7:
                    weekold += 1
    return (len(tasklist), datetime.date.today(), time.time(), weekold, dayold, threedayold)

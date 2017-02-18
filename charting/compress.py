#!/home/joereddington/env/bin/python
import numpy as np
import time
import matplotlib.pyplot as plt
import os
#from scipy.interpolate import spline


def myround(x, base=24*3600):
        return int(base * round(float(x)/base))


def processFile(filename):
        file = open(filename)
        lastrawline = "Hello"
        rawline = file.readline()
        # the array we have is going to be horizonal when we need vertical. So
        # we have to deal with that.
        count = 0
        splitline = "hello world".split()
        outString = []
        for rawline in file:
                lastsplitline = splitline
                splitline = rawline.split()
                count = count+1
                if splitline[1] != lastsplitline[1]:
                        outString.append(rawline)
        return outString

toFile= processFile(os.environ['JURGEN'] + "Jurgen/tracking/priority.txt")

f = open(os.environ['JURGEN'] + "Jurgen/tracking/priCompressed.txt", 'w')
for item in toFile:
        f.write("%s" % item)
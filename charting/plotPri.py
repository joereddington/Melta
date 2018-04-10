#!/home/joereddington/env/bin/python
import numpy as np
import time
import matplotlib.pyplot as plt
import os
import argparse

#Todo


# Plan for adding the long term charting
# 1. Get working locally by adding a argparse that includes the source, and number of days
# 2. Include the compress function and add a switch to use it.
# 3. That means that all we need is the right commands and we're laughing. This
# is actually a reasonable

# Next action - argparse


SOURCE= os.environ['JURGEN']+"Jurgen/data/priority.txt"
DEST = "/home/joereddington/joereddington.com/stress/priority.png"
DAYS = 7
SMOOTHING=5

class ProductivityPlotter():
	"Class designed to take a Jurgen-formatted file and turn it into a graph"
	def __init__(self,source,dest,days):
		self.source=source
		self.dest=dest
		self.days=days

	def smooth(self,y, box_pts=SMOOTHING):
	    box = np.ones(box_pts)/box_pts
	    y_smooth = np.convolve(y, box, mode='same')
	    return y_smooth#from stackexcahnge

	def myround(self,x, base=24*3600):
	    return int(base * round(float(x)/base))

	def processFile(self):
		dayold, weekold,threedayold,seconds,now=([],[],[],[],[])
		count=0
		with open(self.source) as file:
			lastrawline="Hello"
			rawline = file.readline()
			#the array we have is going to be horizonal when we need vertical. So we have to deal with that.
			for rawline in file:
				splitline=rawline.split(',')
				dayold.insert(0,int(splitline[4]))
				threedayold.insert(0,int(splitline[5]))
				weekold.insert(0,int(splitline[3]))
				seconds.insert(0,int(splitline[2]))
				now.insert(0,int(splitline[0]))
				count=count+1
		return (seconds,now,dayold,threedayold,weekold)

	def graph(self,seconds,now, dayold, threedayold,weekold):
		dis=4*24*60*60
		x = np.array(seconds[-dis:])
		ynow  = self.smooth(np.array(now))
		yday  = self.smooth(np.array(dayold))
		y3day = self.smooth(np.array(threedayold))
		yweek = self.smooth(np.array(weekold))
		plt.plot(x,ynow, 'blue')
		plt.plot(x,yday, 'green')
		plt.plot(x,y3day,'purple')
		plt.plot(x,yweek, 'red')
		currenttime=int(seconds[0])
		lastweek=self.myround(currenttime-self.days*24*3600)
		plt.xlim(lastweek, currenttime-1000)
		plt.ylim(ymax=500)
		ticks=np.arange(lastweek,currenttime,24*3600)
		labels=[time.strftime("%a", time.gmtime(x)) for x in ticks]
		plt.xticks(ticks,labels)
		plt.grid()
		plt.savefig(self.dest)

	def get_graph(self):
		a=self.processFile()
		self.graph(a[0],a[1],a[2],a[3],a[4])
		print "%s written with output from %s"%(self.dest, self.source)

if __name__ == "__main__":
	a=ProductivityPlotter(SOURCE,DEST,DAYS)
	a.get_graph()


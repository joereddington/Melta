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


DEST = "priority.png"
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
                import calendar
                import time
                current_seconds=calendar.timegm(time.gmtime())
                seconds_at_start=current_seconds-(60*60*24*self.days)
		dayold, weekold,threedayold,seconds,now=([],[],[],[],[])
		count=0
		with open(self.source) as file:
			lastrawline="Hello"
			rawline = file.readline()
			#the array we have is going to be horizonal when we need vertical. So we have to deal with that.
			for rawline in file:
			     splitline=rawline.split(',')
                             if seconds_at_start < splitline[2]:
                                dayold.insert(0,int(splitline[4]))
                                threedayold.insert(0,int(splitline[5]))
                                weekold.insert(0,int(splitline[3]))
                                seconds.insert(0,int(splitline[2]))
                                now.insert(0,int(splitline[0]))
		return (seconds,now,dayold,threedayold,weekold)

	def graph(self,seconds,now, dayold, threedayold,weekold):
                print len(seconds)
		#dis=4*24*60*60
		#x = np.array(seconds[-dis:])
		x = np.array(seconds)
		ynow  = self.smooth(np.array(now))
		yday  = self.smooth(np.array(dayold))
		y3day = self.smooth(np.array(threedayold))
		yweek = self.smooth(np.array(weekold))
		plt.plot(x,ynow, 'blue')
		plt.plot(x,yday, 'green')
		plt.plot(x,y3day,'purple')
		plt.plot(x,yweek, 'red')
                import calendar
                import time
                current_seconds=calendar.timegm(time.gmtime())
                seconds_at_start=current_seconds-(60*60*24*self.days)
		plt.xlim(seconds_at_start, current_seconds-1000)
		plt.ylim(ymax=500)
		ticks=np.arange(seconds_at_start,current_seconds,24*3600)
		labels=[time.strftime("%a", time.gmtime(x)) for x in ticks]
		plt.xticks(ticks,labels)
		plt.grid()
		plt.savefig(self.dest)

	def get_graph(self):
		a=self.processFile()
		self.graph(a[0],a[1],a[2],a[3],a[4])
		print "%s written with output from %s"%(self.dest, self.source)


def setup_argument_list():
    "creates and parses the argument list for Watson"
    parser = argparse.ArgumentParser( description="creates the priority chart")
    parser.add_argument('-f', nargs="?", help="File to use for data")
    parser.add_argument('-c', nargs="?" , help="Should we compress")
    parser.add_argument( '-d', nargs="?", help="days")
    parser.add_argument( '-o', action='store_true', help="outputfile")
    parser.set_defaults(verbatim=False)
    return parser.parse_args()



if __name__ == "__main__":
        args=setup_argument_list()
        print args.f
	a=ProductivityPlotter(args.f,DEST,DAYS)
	a.get_graph()


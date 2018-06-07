#!/home/joereddington/env/bin/python
import numpy as np
import time
import matplotlib.pyplot as plt
import os
import argparse
import calendar_helper_functions as icalhelper

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
	def __init__(self,args,dest):
                self.args=args
		self.source=args.f
		self.dest=dest
                if args.o:
                    self.dest=args.o
		self.days=int(args.d)
                self.number_of_ticks=int(args.t)

	def smooth(self,y, box_pts=SMOOTHING):
	    box = np.ones(box_pts)/box_pts
	    y_smooth = np.convolve(y, box, mode='same')
	    return y_smooth#from stackexcahnge

	def array_to_lists(self,content):
                import calendar
                import time
                current_seconds=calendar.timegm(time.gmtime())
                seconds_at_start=current_seconds-(60*60*24*self.days)
		dayold, weekold,threedayold,seconds,now=([],[],[],[],[])
		count=0
                for rawline in content:
			     splitline=rawline.split(',')
                             if seconds_at_start < splitline[2]:
                                dayold.insert(0,int(splitline[4]))
                                threedayold.insert(0,int(splitline[5]))
                                weekold.insert(0,int(splitline[3]))
                                seconds.insert(0,int(splitline[2]))
                                now.insert(0,int(splitline[0]))
		return (seconds,now,dayold,threedayold,weekold)

	def graph(self,seconds,now, dayold, threedayold,weekold):
		x = np.array(seconds)
		ynow  = self.smooth(np.array(now))
		yday  = self.smooth(np.array(dayold))
		y3day = self.smooth(np.array(threedayold))
		yweek = self.smooth(np.array(weekold))
		blue, =plt.plot(x,ynow, 'blue')
		green, =plt.plot(x,yday, 'green')
		purple, =plt.plot(x,y3day,'purple')
		red, =plt.plot(x,yweek, 'red', label="7 days")
		plt.legend([blue, green, purple, red], ['All tasks', '1 day old', '3 days old', '7 days old'])
                import calendar
                import time
                current_seconds=calendar.timegm(time.gmtime())
                seconds_at_start=current_seconds-(60*60*24*self.days)
		plt.xlim(seconds_at_start, current_seconds)
		plt.ylim(ymax=500)
		distance_between_ticks=(current_seconds-seconds_at_start)/self.number_of_ticks
		ticks=np.arange(seconds_at_start-(distance_between_ticks/2),current_seconds+(distance_between_ticks/2),distance_between_ticks)
		labels=[time.strftime("%a", time.gmtime(x)) for x in ticks]
		labels.pop(0)
		print labels
		plt.xticks(ticks,labels)
#		plt.xticks(minorticks,labels,minor=True)
#		plt.grid()
		plt.savefig(self.dest)

	def get_graph(self):
                a=[]
                if self.args.c:
                    a=self.array_to_lists(compress(icalhelper.get_content(self.source)))
                else:
                    a=self.array_to_lists(icalhelper.get_content(self.source))
		self.graph(a[0],a[1],a[2],a[3],a[4])
		print "%s written with output from %s"%(self.dest, self.source)


def setup_argument_list():
    "creates and parses the argument list for Watson"
    parser = argparse.ArgumentParser( description="creates the priority chart")
    parser.add_argument('-f', nargs="?", help="File to use for data")
    parser.add_argument('-o', nargs="?" , help="outputfile")
    parser.add_argument( '-d', nargs="?", help="days", default=7)
    parser.add_argument( '-t', nargs="?", help="number of ticks", default=7)
    parser.add_argument( '-c', action='store_true', help="should we compress")
    parser.set_defaults(verbatim=False)
    return parser.parse_args()



def compress(content):
        # the array we have is going to be horizonal when we need vertical. So
        # we have to deal with that.
        count = 0
        splitline = "hello world".split()
        outString = []
        for rawline in content:
                lastsplitline = splitline
                splitline = rawline.split()
                count = count+1
                if splitline[1] != lastsplitline[1]:
                        outString.append(rawline)
        return outString


if __name__ == "__main__":
        args=setup_argument_list()
	a=ProductivityPlotter(args,DEST)
	a.get_graph()


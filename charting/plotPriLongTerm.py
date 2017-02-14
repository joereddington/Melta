#!/home/joereddington/env/bin/python
import plotPri
import numpy as np
import time
import matplotlib.pyplot as plt
import os


SOURCE= os.environ['JURGEN']+"melta/tracking/priCompressed.txt"
DEST = "/home/joereddington/joereddington.com/stress/priorityLong.png"
DAYS = 650
SMOOTHING=6

class LongTermPlotter(plotPri.ProductivityPlotter):

	def graph(self,seconds,now, dayold, threedayold,weekold):
		dis=100*24*60*60
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
		six_months_age=self.myround(currenttime-self.days*24*3600)
		plt.xlim(six_months_age, currenttime+24*3600)
		plt.ylim(ymax=500)
		ticks=np.arange(six_months_age,currenttime,90*24*3600)
		labels=[time.strftime("%b %Y", time.gmtime(x-1)) for x in ticks]
		plt.xticks(ticks,labels)
		plt.grid()
		plt.savefig(self.dest)

a=LongTermPlotter(SOURCE,DEST,DAYS)
a.get_graph()





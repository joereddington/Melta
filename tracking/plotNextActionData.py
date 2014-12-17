#!/home/joereddington/env/bin/python
import numpy as np
import time
import matplotlib.pyplot as plt
#from scipy.interpolate import spline

def myround(x, base=24*3600):
    return int(base * round(float(x)/base))

def processFile(filename):
	file = open(filename)
	lastrawline="Hello"
	rawline = file.readline()
	#the array we have is going to be horizonal when we need vertical. So we have to deal with that. 
	dayold=[]
	weekold=[]
	threedayold=[]
	seconds=[]
	now=[]
	count=0
	for rawline in file:
		splitline=rawline.split()
		dayold.insert(0,splitline[4])
		threedayold.insert(0,splitline[5])
		weekold.insert(0,splitline[3])
		seconds.insert(0,splitline[2])
		now.insert(0,splitline[0])
	        count=count+1	
	return (seconds,now,dayold,threedayold,weekold)

def graph(seconds,now, dayold, threedayold,weekold):
	dis=4*24*60*60
	x = np.array(seconds[-dis:])

	ynow = np.array(now)
	yday = np.array(dayold)
	y3day = np.array(threedayold)
	yweek = np.array(weekold)
	plt.plot(x,ynow, 'blue')
	plt.plot(x,yday, 'green')
	plt.plot(x,y3day,'purple')
	plt.plot(x,yweek, 'red')
#	plt.fill_between(x,ynow,yday,color='lightblue')
#	plt.fill_between(x,yday,y3day,color='green')
#	plt.fill_between(x,y3day,yweek,color='purple')
#	plt.fill_between(x,yweek,[0] *len(seconds),color='red')
	currenttime=int(seconds[0])
	lastweek=myround(currenttime-7*24*3600)
	plt.xlim(lastweek, currenttime)
	plt.ylim(ymax=100)
	ticks=np.arange(lastweek,currenttime,24*3600)
	labels=[time.strftime("%a", time.gmtime(x)) for x in ticks]
	plt.xticks(ticks,labels)
	plt.grid()
	plt.savefig('/home/joereddington/joereddington.com/stress/stress.png')

a=processFile("/home/joereddington/joereddington.com/Jurgen/tracking/results.txt")
print "file processed"
graph(a[0],a[1],a[2],a[3],a[4])

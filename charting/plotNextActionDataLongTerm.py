#!/home/joereddington/env/bin/python
import numpy as np
import time
import matplotlib.pyplot as plt
#from scipy.interpolate import spline
import plotPri



def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth


#def myround(x, base=24*3600):
#    return int(base * round(float(x)/base))

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
		splitline=rawline.split(',')
		dayold.insert(0,int(splitline[4]))
		threedayold.insert(0,int(splitline[5]))
		weekold.insert(0,int(splitline[3]))
		seconds.insert(0,int(splitline[2]))
		now.insert(0,int(splitline[0]))
	        count=count+1
	return (seconds,now,dayold,threedayold,weekold)

def graph(seconds,now, dayold, threedayold,weekold):
	dis=4*24*60*60
	x = np.array(seconds[-dis:])

	ynow = np.array(now)
	yday = np.array(dayold)
	y3day = np.array(threedayold)
	yweek = np.array(weekold)
	print "helo" +str( type(yweek))
	plt.plot(x,smooth(ynow,5), 'blue')
	plt.plot(x,smooth(yday,5), 'green')
	plt.plot(x,smooth(y3day,5),'purple')
	plt.plot(x,smooth(yweek,5), 'red')
#	plt.fill_between(x,ynow,yday,color='lightblue')
#	plt.fill_between(x,yday,y3day,color='green')
#	plt.fill_between(x,y3day,yweek,color='purple')
#	plt.fill_between(x,yweek,[0] *len(seconds),color='red')
	currenttime=int(seconds[0])
	lastweek=plotPri.myround(currenttime-180*24*3600)
	plt.xlim(lastweek, currenttime+60*60*24)
	plt.ylim(ymax=200)
	ticks=np.arange(lastweek,currenttime,30*24*3600)
	labels=[time.strftime("%b", time.gmtime(x)) for x in ticks]
	plt.xticks(ticks,labels)
	plt.grid()
	plt.savefig('/home/joereddington/joereddington.com/stress/priLongTerm.png')

a=processFile("/home/joereddington/meta/tracking/priCompressed.txt")
print "file processed"
graph(a[0],a[1],a[2],a[3],a[4])

import numpy as np 
%matplotlib inline
import matplotlib
import matplotlib.pyplot as plt 
from xml.dom import minidom
import time as tm
import datetime

class TouchPair:
	def __init__(self, classification, orientation, distance, time):
		self.classification = classification
		self.orientation = orientation
		self.distance = distance
		self.time = time

# form a touch pair with 3 calculated features
# TODO: normalize features
def pair(touchPoint, lastPoint, indexLastPoint):
	orientation = abs(float(touchPoint[1]) - float(lastPoint[1]))
	yDistance = abs(float(touchPoint[2]) - float(lastPoint[2]))
	xDistance = abs(float(touchPoint[3]) - float(lastPoint[3]))
	distance = np.sqrt([yDistance, xDistance])
	timeStr1 = touchPoint[4]
	timeFormat1 = datetime.datetime.strptime(timeStr1, "%Y/%m/%d %H:%M:%S:%f")
	time1 = tm.mktime(timeFormat1.timetuple())+(timeFormat1.microsecond/1000000.0)
	timeStr2 = lastPoint[4]
	timeFormat2 = datetime.datetime.strptime(timeStr2, "%Y/%m/%d %H:%M:%S:%f")
	time2 = tm.mktime(timeFormat2.timetuple())+(timeFormat2.microsecond/1000000.0)
	time = (time1 - time2)*1000
	global lastPoints
	if touchPoint[0] == lastPoint[0]:
		classification = "same"
		lastPoints[indexLastPoint] = touchPoint
	else:
		classification = "different"
		lastPoint.append(touchPoint)
	touchPair = TouchPair(classification, orientation, distance, time)
	global touchPairs
	touchPairs.append(touchPair)

if __name__ == "__main__":
	# read data from xml files
	xmldoc = minidom.parse('2 - Heuristics.xml')
	logs = xmldoc.getElementsByTagName('Point')
	touchPoints = [[0 for j in range(5)] for i in range(len(logs))]
	for i in range(len(logs)):
		touchPoints[i][0] = logs[i].attributes['student'].value
		touchPoints[i][1] = logs[i].attributes['o'].value
		touchPoints[i][2] = logs[i].attributes['y'].value
		touchPoints[i][3] = logs[i].attributes['x'].value
		touchPoints[i][4] = logs[i].attributes['timestamp'].value

	# global touchPairs
	touchPairs = []
	countPair = 0

	# initialize lastPoints with no.1 touchpoint
	# list columns are in order of student, o, y, x, timestamp
	lastPoints = [[touchPoints[0][0],
					touchPoints[0][1],
					touchPoints[0][2],
					touchPoints[0][3],
					touchPoints[0][4]]]

	for i in range(1, len(logs)):
		if len(lastPoints) == 1:
			pair(touchPoints[i], lastPoints[0], 0)
			countPair += 1
		else:
			for j in range(len(lastPoints)-1):
				pair(touchPoints[i], lastPoints[j], j)
				countPair += 1

	# train a MLP in weka using leave-one-out nested cross validation


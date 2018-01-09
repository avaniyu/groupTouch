import numpy as np 
%matplotlib inline
import matplotlib
import matplotlib.pyplot as plt 
from xml.dom import minidom
import csv
import time as tm
import datetime

class TouchPair:
	def __init__(self, classification, orientation, distance, time):
		self.classification = classification
		self.orientation = orientation
		self.distance = distance
		self.time = time

# form a touch pair with 3 calculated features
def pair(touchPoint, lastPoint, indexLastPoint):
	orientation = (abs(float(touchPoint[1]) - float(lastPoint[1]))) % 1
	yDistance = abs(float(touchPoint[2]) - float(lastPoint[2]))
	xDistance = abs(float(touchPoint[3]) - float(lastPoint[3]))
	distance = np.sqrt(yDistance*yDistance + xDistance*xDistance) / 1557
	time = (touchPoint[4] - lastPoint[4])*1000
	global deltaTimeList
	deltaTimeList.append(time)
	global lastPoints
	if touchPoint[0] == lastPoint[0]:
		classification = "same"
		lastPoints[indexLastPoint] = touchPoint
		# print("same")
	else:
		classification = "different"
		flagNewUser = True
		if (len(lastPoints)) > 1:
			for i in range(len(lastPoints)):
				if touchPoint[0] == lastPoints[i][0]:
					flagNewUser = False
					# print("flag")
		if flagNewUser == True:
			lastPoints.append(touchPoint)
	# 	print("different")
	# 	print(touchPoint[0])
	# 	print(lastPoint[0])
	# 	print(lastPoints)
	# print("------------------")
	touchPair = TouchPair(classification, orientation, distance, time)
	global touchPairs
	touchPairs.append(touchPair)	

if __name__ == "__main__":
	# read data from xml files
	no = "2"
	xmldoc = minidom.parse('2 - Heuristics.xml')
	logs = xmldoc.getElementsByTagName('Point')
	touchPoints = []
	deltaTimeList = []
	# remove outliers with elapsed time between touches above 80% of full dataset
	# for i in range(300):
	for i in range(len(logs)):
		if '?' not in logs[i].attributes['student'].value:
			if i == 0:
				tempTimeStr = logs[0].attributes['timestamp'].value
				tempTimeFormat = datetime.datetime.strptime(tempTimeStr, "%Y/%m/%d %H:%M:%S:%f")
				tempTime = tm.mktime(tempTimeFormat.timetuple())+(tempTimeFormat.microsecond/1000000.0)
				thisTime = tempTime
			else:
				thisTimeStr = logs[i].attributes['timestamp'].value
				thisTimeFormat = datetime.datetime.strptime(thisTimeStr, "%Y/%m/%d %H:%M:%S:%f")
				thisTime = tm.mktime(thisTimeFormat.timetuple())+(thisTimeFormat.microsecond/1000000.0)
			deltaTime = (thisTime - tempTime)*1000
			deltaTimeList.append(deltaTime)
			tempTime = thisTime
			touchPoints.append([logs[i].attributes['student'].value,
					logs[i].attributes['o'].value,
					logs[i].attributes['y'].value,
					logs[i].attributes['x'].value,
					thisTime,
					deltaTime])
	deltaTimeList = sorted(deltaTimeList, reverse=True)
	deltaTimeThreshold = deltaTimeList[int(0.2*len(deltaTimeList))]
	
	countDel = 0
	for i in range(len(touchPoints)-1):
		if touchPoints[i-countDel][5] > deltaTimeThreshold:
			del touchPoints[i-countDel]
			countDel += 1

	# global touchPairs
	touchPairs = []

	# initialize lastPoints with no.1 touchpoint
	# list columns are in order of student, o, y, x, timestamp
	lastPoints = [[touchPoints[0][0],
					touchPoints[0][1],
					touchPoints[0][2],
					touchPoints[0][3],
					touchPoints[0][4]]]

	countDiff = 0

	for i in range(1, len(touchPoints)):
		if len(lastPoints) == 1:
			pair(touchPoints[i], lastPoints[0], 0)
		else:
			for j in range(len(lastPoints)):
				pair(touchPoints[i], lastPoints[j], j)

	# normalize time feature and delete outliers
	deltaTimeList = sorted(deltaTimeList, reverse=True)
	deltaTimeThreshold = deltaTimeList[int(0.2*len(deltaTimeList))-1]

	countDel = 0
	for i in range(len(touchPairs)):
		if touchPairs[i-countDel].time > deltaTimeThreshold:
			del touchPairs[i-countDel]
			countDel += 1
		else:
			touchPairs[i-countDel].time = touchPairs[i-countDel].time / deltaTimeThreshold

	with open(no+"touchPairs.csv","a",newline="") as fp:
		writer = csv.writer(fp, dialect='excel', delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
		writer.writerow(["classification", "orientation", "distance", "time"])
		for i in range(len(touchPairs)):
			writer.writerow([touchPairs[i].classification,
							touchPairs[i].orientation,
							touchPairs[i].distance,
							touchPairs[i].time])
	file.close()

	# train a MLP in weka using leave-one-out nested cross validation


import numpy as np 
%matplotlib inline
import matplotlib
import matplotlib.pyplot as plt 
from xml.dom import minidom
# import itertools.combinations

class TouchPair:
	def __init__(self, classification, orientation, distance, time):
		self.classification = classification
		self.orientation = orientation
		self.distance = distance
		self.time = time

# form a touch pair with 3 calculated features
def pair(touchPoint, lastPoint):
	print("pair()")
	orientation = float(lastPoints[1])
	orientation = float(touchPoint[1]) - float(lastPoints[1])

	yDistance = abs(touchPoints[2] - lastPoints[2])
	xDistance = abs(touchPoints[3] - lastPoints[3])
	distance = np.sqrt([yDistance, xDistance])
	time = touchPoints[4] - lastPoints[4]
	if touchPoint.attributes['student'].value == lastPoints[0]:
		classification = "same"
	else:
		classification = "different"
	touchPair = TouchPair(classification, orientation, distance, time)
	global touchPairs
	touchPairs.append(touchPair)
	print("pair()")


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

		# initialize lastPoints with no.1 touchpoint
		# list columns are in order of student, o, y, x, timestamp
		lastPoints = [touchPoints[0][0],
						touchPoints[0][1],
						touchPoints[0][2],
						touchPoints[0][3],
						touchPoints[0][4]]
		# lastPoints[0].append('Jiayao')

		for i in range(1, len(logs)):
			if len(lastPoints) == 1:
				pair(touchPoints[i], lastPoints[0])
			else:
				for j in range(countStudents):
					pair(touchPoints[i], lastPoints[j])
					if touchPairs[-1][0] == "different":
						lastPoints.append(touchPoints[i])

		# train a MLP in weka using leave-one-out nested cross validation


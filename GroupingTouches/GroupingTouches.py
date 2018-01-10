import numpy as np 
%matplotlib inline
import matplotlib
import matplotlib.pyplot as plt 
from xml.dom import minidom
import csv
import time as tm
import datetime

class TouchPair:
	def __init__(self, orientation, distance, time):
		self.orientation = orientation
		self.distance = distance
		self.time = time

# form a touch pair with 3 calculated features
def pair(touchPoint, lastPoint):
	orientation = round((abs(float(touchPoint[0]) - float(lastPoint[0]))) % 1, 5)
	yDistance = abs(float(touchPoint[1]) - float(lastPoint[1]))
	xDistance = abs(float(touchPoint[2]) - float(lastPoint[2]))
	distance = round(np.sqrt(yDistance*yDistance + xDistance*xDistance) / 1557, 3)
	time = (touchPoint[3] - lastPoint[3])*1000

	paramTouchPair = TouchPair(orientation, distance, time)
	return paramTouchPair

def MLP(paramTouchPair, paramCountPairing):
	classification = predictionResults[paramCountPairing][6]
	print(paramCountPairing)
	return classification

if __name__ == "__main__":
	# read predictions from .csv
	with open("1touchPairsFullInfo.csv", "r") as f:
		reader = csv.reader(f)
		next(reader, None)
		predictionResults = list(reader)
		# prediction = predictionResults[][6]

	# read touch points from .xml
	indexNow = 0
	nameList = ["1 - Brainstorm", 
				"2 - Heuristics", "3 - Heuristics", "4 - Heuristics", "5 - Heuristics", 
				"6 - Map", "7 - Map", "8 - Map", "9 - Map",
				"10 - Resources", "11 - Resources", "12 - Resources", "13 - Resources",
				"14 - Wireframes", "15 - Wireframes", "16 - Wireframes", "17 - Wireframes"]
	xmldoc = minidom.parse(nameList[indexNow]+".xml")
	logs = xmldoc.getElementsByTagName('Point')

	touchPoints = []
	deltaTimeThreshold = 114275 # known from data preprocessing

	countInvalidData = 0
	for i in range(len(logs)):
		if '?' in logs[i].attributes['student'].value and logs[i].attributes['student'].value == "":
			# print("invalid data: missing ground truth")
			countInvalidData += 1
		else:
			if i+countInvalidData == 0:
				tempTimeStr = logs[0].attributes['timestamp'].value
				tempTimeFormat = datetime.datetime.strptime(tempTimeStr, "%Y/%m/%d %H:%M:%S:%f")
				tempTime = tm.mktime(tempTimeFormat.timetuple())+(tempTimeFormat.microsecond/1000000.0)
				thisTime = tempTime
			else:
				thisTimeStr = logs[i].attributes['timestamp'].value
				thisTimeFormat = datetime.datetime.strptime(thisTimeStr, "%Y/%m/%d %H:%M:%S:%f")
				thisTime = tm.mktime(thisTimeFormat.timetuple())+(thisTimeFormat.microsecond/1000000.0)
			deltaTime = (thisTime - tempTime)*1000
			if deltaTime > deltaTimeThreshold:
				# mark this point in grey due to too long time elapsed
				print("invalida data: too long time elapsed")
			else:
				touchPoints.append([logs[i].attributes['o'].value,
									logs[i].attributes['y'].value,
									logs[i].attributes['x'].value,
									thisTime,
									deltaTime])

	# initialize lastPoints with no.1 touchpoint
	# list columns are in order of o, y, x, timestamp, deltaTime, user 
	lastPoints = [[touchPoints[0][0],
					touchPoints[0][1],
					touchPoints[0][2],
					touchPoints[0][3],
					touchPoints[0][4],
					"user1"]]
	countUser = 1
	touchGroup = [[0]] # row: user; column: index of touch point

	countPairing = 0
	for i in range(1, len(touchPoints)):
		# print("---------")
		# print(touchPoints[i])
		flagFirstUser = True
		# flagNewUser = False

		if len(lastPoints) == 1:
			touchPair = pair(touchPoints[i], lastPoints[0])
			classification = MLP(touchPair, countPairing)
			countPairing += 1

			if classification == "same" and flagFirstUser == True:
				touchPoints[i].append("user1") # declare user
				touchGroup[0].append(i)
				lastPoints[0] = touchPoints[i]
				flagFirstUser = False
			elif classification == "different":
				countUser += 1
				touchPoints[i].append("user"+str(countUser))
				touchGroup.append([i])
				lastPoints.append(touchPoints[i])
				# flagNewUser = True

		else:
			countDiff = 0
			for j in range(len(lastPoints)):
				if countPairing <= 12805:
					touchPair = pair(touchPoints[i], lastPoints[j])
					print("countPairing = "+str(countPairing))
					classification = MLP(touchPair, countPairing)
					countPairing += 1

					if classification == "same" and flagFirstUser == True:
						touchPoints[i].append(lastPoints[j][-1]) # declare user
						touchGroup[j].append(i)
						lastPoints[j] = touchPoints[i]
						flagFirstUser = False
						countDiff = 0
						# flagNewUser = False
						print("same")
					elif classification == "different":
						countDiff += 1
						print("different")
						# print(countDiff)
			if countDiff == len(lastPoints):
				countUser += 1
				touchPoints[i].append("user"+str(countUser))
				touchGroup.append([i])
				lastPoints.append(touchPoints[i])
				# flagNewUser = True
				print("different")

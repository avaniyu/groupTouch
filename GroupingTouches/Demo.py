# Jan 11, 2018
# by Jiayao Yu

import numpy as np 
%matplotlib inline
import matplotlib
import matplotlib.pyplot as plt 
from xml.dom import minidom
import csv
import time as tm
import datetime
import tkinter as tk
from tkinter import ttk 

class Demo(tk.Frame):

	def __init__(self, parent=None):
		tk.Frame.__init__(self, parent)
		self.pack()
		self.GUI()
		# read predictions from .csv
		with open("1touchPairsFullInfo.csv", "r") as f:
			reader = csv.reader(f)
			next(reader, None)
			self.predictionResults = list(reader)

		# read touch points from .xml
		indexNow = 0
		nameList = ["1 - Brainstorm", 
					"2 - Heuristics", "3 - Heuristics", "4 - Heuristics", "5 - Heuristics", 
					"6 - Map", "7 - Map", "8 - Map", "9 - Map",
					"10 - Resources", "11 - Resources", "12 - Resources", "13 - Resources",
					"14 - Wireframes", "15 - Wireframes", "16 - Wireframes", "17 - Wireframes"]
		xmldoc = minidom.parse(nameList[indexNow]+".xml")
		self.logs = xmldoc.getElementsByTagName('Point')
		self.allTouchPoints = []
		self.touchPoints = []	# removed outliers on elapsed time
		self.deltaTimeThreshold = 114275 # known from data preprocessing

	def GUI(self):
		self.colors = ['red', 'blue', 'yellow', 'green', 'grey', 'black', 'white', 'cyan']
		self.frameUserIndicator = tk.Canvas(self)
		self.frameControlPanel = tk.Canvas(self)
		self.frameTableTop = tk.Canvas(self)

		self.frameUserIndicator.grid(row=0, column=0)
		self.frameControlPanel.grid(row=0, column=1)
		self.frameTableTop.grid(row=1, column=0, columnspan=2)

		# user indicators
		amountUsers = 2
		self.userIndicators = [0 for i in range(amountUsers)]
		for i in range(amountUsers):
			self.userIndicators[i] = tk.Label(self.frameUserIndicator, 
									text="User "+str(i+1), background=self.colors[i], foreground='white')
			self.userIndicators[i].grid(row=0, column=i)

		# control frame
		self.btnStart = tk.Button(self.frameControlPanel, text="Start", width=10)
		self.btnStart.grid(row=0, column=0)
		self.btnStart.bind('<Button-1>', self.groupTouch)

		# PixelSense tabletop
		self.tabletop = tk.Canvas(self.frameTableTop, borderwidth=2, relief=tk.GROOVE, width=651, height=419.4)
		self.tabletop.grid(row=0, column=0)

	def groupTouch(self, event):

		# read all logs into self.allTouchPoints[][]
		countInvalidData = 0
		for i in range(len(self.logs)):
			if '?' in self.logs[i].attributes['student'].value and self.logs[i].attributes['student'].value == "":
				countInvalidData += 1
			else:
				if i+countInvalidData == 0:
					tempTimeStr = self.logs[0].attributes['timestamp'].value
					tempTimeFormat = datetime.datetime.strptime(tempTimeStr, "%Y/%m/%d %H:%M:%S:%f")
					tempTime = tm.mktime(tempTimeFormat.timetuple())+(tempTimeFormat.microsecond/1000000.0)
					thisTime = tempTime
				else:
					thisTimeStr = self.logs[i].attributes['timestamp'].value
					thisTimeFormat = datetime.datetime.strptime(thisTimeStr, "%Y/%m/%d %H:%M:%S:%f")
					thisTime = tm.mktime(thisTimeFormat.timetuple())+(thisTimeFormat.microsecond/1000000.0)
				deltaTime = (thisTime - tempTime)*1000
				index = i - countInvalidData
				self.allTouchPoints.append([index, self.logs[i].attributes['o'].value,
											self.logs[i].attributes['y'].value,
											self.logs[i].attributes['x'].value,
											thisTime,
											deltaTime])
		

		self.drawTouch(0, 100, 100)

	def MLP(self, paramCountPairing):
		classification = self.predictionResults[paramCountPairing][6]
		return classification

	def drawTouch(self, paramO, paramY, paramX):
		rLong = 7
		rShort = 5
		anchors = [float(paramX)-rLong, float(paramY)+rShort, 
						float(paramX)+rLong, float(paramY)-rShort]
		self.tabletop.create_oval(anchors[0], anchors[1], anchors[2], anchors[3],
									fill=self.colors[0], outline='grey')

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Group Touch Demo")
    root.geometry("1000x600")
    root.resizable(width=False, height=False)
    Demo(root).mainloop()
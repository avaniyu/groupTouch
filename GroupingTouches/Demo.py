import tkinter as tk
from tkinter import ttk 
import numpy as np 
%matplotlib inline
import matplotlib
import matplotlib.pyplot as plt 
from xml.dom import minidom
import csv
import time as tm
import datetime

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
		self.touchPoints = []
		self.deltaTimeThreshold = 114275 # known from data preprocessing

	def GUI(self):
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
									text="User "+str(i+1), background='green', foreground='white')
			self.userIndicators[i].grid(row=0, column=i)

		# control frame
		self.btnStart = tk.Button(self.frameControlPanel, text="Start", width=10)
		self.btnStart.grid(row=0, column=0)
		self.btnStart.bind('<Button-1>', self.groupTouch)

		# PixelSense tabletop
		self.tabletop = tk.Canvas(self.frameTableTop, borderwidth=2, relief=tk.GROOVE, width=651, height=419.4)
		self.tabletop.grid(row=0, column=0)

	def groupTouch(event):
		print("groupTouch()")

	def MLP(paramCountPairing):
		classification = self.predictionResults[paramCountPairing][6]
		return classification

	def drawTouch():
		print("drawTouch()")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Group Touch Demo")
    root.geometry("1000x600")
    root.resizable(width=False, height=False)
    Demo(root).mainloop()
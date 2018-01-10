import csv

if __name__ == "__main__":
	index = 1
	with open("leave"+str(index)+"test.csv","a",newline="") as g:
		writer = csv.writer(g, dialect='excel', delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
		writer.writerow(["classification", "orientation", "distance", "time"])
		for i in range(1, 17):
			k = (index + i) % 17
			if k == 0:
				k = 17
			with open(str(k)+"touchPairs.csv", "r") as f:
				reader = csv.reader(f)
				next(reader, None)
				for row in reader:
					writer.writerow(row)
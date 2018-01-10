import csv

if __name__ == "__main__":
	# for i in range(1, 17):
	k = 1
	with open(str(k)+"touchPairsPredictions.csv", "r") as f:
		reader = csv.reader(f)
		next(reader, None)
		for row in reader:

			writer.writerow(row)
# code for combining the csv files from different runs

import csv
reader = csv.reader(open("./data/driving_log.csv"))
reader1 = csv.reader(open("../../../root/Desktop/train/recov/driving_log.csv"))
f = open("./data/combined.csv", "a")
writer = csv.writer(f)

for row in reader:
    writer.writerow(row)
f.close()
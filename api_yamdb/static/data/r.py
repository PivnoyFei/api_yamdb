import csv

reader = csv.reader(open('users.csv'))
data = list(reader)
print(len(data))
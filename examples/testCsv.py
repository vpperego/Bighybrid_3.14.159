import csv
with open('input.csv') as csvfile:
	reader = csv.reader(csvfile)
	fields = reader.next()
	l = reader.next()
	i = 0
	for f in fields:
		print( f + l[i])
		i = i + 1 

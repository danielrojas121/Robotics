import sys

with open(sys.argv[1], 'r') as f:
	for line in f:
		for num in line.split():
			print num

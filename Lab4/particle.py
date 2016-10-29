import sys
from turtle import *


def main():
	if len(sys.argv) == 2:
		readFile()
	else:
		print "Error: Must provide one coordinate text file as an argument"
		sys.exit(1)


def readFile():
	with open(sys.argv[1], 'r') as f:
		for line in f:
			for num in line.split():
				print num

main()
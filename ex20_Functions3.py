# Functions with Files

from sys import argv

script, inputFile = argv

def printAll(file):
	print file.read()
	

def rewindAll(file):
	file.seek(0)
	
	
def printLine(lineCount, file):
	print lineCount, file.readline()
	

currentFile = open(inputFile)

print "First let's print the whole file:\n"
printAll(currentFile)

print "Now let's rewind"
rewindAll(currentFile)

print "Let's print the first 3 lines:"
printLine(1, currentFile)
printLine(2, currentFile)
printLine(3, currentFile)

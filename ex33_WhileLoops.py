numberList = []

def addToList(maxNum, incrementCount):

	i = 0

	while (i < maxNum):
		print "At the top i is %d" % i
		numberList.append(i)
		
		i += incrementCount
		print "Numbers now: ", numberList
		print "At the bottom i is %d" % i


		
addToList(6, 1)	
	
print "The numbers: "

for num in numberList:
	print num 
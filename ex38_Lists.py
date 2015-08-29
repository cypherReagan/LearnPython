tenThingsStr = "Apples Oranges Crows Telephone Light Sugar"

print "Wait there are not 10 things in the list so let's fix it"

# Make list from string.
# split() call returns list using space as a separator.
stuffList = tenThingsStr.split(' ')
moreStuffList = ["Day", "Night", "Song", "Frisbee", "Corn", "Banana", "Girl", "Boy"]

# transfer (i.e. remove) items from moreStuff to stuff
while (len(stuffList) != 10):
	nextOne = moreStuffList.pop()
	print "Adding: ", nextOne
	stuffList.append(nextOne)
	print "Now there are %d items in stuff list." % len(stuffList)
	
	
print "stuffList = ", stuffList
print stuffList[1]
print stuffList[-1] # loops around list and prints last item
print stuffList.pop() # prints item just popped off (the last one)

# string join() returns string joined bt separator
print ' '.join(stuffList) # prints list items separated by a space
print '#'.join(stuffList[3:5]) # prints items 3 to 5 separated by a '#'

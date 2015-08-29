# Demonstrates for-loops and lists
countList = [1, 2, 3, 4, 5]
fruitList = ['apples', 'oranges', 'pears', 'apricots']
changeList = [1, 'pennies', 2, 'dimes', 3, 'quarters']

for number in countList:
	print "This is count %d" % number
	
	
for fruit in fruitList:
	print "This is fruit = %s" % fruit
	

# Since we don't know what type is in the mixed list
# use %r to reference elements.
for change in changeList:
	print "I got %r" % change
	
	
# We can build lists. Start with empty one.
elements = []

# then use the range function to do 0 to 5 counts
elements = (range(0,6))

for i in elements:
	print "Elements[%d] = %d" % (i, elements[i])

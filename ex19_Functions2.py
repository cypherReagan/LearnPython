# Functions and Variables

def cheeseAndCrackers (cheeseCount, crackerBoxCount):
	print "You have %d cheeses!" % (cheeseCount)
	print "You have %d boxes of crackers!" % (crackerBoxCount)
	
	
print "Give the numbers directly:"
cheeseAndCrackers(20, 30)

print "OR use variables from the script:"
cheeseAmount = 10
crackerAmount = 50
cheeseAndCrackers(cheeseAmount, crackerAmount)

print "We can even do math inside:"
cheeseAndCrackers(10+20, 30+50)

print "We can do combinations:"
cheeseAndCrackers(cheeseAmount +100, crackerAmount +200)
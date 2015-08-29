# Returning values from functions

def add(a, b,):
	print "ADDING %d + %d" % (a,b)
	return a + b
	
def substract(a,b):
	print "SUBTRACTING %d - %d" % (a,b)
	return a - b
	
	
def multiply(a, b):
	print "MULTIPLYING %d * %d" % (a,b)
	return a * b
	
def divide(a, b):
	print "DIVIDING %d / %d" % (a, b)
	
	
age = add(30, 5)
height = substract(78,4)
weight = multiply(110,2)
iq = divide(200,2)
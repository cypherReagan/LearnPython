# This is a review of everything so far

print "You\'d need to know \'bout escapes with \\ that don newlines and \t tabs."

poem = """
\tThe logic so firmly planted 
cannot discern \n the needs of love 
nor comprehend passion from intuition  
and requires an explanation 
\n\twhere there is none.
"""

print "-------------"
print "%s" % poem
print "-------------"

five = 10 - 2 + 3 - 6
print "This should be five: %d" % five

def secretFormula(startingPt):
	jellyBeans = startingPt * 500
	jars = jellyBeans / 1000
	crates = jars / 100
	return jellyBeans, jars, crates
	
	
startingPoint = 10000
beans, jars, crates = secretFormula(startingPoint)

print "With a starting point of %d " % startingPoint
print "We'd have %d beans, %d jars, %d crates" % (beans, jars, crates)

startingPoint /= 10

print " OR we could try it this way... with starting point = %d" % startingPoint
print "We'd have %d beans, %d jars, %d crates" % (secretFormula(startingPoint))


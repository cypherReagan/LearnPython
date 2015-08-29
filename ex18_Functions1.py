# this resembles the scripts with argv
def print_two(*args):
	arg1, arg2 = args
	print "arg1 = %r, arg2 = %r" % (arg1, arg2)
	

# the *args is pointless, do this instead
def print_two_again(arg1, arg2):
	print "arg1 = %r, arg2 = %r" % (arg1, arg2)
	
	
# this prints just one
def print_one(arg1):
	print"arg1 = %r" % (arg1)
	
	
# this prints nothing
def print_none():
	print "I got nothing"
	
	
print_two("Print", "Two")
print_two_again("Print", "Two... again")
print_one("Bazinga!")
print_none()
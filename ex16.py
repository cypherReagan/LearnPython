from sys import argv

script, filename = argv

print "We are going to erase %r." % filename
print "If you don't want to proceed then press CTRL-C(^C)"
print "If you want to proceed then hit RETURN"

raw_input("?")

print "Opening the file %r..." % filename
target = open(filename, 'w')

# The following is redundant. The w option in open() call
# will truncate automatically.
#print "Truncating the file..."
#target.truncate()

print "Now I'm going to ask you for 3 lines."

line1 = raw_input("line1: ")
line2 = raw_input("line2: ")
line3 = raw_input("line3: ")

target.write(line1 + "\n" + line2 + "\n" + line3 + "\n")


print"Closing file..."
target.close()


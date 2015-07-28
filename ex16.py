from sys import argv

script, filename = argv

print "We are going to erase %r." % filename
print "If you don't want to proceed then press CTRL-C(^C)"
print "If you want to proceed then hit RETURN"

raw_input("?")

print "Opening the file %r..." % filename
target = open(filename, 'w')

print "Truncating the file..."
target.truncate()

print "Now I'm going to ask you for 3 lines."

line = raw_input("line1: ")
target.write(line)
target.write("\n")

line = raw_input("line2: ")
target.write(line)
target.write("\n")


line = raw_input("line3: ")
target.write(line)
target.write("\n")


print"Closing file..."
target.close()


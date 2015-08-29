from sys import argv

script, user_name, who = argv
prompt = '---->'

print "Hi %s, I'm the %s of the script\n" % (user_name, script)
print "I'd like to ask you a few questions about %s." % who

print "Do you like me %s?" % user_name
likes = raw_input(prompt)

print "Where do you live?"
lives = raw_input(prompt)

print "What kind of computer do you have?"
computer = raw_input(prompt)

print """
Alright, so you said %r about liking me.
You live in %r. Not sure where that is.
And you have a %r computer. Nice.
<<<<<<< HEAD
""" % (likes, lives, computer)
=======
""" % (likes, lives, computer)
>>>>>>> master

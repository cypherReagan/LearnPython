import hashmap

# create a mapping of state to abbreviation
statesList = hashmap.new()
hashmap.set(statesList, 'Oregon', 'OR')
hashmap.set(statesList, 'Florida', 'FL')
hashmap.set(statesList, 'California', 'CA')
hashmap.set(statesList, 'New York', 'NY')
hashmap.set(statesList, 'Michigan', 'MI')

# create a basic set of states and some cities in them
citiesList = hashmap.new()
hashmap.set(citiesList, 'CA', 'San Francisco')
hashmap.set(citiesList, 'MI', 'Detroit')
hashmap.set(citiesList, 'FL', 'Jacksonville')

#add some more cities
hashmap.set(citiesList, 'NY', 'New York')
hashmap.set(citiesList, 'OR', 'Portland')

# print some states
print '-' * 10
print "Michigan has: %s" % hashmap.get(citiesList, 'MI')
print "Florida has: %s" % hashmap.get(citiesList, 'FL')

# do it by using the state then cities dict
print '-' * 10
print "Michigan has: %s" % hashmap.get(citiesList, hashmap.get(statesList, 'Michigan'))
print "Florida has: %s" % hashmap.get(citiesList, hashmap.get(statesList, 'Florida'))

# print every abbreviation
print '-' * 10
hashmap.list(statesList)

# print every city in state
print '-' * 10
hashmap.list(citiesList)

print '-' * 10
state = hashmap.get(statesList, 'Texas')

if (not state):
	print "Sorry no Texas"
	
print "The city for the state 'TX' is: %s" % hashmap.get(citiesList, 'TX', 'Does Not Exist')
# Using Dictionaries

# create mapping of state to abbreviation
statesDict = {
	'Oregon': 'OR',
	'Florida': 'FL',
	'California': 'CA',
	'New York': 'NY',
	'Michigan': 'MI'
}

# create a basic set of states and some cities in them
citiesDict = {
	'CA': 'San Francisco',
	'MI': 'Detroit',
	'FL': 'Jacksonville'
}

# add more cities
citiesDict['NY'] = 'New York'
citiesDict['OR'] = 'Portland'

# print out some cities
print '-' * 10
print "NY State has: ", citiesDict['NY']
print "OR State has: ", citiesDict['OR']

# print some states
print '-' * 10
print "Michigan's abbrev. is: ", statesDict['Michigan']
print "Florida's abbrev. is: ", statesDict['Florida']

# do it by using the state then cities dict
print '-' * 10
print "Michigan has: ", citiesDict[statesDict['Michigan']]
print "Florida has: ", citiesDict[statesDict['Florida']]

# print every state abbreviateion
print '-' * 10
for abbrev, city in citiesDict.items():
	print "%s has the city %s" % (abbrev, city)
	
	
# now do both at the same time
print '-' * 10
for state, abbrev in statesDict.items():
	print "%s is abbreviated %s and has the city %s" % (state, abbrev, citiesDict[abbrev])

print '-' * 10	

# unsafe get 
#state = statesDict['Texas']

# saftely get state that might not be there
state = statesDict.get('Texas')

if (not state):
	print "Sorry no Texas"
	
# get a city with a default values
city = citiesDict.get('TX', 'Does Not Exitst')
print "The city for the state TX is %s" % city	

	
